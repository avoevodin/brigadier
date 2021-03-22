from django.shortcuts import render

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    todo()
    """
    template_name = 'home.html'
