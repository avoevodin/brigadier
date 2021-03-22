from django.urls import path

from .views import (
    EmployeeListView, EmployeeDetailView,
    EmployeeCreateView, EmployeeEditView
)

app_name = 'employees'
urlpatterns = [
    path('', EmployeeListView.as_view(), name='list'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='detail'),
    path('add/', EmployeeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', EmployeeEditView.as_view(), name='edit'),
]
