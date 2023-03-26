from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView
from django.urls import path
# if we want to make an exception for our post requests we would use this
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('logout', LogoutView.as_view(),name="logout"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate")
]


