from django.urls import path, re_path
from . import views

urlpatterns = [
    path("validate", views.validate, name="validate"),
    path("user", views.user, name="user"),
    re_path(r"^user/(?P<pk>[0-9]+)$", views.user),
]
