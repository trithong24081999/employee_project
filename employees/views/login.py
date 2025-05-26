from ..serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import time


class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        response = super().post(request=request)
        # token = RefreshToken.for_user(user=user)
        time.sleep(10)
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)
        response.data['user'] = {'username': user.username, 'email': user.email}
        response.set_cookie(key="refresh_token",
                            value=response.data.get("refresh"),
                            secure=True,
                            httponly=True,
                            samesite="Lax",
                            max_age=settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME').total_seconds())
        response.data['token'] = response.data.pop('access')
        response.data.pop('refresh', None)
        return response


class Refresh(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            access_token_exp = refresh.access_token['exp']
            return Response({
                'token': access_token,
                'token_exp': access_token_exp
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
