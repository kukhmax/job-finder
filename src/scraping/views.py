from django.views.generic import ListView
from django.views.generic.edit import FormView
from django_filters.views import FilterView
from django.shortcuts import render

from .filters import VacancyFilter
# from .forms import VacancyFindForm
from .models import Vacancy


class VacancyFindView(FilterView):
    """View of home page with search form"""
    filterset_class =  VacancyFilter

    template_name = 'scraping/home.html'
    success_url = 'vacansies'



class VacancyListView(FilterView, ListView):
    """List of found vacanies"""
    model = Vacancy
    filterset_class =  VacancyFilter

    template_name = 'scraping/vacancies.html'
    context_object_name = 'filter'
    paginate_by = 15


# def vacancy_list(request):
#     f = VacancyFilter(request.GET, queryset=Vacancy.objects.all())
#     return render(request, 'scraping/vacancies.html', {'filter': f})