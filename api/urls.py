from django.urls import path, re_path
from . import views

urlpatterns = [
    path("categories", views.categories, name="categories"),
    re_path(r"^task/(?P<pk>[0-9]+)$", views.task),
    path("task", views.task, name="task"),
    re_path(r"^task_assigned/(?P<pk>[0-9]+)$", views.task_assigned),
    path("task_assigned", views.task_assigned, name="task_assigned"),
    re_path(r"^log_entries/(?P<pk>[0-9]+)$", views.log_entries),
    path("log_entries", views.log_entries, name="log_entries"),
]
