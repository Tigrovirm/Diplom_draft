from django.urls import path
from .views import DeleteMemory
from . import views


app_name = "memory"

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('remembering/<str:pk>/', views.viewRemembering, name='remembering'),
    path('remembering/<str:pk>/delete', DeleteMemory.as_view(), name="delete"),
    path('add/', views.addMemory, name='add'),
]