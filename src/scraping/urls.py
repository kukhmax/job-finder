from django.urls import path

from .views import VacancyFindView, vacancy_list

urlpatterns = [
    path('', VacancyFindView.as_view(), name='home'),
    path('vacancies/', vacancy_list, name='vacancies'),
]
