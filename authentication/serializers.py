from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user model.
    """

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = models.CustomUsers
        fields = ["name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new custom user instance.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ViewUserSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing user details.
    """

    class Meta:
        model = models.CustomUsers
        fields = ["id", "name", "email", "timestamp", "is_staff"]
