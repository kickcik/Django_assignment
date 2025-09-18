from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from to_do_list.forms import TodoForm
from to_do_list.models import ToDoList

@login_required
def todo_list(request):
    todo_lists = ToDoList.objects.filter(author=request.user)

    q = request.GET.get('q')
    if q:
        todo_lists = todo_lists.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(todo_lists, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        'todo_lists': todo_lists,
        'page_object': page_object,
    }
    return render(request, 'todo_list.html', context)

@login_required
def todo_info(request, todo_id):
    todo_list = get_object_or_404(ToDoList, pk=todo_id)
    context = {'todo_list': todo_list}
    return render(request, 'todo_info.html', context)

@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo =form.save(commit=False)
        todo.author = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'todo_id':todo.id}))
    context = {'form': form}

    return render(request, 'todo_create.html', context)

@login_required
def todo_update(request, todo_id):
    todo = get_object_or_404(ToDoList, pk=todo_id, author=request.user)

    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'todo_id':todo.id}))
    context = {
        'todo': todo,
        'form': form
    }
    return render(request, 'todo_update.html', context)

@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    todo = get_object_or_404(ToDoList, pk=todo_id, author=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))


