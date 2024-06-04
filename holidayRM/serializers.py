from rest_framework import serializers
from .models import Vacation
from django.contrib.auth.models import User


class VacationSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize
    and deserialize Vacation instances into JSON format for API endpoints.

    Attributes:
        model (Model): The model that this serializer is associated with, which is the Vacation model.
        fields (list): The fields of the Vacation model that should be included in the serialized representation.
    """
    class Meta:
        model = Vacation
        fields = ['id', 'date_from', 'date_to']


class VacationGetSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize
    and deserialize Vacation instances into JSON format for API endpoints, including the user and approval status.

    Attributes:
        model (Model): The model that this serializer is associated with, which is the Vacation model.
        fields (list): The fields of the Vacation model that should be included in the serialized representation.
    """
    class Meta:
        model = Vacation
        fields = ['id', 'date_from', 'date_to', 'user', 'is_approved']


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize
    and deserialize User instances into JSON format for API endpoints.

    Attributes:
        model (Model): The model that this serializer is associated with, which is the User model.
        fields (list): The fields of the User model that should be included in the serialized representation.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
