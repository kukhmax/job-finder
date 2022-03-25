from django.views.generic import ListView
from django.views.generic.edit import FormView
from django_filters.views import FilterView

from .filters import VacancyFilter
from .forms import VacancyFindForm
from .models import Vacancy


class VacancyFindView(FilterView):
    """View of home page with search form"""
    filterset_class =  VacancyFilter

    template_name = 'scraping/home.html'
    # success_url = 'vacansies'

    # def get(self, request, *args, **kwargs):
    #     """Handle GET requests: instantiate a blank version of the form."""
    #     return self.render_to_response(self.get_context_data())


class VacancyListView(ListView):
    """List of found vacanies"""
    model = Vacancy
    filterset_class =  VacancyFilter

    template_name = 'scraping/vacancies.html'
    context_object_name = 'vacancies_list'
