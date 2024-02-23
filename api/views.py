from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.parsers import JSONParser
from . import serializers
from . import models
from django.shortcuts import get_object_or_404
import json


def add_log_entry(type, task=None, user=None):
    """
    Adds a log entry to the database.
    :param type: The type of log entry (e.g., 'Created', 'Updated', 'Deleted', 'Assigned').
    :param task: Optional; the Task instance related to the log entry.
    :param user: Optional; the CustomUsers instance related to the log entry.
    """
    log_entry = models.Log(
        type=type,
        task=task,
        user=user,
    )
    log_entry.save()


def add_task_assigned(task, user, isOwner=False):
    """
    Assigns a task to a user.
    :param task: The Task instance to be assigned.
    :param user: The CustomUsers instance to whom the task is assigned.
    """
    task_assigned = models.TaskAssigned(task=task, user=user, isOwner=isOwner)
    task_assigned.save()
    add_log_entry(
        "Assigned", task=task, user=user
    )  # Add a log entry for task assignment


@api_view(["GET", "POST"])  # Define allowed methods
@permission_classes([])  # No permission required
@authentication_classes([])  # No authentication required
def categories(request):
    """
    Handle GET requests: List all categories
    Handle POST requests: Create a new category
    """
    if request.method == "GET":
        query = models.Category.objects.all()  # Retrieve all Category objects
        query_serializer = serializers.CategorySerializer(
            query, many=True
        )  # Serialize the data
        return JsonResponse(query_serializer.data, safe=False)  # Return serialized data

    elif request.method == "POST":
        data = JSONParser().parse(request)  # Parse the incoming JSON data
        serializer = serializers.CategorySerializer(
            data=data
        )  # Deserialize the data to a Category object
        if serializer.is_valid():
            serializer.save()  # Save the new Category object to the database
            return JsonResponse(
                serializer.data, status=201
            )  # Return the newly created category
        return JsonResponse(
            {"message": serializer.errors}, status=400
        )  # Return errors if the data is invalid


@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def tasks(request, pk=None):
    """
    Handle GET request: Retrieve tasks assigned to a specific user
    """
    if request.method == "GET":
        tasks_assigned = models.TaskAssigned.objects.filter(user__id=int(pk))
        serializer = serializers.ViewTaskAssignedSerializer(tasks_assigned, many=True)
        return JsonResponse(serializer.data, safe=False)


def delete_task(task_id, user_id):
    task_assigned = get_object_or_404(
        models.TaskAssigned, task_id=task_id, user_id=user_id
    )
    if task_assigned:
        if task_assigned.isOwner:
            task_assigned.task.delete()
        else:
            task_assigned.delete()


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([])
@authentication_classes([])
def task(request, pk=None):
    """
    Handle GET request: Retrieve a specific task or list all tasks
    Handle POST request: Create a new task
    Handle PUT request: Update an existing task
    Handle DELETE request: Delete a task
    """
    if request.method == "GET":
        if pk:
            task = get_object_or_404(models.Task, pk=pk)
            serializer = serializers.ViewTaskSerializer(task)
        else:
            tasks = models.Task.objects.all()
            serializer = serializers.ViewTaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        serializer = serializers.TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            assign_users = request.data.get("assign_users", [])
            for i, user_id in enumerate(json.loads(assign_users)):
                user = get_object_or_404(models.CustomUsers, pk=user_id)
                if i == 0:
                    add_task_assigned(
                        task, user, True
                    )  # Assign the task to the first user with isOwner=True
                else:
                    add_task_assigned(task, user)  # Assign the task to other users
            add_log_entry("Created", task=task)  # Add a log entry for task creation
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({"message": serializer.errors}, status=400)

    elif request.method == "PUT":
        task = get_object_or_404(models.Task, pk=pk)
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            add_log_entry("Updated", task=task)  # Add a log entry for task update

            assign_users = request.data.get("assign_users", [])
            try:
                assign_users = json.loads(assign_users)
            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON format for assign_users"}, status=400
                )
            existing_assigned_users = models.TaskAssigned.objects.filter(task=task)

            existing_assigned_users.exclude(user__id__in=assign_users).delete()

            for user_id in assign_users:
                if not existing_assigned_users.filter(user__id=user_id).exists():
                    user = get_object_or_404(models.CustomUsers, pk=user_id)
                    add_task_assigned(task, user)  # Assign the task to the user

            return JsonResponse(serializer.data)
        return JsonResponse({"message": serializer.errors}, status=400)

    elif request.method == "DELETE":
        task_id = pk
        user_id = request.data.get("user_id", None)
        if user_id is None or user_id == "":
            return JsonResponse({"message": "user_id is required"}, status=400)
        delete_task(task_id, user_id)
        return JsonResponse({"message": "Task was deleted successfully"}, status=204)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([])
@authentication_classes([])
def task_assigned(request, pk=None):
    """
    Handle GET request: Retrieve a specific task assignment or list all
    Handle POST request: Create a new task assignment
    Handle PUT/PATCH request: Update an existing task assignment
    Handle DELETE request: Delete a task assignment
    """
    if request.method == "GET":
        if pk:
            task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
            serializer = serializers.ViewTaskAssignedSerializer(task_assigned)
        else:
            tasks_assigned = models.TaskAssigned.objects.all()
            serializer = serializers.ViewTaskAssignedSerializer(
                tasks_assigned, many=True
            )
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.TaskAssignedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            add_log_entry(
                "Assigned",
                task=serializer.validated_data["task"],
                user=serializer.validated_data["user"],
            )  # Add a log entry for task assignment
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({"message": serializer.errors}, status=400)

    elif request.method == "PUT":
        task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.TaskAssignedSerializer(
            task_assigned, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            add_log_entry(
                "Updated",
                task=serializer.validated_data["task"],
                user=serializer.validated_data["user"],
            )  # Add a log entry for task assignment update
            return JsonResponse(serializer.data)
        return JsonResponse({"message": serializer.errors}, status=400)

    elif request.method == "DELETE":
        task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
        task_assigned.delete()
        add_log_entry(
            "Deleted", task=task_assigned.task, user=task_assigned.user
        )  # Add a log entry for task assignment deletion
        return JsonResponse(
            {"message": "Task assignment was deleted successfully"}, status=204
        )


@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def log_entries(request, pk=None):
    """
    Handle GET request: Retrieve a specific log entry or list all
    """
    if request.method == "GET":
        if pk:
            log_entry = get_object_or_404(models.Log, pk=pk)
            serializer = serializers.ViewLogSerializer(log_entry)
        else:
            logs = models.Log.objects.all().order_by("-timestamp")  # Newest first
            serializer = serializers.ViewLogSerializer(logs, many=True)
        return JsonResponse(serializer.data, safe=False)
