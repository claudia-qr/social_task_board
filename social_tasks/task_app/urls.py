from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.login),
    path('tasks', views.tasks),
    path('tasks/delete/<int:id>', views.delete_task),
    path('tasks/edit/<int:id>', views.edit_task),
    path('tasks/update/<int:id>', views.update_task),
    path('tasks/new', views.new),
    path('create_task', views.create_task),
    path('account/<int:id>', views.account),
    path('profile/<int:id>', views.profile),
    path('account/update/<int:id>', views.update_account),
    path('add_comment/<int:id>', views.add_comment),
    path('like/<int:id>', views.add_like),
    path('tasks/<int:id>', views.complete_task),
    path('comm_edit/<int:id>', views.edit_comm),
    path('comm_delete/<int:id>', views.delete_comm)
]