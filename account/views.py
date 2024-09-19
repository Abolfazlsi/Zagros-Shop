from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.views import View
from account.forms import LoginForm, OtpLoginRegisterForm, OtpForm, AddAddressForm, UserEditForm
from account.models import User, Otp
from django.utils.crypto import get_random_string
from uuid import uuid4
import random


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:home")
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]

            )
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("home:home")
            else:
                form.add_error("username", "invalid user data")
        else:
            form.add_error("username", "invalid user data")

        return render(request, "account/login.html", {"form": form})


class OtpLoginRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:home")
        form = OtpLoginRegisterForm()
        return render(request, "account/otp_login-register.html", {"form": form})

    def post(self, request):
        form = OtpLoginRegisterForm(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            phone = form.cleaned_data["phone"]

            token = str(uuid4())
            Otp.objects.create(phone=phone, code=code, token=token)
            print(code)
            return redirect(reverse("account:otp") + f"?token={token}")

        else:
            form.add_error("phone", "invalid user data")

        return render(request, "account/otp_login-register.html", {"form": form})


class OtpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:home")
        form = OtpForm()
        return render(request, "account/verify.html", {"form": form})

    def post(self, request):
        token = request.GET.get("token")
        form = OtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd["code"], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return redirect("home:home")
            else:
                form.add_error("code", "invalid code")

        else:
            form.add_error("code", "invalid data")

        return render(request, "account/verify.html", {"form": form})


class AddAddressView(View):
    def get(self, request):
        form = AddAddressForm()
        return render(request, "account/add_address.html", {"form": form})

    def post(self, request):
        form = AddAddressForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
            else:
                form.add_error("full_name", "you are not login.")
        else:
            form.add_error("full_name", "invalid data")

        return render(request, "account/add_address.html", {"form": form})


class UserEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = UserEditForm(instance=user)
        return render(request, "account/user_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home:home")
        return render(request, "account/user_edit.html", {"form": form})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home:home")
    else:
        return redirect("home:home")
