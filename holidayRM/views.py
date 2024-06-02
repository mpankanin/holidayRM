from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Vacation
from django.contrib.auth.models import User
from .serializers import VacationSerializer, UserSerializer


@api_view(['GET'])
def vacation_list(request):
    vacations = Vacation.objects.all()
    serializer = VacationSerializer(vacations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def vacation_post(request):
    serializer = VacationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def vacation_detail(request, id):
    try:
        vacation = Vacation.objects.get(pk=id)
    except Vacation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VacationSerializer(vacation)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = VacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vacation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"access_token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for{}".format(request.user.username))
