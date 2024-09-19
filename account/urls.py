from django.urls import path
from account import views

app_name = "account"
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("otp-login-register", views.OtpLoginRegisterView.as_view(), name="otp_login_register"),
    path("Otp", views.OtpView.as_view(), name="otp"),
    path("logout", views.log_out, name="logout"),
    path("add-address", views.AddAddressView.as_view(), name="add_address"),
    path("user-edit", views.UserEditView.as_view(), name="user_edit"),
]
