from ..serializers import DepartmentSerializer, Department
from ..models.employee import Employee
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
        if request.user.groups.filter(name='employee_admin').exists():
            return super().list(request)
        else:
            data = {}
            profile = getattr(request.user, 'profile', None)
            # employee = request.user.profile.employee
            if profile:
                department = profile.employee.department
                serializer = self.get_serializer(department)
        return Response({'results': [serializer.data]})

    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)

    def create(self, request):
        return super().create(request)

    def update(self, request, pk=None):
        return super().update(request, pk)
