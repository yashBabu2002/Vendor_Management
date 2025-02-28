from django.conf import settings
from django.contrib.auth import get_user_model, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data

        access_token = response_data["access"]
        refresh_token = response_data["refresh"]

        response = Response({"user": response_data["user"], "access": access_token, "refresh": refresh_token}, status=status.HTTP_200_OK)

        # If request is secure (HTTPS), store tokens in HttpOnly cookies
        if request.is_secure():
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax")
        else:
            # If request is not secure (HTTP), send tokens in response body
            response.data["access"] = access_token
            response.data["refresh"] = refresh_token

        return response

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

            if request.is_secure():
                response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
                response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
            
            logout(request)
            return response
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"user": UserSerializer(request.user).data}, status=status.HTTP_200_OK)
