from django.urls import path

from .views import (
    ProjectListView, TaskListView,
    ProjectDetailView, TaskDetailView
)

app_name = 'projects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail')
]