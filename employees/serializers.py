from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        res = super(MyTokenObtainPairSerializer, self).validate(attrs)
        res['token_expires'] = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds()
        return res

from rest_framework import serializers
from .models.user import EmployeeUser
from django.contrib.auth.models import User
from .models.employee import Employee
from .models.department import Department

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user
    

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id','name', 'age', 'phone', 'birthday', 'email', 'joining_date', 'active', 'department']

        
class DepartmentSerializer(serializers.ModelSerializer):
    child_ids = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ['id', 'name', 'child_ids']

    def get_child_ids(self, obj):
        child = obj.child_ids.all()
        return DepartmentSerializer(child, many=True).data