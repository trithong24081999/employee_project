from django.urls import path
from employees.e_feature.redis.redis_consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
