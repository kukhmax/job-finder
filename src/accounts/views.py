from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView

from .forms import LoginForm, UserRegistrationForm
from .models import MyUser


class UserCreateView(SuccessMessageMixin, CreateView):
    """View for create user."""

    model = MyUser
    success_url = reverse_lazy('accounts:success_reg')
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_message = 'User successfully registered'


class LoginUserView(SuccessMessageMixin, LoginView):
    """View for login page."""

    template_name = 'accounts/login.html'
    next_page = reverse_lazy('scraping:home')
    success_message = 'You are logged in'
    form_class = LoginForm


class LogoutUserView(SuccessMessageMixin, LogoutView):
    """View for logout page."""

    next_page = reverse_lazy('accounts:login')
    logout_message = 'You are logged out'


class SuccessRegistrationView(TemplateView):
    template_name = 'accounts/success_register.html'


class SettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    fields = ['location', 'language', 'send_email']
    template_name = 'accounts/update_settings.html'
    success_url = reverse_lazy('accounts:success_reg')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    
    model = MyUser
    success_url = reverse_lazy('scraping:home')
    template_name = 'accounts/delete_user_confirm.html'
    success_message = _('User successfully deleted')
    unable_to_change_others_message = _(
        'You do not have permission to change another user.',
    )
    deletion_error_message = _(
        'Cannot delete user because it is in use',
    )
