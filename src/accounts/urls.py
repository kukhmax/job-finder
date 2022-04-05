from django.urls import path

from .views import (LoginUserView, LogoutUserView, SuccessRegistrationView,
                    UserCreateView)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('success_registaration/', SuccessRegistrationView.as_view(), name='success_reg'),
]
