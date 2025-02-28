from django.contrib.gis.db import models  
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

User = get_user_model()

class Shop(models.Model):
    BUSINESS_TYPES = [
        ("retail", "Retail"),
        ("restaurant", "Restaurant"),
        ("service", "Service"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    type_of_business = models.CharField(max_length=50, choices=BUSINESS_TYPES, default="retail")
    location = models.PointField(geography=True)  

    def save(self, *args, **kwargs):
        if not isinstance(self.location, Point):
            raise ValueError("Location must be a Point object (lat, long)")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_type_of_business_display()})"
