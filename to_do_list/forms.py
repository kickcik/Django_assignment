from django import forms

from to_do_list.models import ToDoList


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title', 'description', 'start_date', 'end_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }