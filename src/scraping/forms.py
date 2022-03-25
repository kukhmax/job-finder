from django import forms

from .models import Language, Location


class VacancyFindForm(forms.Form):
    """A form for selecting vacancies by
    location and programming language """
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label='Location',
        to_field_name='name',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='name',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language',
    )
