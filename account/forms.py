from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators

from account.models import User, Address


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تایید گذرواژه", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "your phone/email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "your password"}))


class OtpLoginRegisterForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "your phone"}))


class OtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "code ..."}),
                           validators=[validators.MaxLengthValidator(4)])


class AddAddressForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("is_active", "is_admin", "password")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
            "last_login": forms.HiddenInput(),
        }
