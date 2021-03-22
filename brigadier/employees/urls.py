from django.urls import path

from .views import EmployeeListView, EmployeeDetailView

app_name = 'employees'
urlpatterns = [
    path('', EmployeeListView.as_view(), name='list'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='detail'),
]
