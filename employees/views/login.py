from ..serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, Token, OutstandingToken, BlacklistedToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import time
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        token = OutstandingToken.objects.filter(user=user)
        if token:
            a = [BlacklistedToken.objects.get_or_create(token=outstanding_token) for outstanding_token in token]
        response = super().post(request=request)
        time.sleep(1)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)
        response.data.update({'username': user.username, 'email': user.email, 'id': user.id})

        response.set_cookie(key="refresh_token",
                            value=response.data.get("refresh"),
                            httponly=True,         # Không cho JS truy cập
                            secure=False,          # Vì đang chạy local không có HTTPS
                            samesite="Lax",
                            path= '/',
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
