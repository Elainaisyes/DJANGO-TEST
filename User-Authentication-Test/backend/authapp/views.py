from django.shortcuts import render

# Django’s built-in user system.
"""What User can do:
    store username/password
    hash passwords automatically
    check passwords securely
    query users from databas
 """
from django.contrib.auth.models import User

#Turns a normal function into an API endpoint
#Example: @api_view(['POST']) - Only allows POST requests
from rest_framework.decorators import api_view

#A special response for APIs.- Automatically converst to JSON
from rest_framework.response import Response

#A helper for HTTP status codes. (Ex: 401, 403, etc) (status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status

# A class that creates JWT tokens for a user.
"""What it can do:
    generate access tokens
    generate refresh tokens
    handle expiration automatically
"""
from rest_framework_simplejwt.tokens import RefreshToken

# Checks if username + password are correct.
"""Behind the scenes:
    finds user in database
    hashes input password
    compares it to stored hashed password
"""
from django.contrib.auth import authenticate

# Lets us attach security rules to a view
from rest_framework.decorators import permission_classes

# A built in rule checking if users are logged in. 
"""What it checks:
    Does request have a valid token?
    Is token not expired?
    Does token belong to a real user?
"""
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(["POST"])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password') 

    if not username or not password:
        return Response({'error': 'Missing Fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username = username,
        password = password
    )

    return Response ({'message': 'User created'})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    """What authenticate does here
        1. Look for user with this username
        2. If not found → return None
        3. If found → hash input password
        4. Compare with stored password
        5. If match → return user object
        6. If not → return None
    """
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    #Inside this token:
    """{
        "user_id": 1,
        "exp": future_time,
        "type": "refresh"
    }"""
    refresh = RefreshToken.for_user(user)

    response = Response({
        'access': str(refresh.access_token)
    })

    response.set_cookie(
        key="access_token",
        value=str(access),
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=300,  # 5 min
    )

    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False, # Set to True in production
        samesite="Lax"
    )

    return response

@api_view(['POST'])
def refresh(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)

        return Response({'access': access_token})

    except Exception:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

# Protected route!
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    return Response({
        'message': f'Welcome {request.user.username}'
    })