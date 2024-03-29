from django.db import models
from django.utils import timezone
from authentication.models import CustomUsers

# Create your models here.


# Category model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Task model
class Task(models.Model):
    title = models.CharField(max_length=256)
    priority = models.CharField(
        max_length=10,
        choices=[("Important", "Important"), ("Medium", "Medium"), ("Low", "Low")],
        default="Medium",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    progress = models.CharField(
        max_length=11,
        choices=[("Open", "Open"), ("In Progress", "In Progress"), ("Done", "Done")],
        default="Open",
    )
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField()
    attachment = models.FileField(
        null=True, blank=True, upload_to="static/attachments/"
    )
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Tasks"


# TaskAssigned model
class TaskAssigned(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    isOwner = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.task} - {self.user}"

    class Meta:
        verbose_name_plural = "Task Assigned"


# Log model
class Log(models.Model):
    type = models.CharField(max_length=10, default="")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        CustomUsers, on_delete=models.CASCADE, blank=True, null=True
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.task} - {self.user}"

    class Meta:
        verbose_name_plural = "Logs"
