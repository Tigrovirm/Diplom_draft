from django.urls import path, include
from .views import DeleteMemory
from . import views


app_name = "memory"

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name="registration"),
    path('gallery/', views.gallery, name='gallery'),
    path('remembering/<str:pk>/', views.viewRemembering, name='remembering'),
    path('remembering/<str:pk>/delete', DeleteMemory.as_view(), name="delete"),
    path('add/', views.addMemory, name='add'),
]