from django import forms
from django_summernote.widgets import SummernoteWidget

from to_do_list.models import ToDoList, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title', 'image', 'description', 'start_date', 'end_date',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        # 폼 필드가 렌더링될 때 사용할 HTML 위젯을 정의
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '댓글을 입력하세요...', 'rows': 3})
        }
        labels = {
            'content': '댓글'
        }