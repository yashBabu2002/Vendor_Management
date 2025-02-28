from rest_framework import serializers
from .models import Shop
from django.contrib.gis.geos import Point


class ShopSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True, required=True)  
    long = serializers.FloatField(write_only=True, required=True)  

    class Meta:
        model = Shop
        fields = ["id", "name", "owner", "type_of_business", "lat","long","location"]
        read_only_fields = ["owner","location"]  
    def create(self, validated_data):
        lat = validated_data.pop("lat")
        long = validated_data.pop("long")
        if not lat or not long:
            raise serializers.ValidationError({"location": "Latitude and longitude are required"})
        validated_data["location"] = Point(long, lat) 
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        lat = validated_data.pop("lat", None)
        long = validated_data.pop("long", None)
        if lat is not None and long is not None:
            instance.location = Point(long, lat)  
        return super().update(instance, validated_data)
