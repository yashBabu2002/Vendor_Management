# Vendor Shop API Documentation

## Overview

This API provides authentication and shop management features, including user registration, login, shop creation, and search functionality using Django Rest Framework and Django GIS.

## Tech Stack

* Django & Django Rest Framework (DRF)
* Docker
* JWT Authentication

## Installation & Setup

### Using Docker

1. **Build the Docker container:**
   ```sh
   docker build -t vendor_shop .
   ```
2. **Run the container:**
   ```sh
   docker run -p 8000:8000 vendor_shop
   ```
3. **Run Migrations (Inside Docker Container):**
   ```sh
   docker exec -it <container_id> sh -c "python manage.py migrate"
   ```

## API Endpoints

### Authentication

#### Register a User

* **Endpoint:** `POST /api/v1/auth/register/`
* **Payload:**
  ```json
  {
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword",
    "user_type": "vendor"
  }
  ```
* **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "user_type": "vendor"
  }
  ```

#### Login

* **Endpoint:** `POST /api/v1/auth/login/`
* **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
* **Response:**
  ```json
  {
    "user": { "id": 1, "email": "user@example.com", "name": "John Doe" },
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
  ```

#### Logout

* **Endpoint:** `POST /api/v1/auth/logout/`
* **Payload:**
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```
* **Response:**
  ```json
  { "message": "Logged out successfully" }
  ```

#### Get Authenticated User Info

* **Endpoint:** `GET /api/v1/auth/user/`
* **Headers:** `Authorization: Bearer <jwt_access_token>`
* **Response:**
  ```json
  {
    "user": { "id": 1, "email": "user@example.com", "name": "John Doe" }
  }
  ```

### Shop Management

#### Create a Shop

* **Endpoint:** `POST /api/v1/shops/`
* **Headers:** `Authorization: Bearer <jwt_access_token>`
* **Payload:**
  ```json
  {
    "name": "John's Electronics",
    "type_of_business": "Electronics",
    "lat": 12.9716,
    "long": 77.5946
  }
  ```
* **Response:**
  ```json
  {
    "id": 1,
    "name": "John's Electronics",
    "owner": 1,
    "type_of_business": "Electronics",
    "location": "SRID=4326;POINT (77.5946 12.9716)"
  }
  ```

#### Get All Shops

* **Endpoint:** `GET /api/v1/shops/`
* **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "John's Electronics",
      "owner": 1,
      "type_of_business": "Electronics",
      "location": "SRID=4326;POINT (77.5946 12.9716)"
    }
  ]
  ```

#### Update a Shop

* **Endpoint:** `PUT /api/v1/shops/1/`
* **Headers:** `Authorization: Bearer <jwt_access_token>`
* **Payload:**
  ```json
  {
    "name": "John's Updated Electronics",
    "lat": 12.9756,
    "long": 77.5999
  }
  ```
* **Response:**
  ```json
  {
    "id": 1,
    "name": "John's Updated Electronics",
    "owner": 1,
    "type_of_business": "Electronics",
    "location": "SRID=4326;POINT (77.5999 12.9756)"
  }
  ```

#### Delete a Shop

* **Endpoint:** `DELETE /api/v1/shops/1/`
* **Headers:** `Authorization: Bearer <jwt_access_token>`
* **Response:**
  ```json
  { "message": "Shop deleted successfully" }
  ```

### Shop Search

#### Search Shops by Location

* **Endpoint:** `GET /api/v1/shops/search/?lat=12.9716&lon=77.5946&radius=10`
* **Response:**
  ```json
  [
    { "name": "John's Electronics", "distance_km": 1.5 }
  ]
  ```

## Environment Variables

Create a `.env` file and set the following:

```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
```

## Running Tests

```sh
python manage.py test
```
