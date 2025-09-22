from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from to_do_list.forms import TodoForm, CommentForm
from to_do_list.models import ToDoList, Comment


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
    queryset = ToDoList.objects.all().prefetch_related("comments", "comments__author")
    template_name = 'todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by("-created_at")
        paginator = Paginator(comments, 5)
        context = super().get_context_data(**kwargs)  # 기본 context 가져오기
        context.update({
            "comment_form": CommentForm(),
            "page_obj": paginator.get_page(self.request.GET.get("page")),
        })
        return context

class TodoListCreateView(LoginRequiredMixin,CreateView):
    model = ToDoList
    template_name = 'todo_form.html'
    form_class = TodoForm

    def form_valid(self, form):
        print('이미지: ', self.request.FILES.get("image"))
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

class TodoListUpdateView(LoginRequiredMixin,UpdateView):
    model = ToDoList
    template_name = 'todo_form.html'
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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.todo = get_object_or_404(ToDoList, id=self.kwargs["todo_id"])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("todo:info", kwargs={"pk": self.kwargs["todo_id"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["content"]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("해당 댓글을 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("해당 댓글을 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.todo.id})