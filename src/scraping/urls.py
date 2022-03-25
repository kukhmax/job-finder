from django.urls import path

from .views import VacancyFindView, VacancyListView

urlpatterns = [
    path('', VacancyFindView.as_view(), name='home'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
]
