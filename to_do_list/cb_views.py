from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from to_do_list.forms import TodoForm
from to_do_list.models import ToDoList


class TodoListView(LoginRequiredMixin,ListView):
    model = ToDoList
    template_name = 'todo_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = ToDoList.objects.filter(author=self.request.user).order_by('-created_at')

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class TodoListInfoView(DetailView):
    model = ToDoList
    template_name = 'todo_info.html'

class TodoListCreateView(LoginRequiredMixin,CreateView):
    model = ToDoList
    template_name = 'todo_create.html'
    form_class = TodoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.id})

class TodoListUpdateView(LoginRequiredMixin,UpdateView):
    model = ToDoList
    template_name = 'todo_update.html'
    form_class = TodoForm

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)

class TodoListDeleteView(LoginRequiredMixin,DeleteView):
    model = ToDoList

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('todo:list')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])