from django.shortcuts import render

from to_do_list.models import ToDoList


def todo_list(request):
    todo_lists = ToDoList.objects.all()
    context = {'todo_lists': todo_lists}
    return render(request, 'todo_list.html', context)

def todo_info(request, todo_id):
    todo_list = ToDoList.objects.get(pk=todo_id)
    context = {'todo_list': todo_list}
    return render(request, 'todo_info.html', context)

