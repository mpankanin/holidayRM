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
from .serializers import VacationSerializer, UserSerializer, VacationGetSerializer


# ----- VACATION ENDPOINTS -----

# get user's vacations
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_vacation_list(request):
    """
    Get a list of vacations for the authenticated user.

    :param request: The request object.
    :return: A list of vacations for the authenticated user.
    """
    vacations = Vacation.objects.filter(user=request.user)
    get_serializer = VacationGetSerializer(vacations, many=True)
    return Response(get_serializer.data)


# send a new vacation's request
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def vacation_post(request):
    """
    Create a new vacation request for the authenticated user.

    :param request: The request object.
    :return: The created vacation object or an error message.
    """
    serializer = VacationSerializer(data=request.data)
    if serializer.is_valid():
        date_from = serializer.validated_data['date_from']
        date_to = serializer.validated_data['date_to']
        overlapping_vacations = Vacation.objects.filter(user=request.user,
                                                        date_from__lte=date_to,
                                                        date_to__gte=date_from)
        if overlapping_vacations.exists():
            return Response({"detail": "You already have vacations in the requested dates."}
                            , status=status.HTTP_400_BAD_REQUEST)
        vacation = serializer.save(user=request.user)
        get_serializer = VacationGetSerializer(vacation)
        return Response(get_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# approve a vacation's request - admin role
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def approve_vacation(request, id):
    """
    Approve a vacation request. Only accessible by staff users.

    :param request: The request object.
    :param id: The id of the vacation to approve.
    :return: The approved vacation object or an error message.
    """
    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        vacation = Vacation.objects.get(pk=id)
    except Vacation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    vacation.is_approved = True
    vacation.save()

    get_serializer = VacationGetSerializer(vacation)
    return Response(get_serializer.data)


# vacation by id - get, put - only unapproved, delete
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def vacation_detail(request, id):
    """
    Get, update, or delete a vacation by id. Only the owner of the vacation can perform these actions.

    :param request: The request object.
    :param id: The id of the vacation to get, update, or delete.
    :return: The vacation object, a success message, or an error message.
    """
    try:
        vacation = Vacation.objects.get(pk=id)
    except Vacation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if vacation.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        get_serializer = VacationGetSerializer(vacation)
        return Response(get_serializer.data)

    if request.method == 'PUT':
        if vacation.is_approved:
            return Response({"detail": "You cannot modify approved vacations."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = VacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            vacation = serializer.save()
            get_serializer = VacationGetSerializer(vacation)
            return Response(get_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vacation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# get all vacations - admin role
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_vacations(request):
    """
    Get a list of all vacations. Only accessible by staff users.

    :param request: The request object.
    :return: A list of all vacations.
    """
    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    vacations = Vacation.objects.all()
    get_serializer = VacationGetSerializer(vacations, many=True)
    return Response(get_serializer.data)


# ----- AUTHENTICATION ENDPOINTS -----

# sing up a new user
@api_view(['POST'])
def signup(request):
    """
    Register a new user.

    :param request: The request object.
    :return: The created user object or an error message.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login into system - returns valid token
@api_view(['POST'])
def login(request):
    """
    Authenticate a user and return a token.

    This view expects a POST request with 'username' and 'password' in the request data.
    If the credentials are valid, it returns a token and user data.
    If the credentials are not valid, it returns a 404 error.

    :param request: The request object.
    :return: A Response object with the token and user data if the credentials are valid, or a 404 error if they are not.
    """
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"access_token": token.key, "user": serializer.data})


# endpoint to test if token is valid
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    Test if a token is valid.

    This view expects a GET request with a valid token in the 'Authorization' header.
    If the token is valid, it returns a success message.
    If the token is not valid, it returns a 403 error.

    :param request: The request object.
    :return: A Response object with a success message if the token is valid, or a 403 error if it is not.
    """
    return Response("passed for{}".format(request.user.username))



