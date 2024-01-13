from django.urls import path, include
from .views import DeleteMemory, UpdateMemory
from . import views
from django.urls import path, re_path, include


app_name = "memory"

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name="registration"),
    path('gallery/', views.gallery, name='gallery'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('remembering/<str:pk>/', views.viewRemembering, name='remembering'),
    path('remembering/<str:pk>/update', UpdateMemory.as_view(), name='update'),
    path('remembering/<str:pk>/delete', DeleteMemory.as_view(), name="delete"),
    path('add/', views.addMemory, name='add'),
]