from rest_framework import serializers
from .models import Vacation
from django.contrib.auth.models import User


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ['id', 'date_from', 'date_to']


class VacationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ['id', 'date_from', 'date_to', 'user', 'is_approved']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
