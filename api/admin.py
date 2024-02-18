from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Task)
admin.site.register(models.TaskAssigned)
admin.site.register(models.Log)
