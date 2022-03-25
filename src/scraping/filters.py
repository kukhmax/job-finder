from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from .models import Language, Location, Vacancy



class VacancyFilter(FilterSet):

    location = ModelChoiceFilter(
        queryset=Location.objects.all(),
        to_field_name='name',
        label='Location',
    )
    language = ModelChoiceFilter(
        queryset=Language.objects.all(),
        to_field_name='name',
        label='Language',
    )

    class Meta:
        model = Vacancy
        fields = ['location', 'language']
