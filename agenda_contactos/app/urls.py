from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('afiliado/gestion/', views.Usuario, name='afiliado'),
]