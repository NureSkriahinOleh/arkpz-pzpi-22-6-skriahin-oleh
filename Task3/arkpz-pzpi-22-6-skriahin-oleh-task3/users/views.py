from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDetailSerializer, CustomUserCreateSerializer

User = get_user_model()

class UserRegistrationView(APIView):
    """
    Handles user registration.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        responses={
            201: openapi.Response(
                "User successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, example="access_token"),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="refresh_token"),
                    },
                ),
            ),
            400: "Validation error"
        },
    )


    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "user": serializer.data,  
                "access": str(access),    
                "refresh": str(refresh),  
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Provides the current authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserManagementViewSet(ViewSet):
    """
    Handles user management actions (list, retrieve, deactivate).
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.status = False
            user.save()
            return Response({"detail": "User deactivated successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UserDetailSerializer,
        responses={
            200: UserDetailSerializer,
            400: "Validation error",
            404: "User not found."
        }
    )
    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserDetailSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class TokenBlacklistView(APIView):
    """
    Handles JWT token blacklisting (logout).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid or missing token."}, status=status.HTTP_400_BAD_REQUEST)
