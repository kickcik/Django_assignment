"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from to_do_list import views as todo_list_views
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', todo_list_views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>', todo_list_views.todo_info, name='todo_info'),
    path('todo/create', todo_list_views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/update', todo_list_views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', todo_list_views.todo_delete, name='todo_delete'),
    path('cbv/', include('to_do_list.cb_urls')),

    #auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', users_views.sign_up, name='signup'),
    path('accounts/login', users_views.login, name='login'),

    #summernote
    path('summnernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)