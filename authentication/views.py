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


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def validate(request):
    if request.method == "POST":
        # VALIDATE A USER
        data = JSONParser().parse(request)
        Users = models.CustomUsers.objects.all()
        email = data["email"]
        password = data["password"]
        if email and password is not None:
            count = Users.filter(email=email).count()
            if count != 0:
                data = Users.filter(email=email).values("password").first()
                if (
                    check_password(password, data["password"])
                    or password == data["password"]
                ):
                    userData = Users.filter(email=email).first()
                    SerializedData = serializers.ViewUserSerializer(
                        userData, many=False
                    )
                    return JsonResponse(SerializedData.data, safe=False)
                else:
                    return JsonResponse({"message": "Incorrect password."}, safe=False)
            else:
                return JsonResponse(
                    {"message": "No account found."},
                    status=status.HTTP_200_OK,
                )
        return JsonResponse({"message": "empty"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def users(request):
    if request.method == "GET":
        # GET ALL USERS
        instances = models.CustomUsers.objects.filter(is_staff=False)
        objects = serializers.ViewUserSerializer(instances, many=True)
        return JsonResponse(objects.data)


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
