from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import RegisterSerializer, UserProfileSerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Authentication'],
        summary="Register a new user",
        description="Create a new user account with email, username, and password. Returns user data and JWT tokens.",
        request=RegisterSerializer,
        responses={
            201: OpenApiExample(
                name="Success Response",
                value={
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "user",
                        "first_name": "John",
                        "last_name": "Doe"
                    },
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            ),
            400: "Bad Request - Invalid data"
        },
        examples=[
            OpenApiExample(
                name="Registration Example",
                value={
                    "email": "user@example.com",
                    "username": "user",
                    "first_name": "John",
                    "last_name": "Doe",
                    "password": "securepassword123"
                }
            )
        ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "user": serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Authentication'],
        summary="User login",
        description="Authenticate user with email and password. Returns JWT access and refresh tokens.",
        request={
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email", "example": "user@example.com"},
                "password": {"type": "string", "example": "securepassword123"}
            },
            "required": ["email", "password"]
        },
        responses={
            200: OpenApiExample(
                name="Success Response",
                value={
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            ),
            401: "Unauthorized - Invalid credentials"
        }
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['User Profile'],
        summary="Get user profile",
        description="Retrieve the current user's profile information.",
        responses={
            200: UserProfileSerializer,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update user profile",
        description="Update the current user's profile information. Note: email and role cannot be changed.",
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update user profile",
        description="Partially update the current user's profile information. Note: email and role cannot be changed.",
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


