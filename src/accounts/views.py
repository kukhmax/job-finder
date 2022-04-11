import datetime as dt

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from scraping.models import Error

from .forms import ContactForm, LoginForm, UserCreationForm
from .models import MyUser

User = get_user_model()


class UserCreateView(SuccessMessageMixin, CreateView):
    """View for create user."""

    model = MyUser
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:success_reg')
    template_name = 'accounts/register.html'
    
    success_message = _('User successfully registered')


class LoginUserView(SuccessMessageMixin, LoginView):
    """View for login page."""

    template_name = 'accounts/login.html'
    next_page = reverse_lazy('scraping:home')
    success_message = _('You are logged in')
    form_class = LoginForm


class LogoutUserView(SuccessMessageMixin, LogoutView):
    """View for logout page."""

    next_page = reverse_lazy('accounts:login')
    logout_message = 'You are logged out'


class SuccessRegistrationView(TemplateView):
    template_name = 'accounts/success_register.html'


class SettingsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """View for update user settings"""
    model = MyUser
    fields = ['location', 'language', 'send_email']
    template_name = 'accounts/update_settings.html'
    success_url = reverse_lazy('scraping:home')
    success_message = _('User successfully updated')
    
   
    def get_context_data(self, **kwargs):
        contact_form = ContactForm()
        context = super().get_context_data(**kwargs)
        context['contact_form'] = contact_form
        return context



class UserDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    
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

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            location = data.get('location')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'location': location, 'language': language, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [{'location': location, 'language': language, 'email': email}]}
                Error(data=data).save()
            messages.success(request, 'Your data sent to administrator')
            return redirect('scraping:home')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
                


# class ContactFormView(FormView):
#     template_name = 'contact.html'
#     form_class = ContactForm
#     success_url = 'accounts:home'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super().form_valid(form)
