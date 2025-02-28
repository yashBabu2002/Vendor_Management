from django.contrib.auth import get_user_model
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Shop

User = get_user_model()

class ShopTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword123",name="testuser``")
        self.client.force_authenticate(user=self.user)

        self.shop1 = Shop.objects.create(
            name="Shop 1",
            owner=self.user,
            type_of_business="Grocery",
            location=Point(77.5946, 12.9716, srid=4326),
        )
        self.shop2 = Shop.objects.create(
            name="Shop 2",
            owner=self.user,
            type_of_business="Clothing",
            location=Point(77.6046, 12.9816, srid=4326),
        )
        self.search_url = "/api/v1/shops/search/"
        self.shop_list_url = "/api/v1/shops/"

    def test_search_shops_within_radius(self):
        response = self.client.get(self.search_url, {"lat": 12.9716, "lon": 77.5946, "radius": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Shop 1")

    def test_search_shops_without_coordinates(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_create_shop(self):
        response = self.client.post(self.shop_list_url, {
            "name": "New Shop",
            "type_of_business": "retail",
            "lat": 12.965,
            "long": 77.580,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Shop")
        self.assertEqual(response.data["owner"], self.user.id)

    def test_update_shop_location(self):
        update_url = f"{self.shop_list_url}{self.shop1.id}/"
        response = self.client.patch(update_url, {"lat": 12.990, "long": 77.600})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shop1.refresh_from_db()
        self.assertEqual(self.shop1.location.x, 77.600)
        self.assertEqual(self.shop1.location.y, 12.990)

    def test_delete_shop(self):
        delete_url = f"{self.shop_list_url}{self.shop1.id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shop.objects.filter(id=self.shop1.id).exists())
