from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        res = super(MyTokenObtainPairSerializer, self).validate(attrs)
        res['token_expires'] = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds()
        return res

from rest_framework import serializers
from django.contrib.auth.models import User

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