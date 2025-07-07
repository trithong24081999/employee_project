from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):


    def authenticate(self, request):
        res = super().authenticate(request)
        refresh = request.COOKIES.get('refresh_token')
        if  refresh and BlacklistedToken.objects.filter(token__token=refresh).exists():
            raise AuthenticationFailed("Token has been blacklist")
        return res