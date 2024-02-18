from django.shortcuts import render
from rest_framework import status
from . import serializers
from . import models
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password

# Create your views here.


@api_view(["POST", "PUT", "GET", "DELETE"])
@permission_classes([])
@authentication_classes([])
def user(request, pk=None):
    if request.method == "GET":
        # GET A USER BY ID
        if pk is None:
            return JsonResponse({"message": "No user id given!"}, safe=False)
        data = JSONParser().parse(request)
        instance = models.CustomUsers.objects.get(pk=int(pk))
        object = serializers.ViewUserSerializer(instance, many=False)
        return JsonResponse(object.data, safe=False)
    if request.method == "POST":
        # ADD A USER
        data = JSONParser().parse(request)
        serializer = serializers.CustomUserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            SerializedData = serializers.ViewUserSerializer(instance, many=False)
            return JsonResponse(SerializedData.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return JsonResponse(
            {"message": serializer.errors}, status=status.HTTP_202_ACCEPTED
        )
    if request.method == "PUT":
        # UPDATE A USER
        if pk is None:
            return JsonResponse({"message": "No user id given!"}, safe=False)

        try:
            instance = models.CustomUsers.objects.get(pk=int(pk))
        except models.CustomUsers.DoesNotExist:
            return JsonResponse(
                {"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        data = JSONParser().parse(request)

        if data["newPassword"]:
            data["password"] = data["newPassword"]

        serializer = serializers.CustomUserSerializer(
            instance, data=data, partial=True
        )  # Allow partial updates

        if serializer.is_valid():
            instance = serializer.save()
            serialized_data = serializers.ViewUserSerializer(instance, many=False)
            return JsonResponse(serialized_data.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return JsonResponse(
            {"message": serializer.errors}, status=status.HTTP_202_ACCEPTED
        )

    elif request.method == "DELETE":
        if pk is None:
            return JsonResponse({"message": "No user id given!"}, safe=False)
        try:
            user = models.CustomUsers.objects.get(pk=int(pk))
            user.delete()
            return JsonResponse({"message": "User deleted successfully!"}, safe=False)
        except models.CustomUsers.DoesNotExist:
            return JsonResponse({"message": "User not found!"}, safe=False)
