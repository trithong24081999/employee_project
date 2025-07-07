
from django.urls import path, include
from .views.login import Login, Refresh
from .views.react_view import FrontendAppView
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views.user import UserViewSet, UserCreateAPIView
from .views.employee import EmployeeViewSet
from .views.department import DepartmentModelSet

routers = DefaultRouter()
routers.register(r'user', UserViewSet, basename="User")
routers.register(r'department', DepartmentModelSet, basename="Department")

routers.register(r'employee', EmployeeViewSet, basename="Employee")
urlpatterns = [
    path('api/token/', Login.as_view(), name="login"),
    path('api/refresh/', Refresh.as_view(), name="refresh_token"),
    path('api/user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('api/', include(routers.urls)),

    re_path(r'^.*$', FrontendAppView.as_view(), name='frontend'),

]