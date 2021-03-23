from django.urls import path

from .views import (
    EmployeeListView, EmployeeDetailView,
    EmployeeCreateView, EmployeeEditView,
    EmployeeDeleteView
)

app_name = 'employees'
urlpatterns = [
    path('', EmployeeListView.as_view(), name='list'),
    path('add/', EmployeeCreateView.as_view(), name='create'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', EmployeeEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='delete'),
]

