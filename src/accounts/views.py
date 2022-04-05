from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, LoginForm
from .models import MyUser


class UserCreateView(SuccessMessageMixin, CreateView):
    """View for create user."""

    model = MyUser
    success_url = reverse_lazy('success_reg')
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_message = 'User successfully registered'


class LoginUserView(SuccessMessageMixin, LoginView):
    """View for login page."""

    template_name = 'accounts/login.html'
    next_page = reverse_lazy('home')
    success_message = 'You are logged in'
    form_class = LoginForm


class LogoutUserView(SuccessMessageMixin, LogoutView):
    """View for logout page."""

    next_page = reverse_lazy('login')
    logout_message = 'You are logged out'


class SuccessRegistrationView(TemplateView):
    template_name = 'accounts/success_register.html'

