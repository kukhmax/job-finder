from django.urls import path

from .views import (LoginUserView, LogoutUserView, SuccessRegistrationView,
                    UserCreateView, SettingsUpdateView, UserDeleteView)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('success_registaration/', SuccessRegistrationView.as_view(), name='success_reg'),
    path('<int:pk>/account-settings/', SettingsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
