from django.urls import path

from .views import VacancyListView

urlpatterns = [
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
]
