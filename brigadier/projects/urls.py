from django.urls import path

from .views import (
    ProjectListView, TaskListView,
    ProjectDetailView, TaskDetailView,
    ProjectCreateView, ProjectEditView,
    ProjectDeleteView, TaskCreateView,
    TaskEditView, TaskDeleteView,
    add_comment_to_task
)

app_name = 'projects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('add/', ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', ProjectEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
    path('tasks/add/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit', TaskEditView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/comment/', add_comment_to_task, name='add_comment_to_task'),
]
