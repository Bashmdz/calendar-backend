from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Task(models.Model):
    title = models.CharField(max_length=256)
    priority = models.CharField(
        max_length=10,
        choices=[("Important", "Important"), ("Medium", "Medium"), ("Low", "Low")],
        default="Medium",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    progress = models.CharField(
        max_length=10,
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
