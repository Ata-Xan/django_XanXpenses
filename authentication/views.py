from django.core.mail.backends import console
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
import smtplib
from django.core.mail.backends.smtp import EmailBackend
# Create your views here.
class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username= data['username']
        # print('ata')
        if not str(username).isalnum():
            # 400 would be returned in case of error.
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'this username has already taken, choose another one.'}, status=409)

        return JsonResponse({'username_valid':True})




class EmailValidationView(View):
    def post(self, request):
        email = request.POST.get('email', None)
        if email:
            try:
                validate_email(email)
                return JsonResponse({'valid': True})
            except ValidationError:
                pass
        return JsonResponse({'valid': False})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
#         GET USER DATA
#         VALIDATE
#         CREATE A USER ACCOUNT
        print(request.POST);
        username = request.POST['username'];
        email = request.POST['email'];
        password = request.POST['password'];
        context = {
            'fieldValues': request.POST
        }

        # smtp_connection = EmailBackend(
        #     host=settings.EMAIL_HOST,
        #     port=settings.EMAIL_PORT,
        #     username=settings.EMAIL_HOST_USER,
        #     password=settings.EMAIL_HOST_PASSWORD,
        #     use_tls=settings.EMAIL_USE_TLS
        # )
        # print(smtp_connection.host, smtp_connection.port, smtp_connection.username,smtp_connection.password, smtp_connection.use_tls)
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False

                print('after sending email to ', email)
                user.save()

                # path_to view
                    # getting domain we are on
                    # relative url to verification
                    # encode uid
                    # token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)
                })
                activate_url = 'http://'+domain+link
                email_subject = "Activate your account"
                email_body = "Please use the following link to verify your account\n"+activate_url
                email_ = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                print('before sending email to ', email)
                email_.send(fail_silently=False)

                messages.success(request, 'Account has been successfully registered')
        return render(request, 'authentication/register.html')
class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            # print(id)
            user = User.objects.get(pk=id)
            # it means the user has already used the link
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:

                return redirect('login')

            user.is_active=True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as e:
            # print("Exception")
            pass

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, '+user.username+"You are now logged in.")
                    return redirect('expenses')


                else:
                    messages.error(request, 'Account is not active, please check you email')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all the fields.'
        )
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')


