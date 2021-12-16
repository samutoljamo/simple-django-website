from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
import time
from .utils import send_email
from .tokens import email_confirmation_token_generator
from .models import User
from .forms import RegisterUserForm, LoginUserForm
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email, password = data['email'], data['password']
            print(email, password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "invalid email or password")
                return render(request, "accounts/login.html", {'form': form})
        return render(request, "accounts/login.html", {'form': form})

    else:
        return render(request, "accounts/login.html", {'form': LoginUserForm()})


def activate(request, uidb64, token):
    user = get_object_or_404(
        User, pk=force_text(urlsafe_base64_decode(uidb64)))
    if email_confirmation_token_generator.check_token(user, token):
        user.activate_email()
        login(request, user)
        return redirect(reverse("profile"))
    else:
        return HttpResponse("Something went wrong")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("login"))


class Register(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        if settings.USE_EMAIL_CONFIRMATION:
            context = {
                'user': user,
                'domain': get_current_site(self.request),
                'user_uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_confirmation_token_generator.make_token(user)
            }
            body = render_to_string('accounts/confirm_email.html', context)
            email = EmailMessage(
                subject="Email Confirmation",
                body=body,
                to=[user.email]
            )
            send_email(email)

            return HttpResponse("Confirm your email by clicking the link sent to your email")
        else:
            user.activate_email()
            login(self.request, user)
            return redirect(reverse("profile"))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        return super().post(request, *args, **kwargs)
