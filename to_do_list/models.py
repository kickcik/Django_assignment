from django.contrib.auth.models import User
from django.db import models

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

    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk': self.pk})  # 수정


    class Meta:
        verbose_name = '투두'
        verbose_name_plural = '투두 리스트'