from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D  
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from .models import Shop
from .serializers import ShopSerializer
from .permissions import IsOwnerOrAdmin

class ShopSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        radius = request.query_params.get("radius", 5) 

        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required"}, status=400)

        user_location = Point(float(lon), float(lat), srid=4326)

        nearby_shops = Shop.objects.annotate(distance=Distance("location", user_location)) \
                                   .filter(distance__lte=D(km=radius)) \
                                   .order_by("distance")

        return Response([
            {"name": shop.name, "type_of_business": shop.type_of_business,"distance_km": round(shop.distance.km, 2)}
            for shop in nearby_shops
        ])



class ShopViewSet(viewsets.ModelViewSet):
    
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  

    
