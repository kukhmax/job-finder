from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from .models import Language, Location, Vacancy



class VacancyFilter(FilterSet):

    location = ModelChoiceFilter(
        queryset=Location.objects.all(),
        to_field_name='pk',
        label='Location',
        empty_label='--- Choose location ---',        
    )
    language = ModelChoiceFilter(
        queryset=Language.objects.all(),
        to_field_name='pk',
        label='Language',
        empty_label='--- Choose a programming language ---',
    )

    class Meta:
        model = Vacancy
        fields = ['location', 'language']
