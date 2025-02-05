from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter(trailing_slash=False)
app='api'
urlpatterns = [
    path('usuario/',UsuarioAPIView.as_view(),name='usuario'),
    path('usuario/<int:pk>/',UsuarioEdicionAPIView.as_view(),name='usuario_detalle'),
]
