from django.views.generic import TemplateView


class HomeView(TemplateView):
    """View of the home page.

    """
    template_name = 'home.html'
