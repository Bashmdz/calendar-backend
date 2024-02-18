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


@api_view(["GET", "POST"])  # Define allowed methods
@permission_classes([])  # No permission required
@authentication_classes([])  # No authentication required
def categories(request):
    # Handle GET requests: List all categories
    if request.method == "GET":
        query = models.Category.objects.all()  # Retrieve all Category objects
        query_serializer = serializers.CategorySerializer(
            query, many=True
        )  # Serialize the data
        return JsonResponse(query_serializer.data, safe=False)  # Return serialized data

    # Handle POST requests: Create a new category
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


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([])
@authentication_classes([])
def task(request, pk=None):
    # Handle GET request: Retrieve a specific task or list all tasks
    if request.method == "GET":
        if pk:
            # Retrieve a specific task by pk (id)
            task = get_object_or_404(models.Task, pk=pk)
            serializer = serializers.TaskSerializer(task)
        else:
            # List all tasks
            tasks = models.Task.objects.all()
            serializer = serializers.TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Handle POST request: Create a new task
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # Handle PUT/PATCH request: Update an existing task
    elif request.method == "PUT":
        task = get_object_or_404(models.Task, pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Handle DELETE request: Delete a task
    elif request.method == "DELETE":
        task = get_object_or_404(models.Task, pk=pk)
        task.delete()
        return JsonResponse({"message": "Task was deleted successfully"}, status=204)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([])
@authentication_classes([])
def task_assigned(request, pk=None):
    # Handle GET request: Retrieve a specific task assignment or list all
    if request.method == "GET":
        if pk:
            # Retrieve a specific task assignment by pk (id)
            task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
            serializer = serializers.TaskAssignedSerializer(task_assigned)
        else:
            # List all task assignments
            tasks_assigned = models.TaskAssigned.objects.all()
            serializer = serializers.TaskAssignedSerializer(tasks_assigned, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Handle POST request: Create a new task assignment
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.TaskAssignedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # Handle PUT/PATCH request: Update an existing task assignment
    elif request.method == "PUT":
        task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.TaskAssignedSerializer(
            task_assigned, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Handle DELETE request: Delete a task assignment
    elif request.method == "DELETE":
        task_assigned = get_object_or_404(models.TaskAssigned, pk=pk)
        task_assigned.delete()
        return JsonResponse(
            {"message": "Task assignment was deleted successfully"}, status=204
        )
