from django.views.generic import ListView

from .models import Vacancy


class VacancyListView(ListView):
    model = Vacancy

    template_name = 'scraping/vacancies.html'
    context_object_name = 'vacancies'
