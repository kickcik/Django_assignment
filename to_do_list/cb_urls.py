from django.urls import path
from to_do_list import cb_views

app_name = 'todo'
urlpatterns =[
    path('todo/', cb_views.TodoListView.as_view(), name='list'),
    path('todo/<int:pk>', cb_views.TodoListInfoView.as_view(), name='info'),
    path('todo/create', cb_views.TodoListCreateView.as_view(), name='create'),
    path('todo/<int:pk>/update', cb_views.TodoListUpdateView.as_view(), name='update'),
    path('todo/<int:pk>/delete', cb_views.TodoListDeleteView.as_view(), name='delete'),
]