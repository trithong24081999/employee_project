
from django.urls import path, include
from .views.login import Login, Refresh
from .views.react_view import FrontendAppView
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views.user import UserViewSet, UserCreateAPIView

routers = DefaultRouter()
# routers.register(r'user', UserViewSet, basename="User")
urlpatterns = [
    path('api/token/', Login.as_view(), name="login"),
    path('api/refresh/', Refresh.as_view(), name="refresh_token"),
    path('api/', include(routers.urls)),  # Thêm router URLs ở đây
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),  # API tạo user không CSRF

    re_path(r'^.*$', FrontendAppView.as_view(), name='frontend'),

]
