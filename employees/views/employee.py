from ..models.employee import Employee
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from ..serializers import MyTokenObtainPairSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import time
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import permissions
from django.contrib.auth.models import Group

class EmployeeRule(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        res = super().has_object_permission(request, view, obj)
        if request.user.groups.filter(name="employee_admin").exists() and res:
            return True
        else: False



class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, EmployeeRule]


    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name="employee_admin").exists():
            queryset = Employee.objects.all()
            if request.query_params.get('department'):
                queryset = queryset.filter(department__id__in=request.query_params.get('department').split(','))
        else:
            queryset = Employee.objects.filter(profile__user=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        results = serializer.data

        return Response({"results":results})


    
    def get_queryset(self):
        name_param = self.request.query_params.get('name')
        employee = Employee.objects.filter(active=True)
        if name_param:
            employee = employee.filter(Q(first_name__icontains=name_param) | Q(last_name__icontains=name_param),)
            # employee = Employee.objects.annotate(
            #     name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
            # ).filter(name__icontains=name_param)
        return employee
    

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response
    
    @action(detail=False, methods=['get'], url_path="stored_employee")
    def get_stored_employee(self, request, *args, **kwargs):
        queryset = Employee.objects.filter(active=False)
        name_param = self.request.query_params.get('name')
        if name_param:
            queryset = queryset.filter(Q(first_name__icontains=name_param) | Q(last_name__icontains=name_param),)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"results": serializer.data})
    
    @action(detail=False, methods=['get'], url_path="employee_number")
    def get_employee_number(self, request, *args, **kwargs):
        count = len(self.get_queryset())
        return Response({"active_employee_count": count})

    @action(detail=False, methods=['get'], url_path="employee_all")
    def get_employee_all(self, request, *args, **kwargs):
        count = len(self.get_queryset())
        return Response({"active_employee_count": count})