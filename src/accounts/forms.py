from django import forms
from .models import MyUser
from scraping.models import Location, Language


from django.contrib.auth.forms import AuthenticationForm, UsernameField


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Enter email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Enter your password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label = 'Enter your password again',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = MyUser
        fields = ('email',)
    
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("Passwords don't match")
        return data['password2']

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
    )


# class VacancyFindForm(forms.Form):
#     """A form for selecting vacancies by
#     location and programming language """
#     location = forms.ModelChoiceField(
#         queryset=Location.objects.all(),
#         label='Location',
#         to_field_name='name',
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     language = forms.ModelChoiceField(
#         queryset=Language.objects.all(),
#         to_field_name='name',
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label='Language',
#     )
#     send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
#                                     label='Send email')

#     class Meta:
#         model = MyUser
#         fields = ('location', 'language', 'send_email')
