from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth.models import update_last_login
from .utils import *
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if email is valid
    if not email or not is_valid_email(email):
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username is already in use'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)

    if not password:
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)

    confirmation_token = generate_confirmation_token()

    user, created = CustomUser.objects.get_or_create(
        email=email,
        defaults={'confirmation_token': confirmation_token, 'is_verified': False, 'username': username, 'password': hashed_password}
    )

    if not created and user.is_verified:
        return Response({'error': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)

    user.confirmation_token = confirmation_token
    user.save()

    email_sent = send_confirmation_email(email, confirmation_token)

    if email_sent:
        return Response({'message': 'Email sent successfully. Check your email for confirmation.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to send confirmation email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    user = get_object_or_404(CustomUser, confirmation_token=token, is_verified=False)

    user.is_verified = True
    # user.confirmation_token = None  # token clear after verification
    user.save()

    return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    print(f"Received login request for username: {username}, password: {password}")

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        print(f"User with username {username} does not exist")
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        print(f"Authentication failed for username: {username}")
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    update_last_login(None, user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({'token': access_token}, status=status.HTTP_200_OK)
