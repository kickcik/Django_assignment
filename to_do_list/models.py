from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse


class ToDoList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=True, upload_to="todo/%Y/%m/%d")
    thumbnail = models.ImageField(null=True, blank=True, upload_to="todo/%Y/%m/%d/thumbnail")

    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk': self.pk})  # 수정

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300, 300))

        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = '투두'
        verbose_name_plural = '투두 리스트'

class Comment(models.Model):
    todo = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글목록'
        ordering = ['-created_at', '-id']