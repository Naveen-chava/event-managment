from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("signup", views.UserSignupView.as_view(), name="handler-user-signup"),
    path("login", views.UserLoginView.as_view(), name="handler-user-login"),
    path("userprofile", views.UserProfileView.as_view(), name="handler-user-profile"),
    path("staffprofile", views.StaffProfileView.as_view(), name="handler-staff-profile"),
]
