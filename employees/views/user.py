
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.utils.decorators import method_decorator
from ..serializers import MyTokenObtainPairSerializer, UserRegisterSerializer
from rest_framework.views import APIView
from ..models.user import EmployeeUser


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='dispatch')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MyTokenObtainPairSerializer

    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        res = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        profile = getattr(request.user, 'profile', None)
        res.data['username'] = request.user.profile.employee.name if profile else request.user.username
        return res

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
