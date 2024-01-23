from typing import Any
from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=50, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, upload_to="images/", blank=False)
    description = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ваш код для автоматического заполнения полей latitude и longitude на основе address
        if not self.latitude or not self.longitude:
            geolocator = Nominatim(user_agent="memory")
            location = None
            try:
                location = geolocator.geocode(self.address)
            except GeocoderTimedOut as e:
                # Обработка ошибок геокодера
                print(f"Geocoding error: {e}")
            
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.description
