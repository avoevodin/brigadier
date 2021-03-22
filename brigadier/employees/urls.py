from django.urls import path

from .views import EmployeeListView

app_name = 'employees'
urlpatterns = [
    path('', EmployeeListView.as_view(), name='employees')
]