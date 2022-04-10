from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
# from scraping.models import Language, Location
from django.core.exceptions import ValidationError

from .models import MyUser

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(
        label='Enter email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label = 'Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

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
