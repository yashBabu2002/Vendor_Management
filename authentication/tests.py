from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthTests(APITestCase):
    
    def setUp(self):
        self.register_url = "/api/v1/auth/register/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"
        self.user_url = "/api/v1/auth/user/"
        
        self.user_data = {
            "email": "testuser@example.com",
            "name": "testuser",
            "password": "testpassword123",
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_register_user(self):
        response = self.client.post(self.register_url, {
            "email": "newuser@example.com",
            "name": "newuser",
            "password": "newpassword123",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertEqual(response.data["name"], "newuser")

        # Ensure the user was actually created in the database
        user_exists = User.objects.filter(email="newuser@example.com", name="newuser").exists()
        self.assertTrue(user_exists)
    
    def test_login_user(self):
        response = self.client.post(self.login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_get_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.user.email)
    
    def test_get_user_unauthenticated(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_logout_user(self):
      # Generate JWT tokens
      refresh = RefreshToken.for_user(self.user)
      access_token = str(refresh.access_token)

      # Attach access token to request headers
      self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

      response = self.client.post(self.logout_url, {"refresh": str(refresh)})
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data["message"], "Logged out successfully")

      # Reset authentication for subsequent tests
      self.client.credentials()
