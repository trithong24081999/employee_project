from ..serializers import DepartmentSerializer, Department
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


class DepartmentModelSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    
    def list(self, request):
        return super().list(request)

    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)

    def create(self, request):
        return super().create(request)

    def update(self, request, pk=None):
        return super().update(request, pk)
