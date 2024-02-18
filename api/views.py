from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.parsers import JSONParser
from . import serializers
from . import models


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
