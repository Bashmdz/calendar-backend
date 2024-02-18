from rest_framework import serializers
from . import models
from authentication.serializers import ViewUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class ViewTaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = models.Task
        fields = "__all__"


class TaskAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskAssigned
        fields = "__all__"


class ViewTaskAssignedSerializer(serializers.ModelSerializer):
    user = ViewUserSerializer()
    task = ViewTaskSerializer()

    class Meta:
        model = models.TaskAssigned
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = "__all__"


class ViewLogSerializer(serializers.ModelSerializer):
    user = ViewUserSerializer()
    task = ViewTaskSerializer()

    class Meta:
        model = models.Log
        fields = "__all__"
