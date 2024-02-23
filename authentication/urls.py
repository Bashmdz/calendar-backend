from django.urls import path, re_path
from . import views

urlpatterns = [
    # Validate user endpoint
    path("validate", views.validate, name="validate"),
    # Get all users endpoint
    path("users", views.users, name="users"),
    # Get single user endpoint
    path("user", views.user, name="user"),
    # Get user by ID endpoint
    re_path(r"^user/(?P<pk>[0-9]+)$", views.user),
]
