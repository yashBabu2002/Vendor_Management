from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, ShopSearchView

router = DefaultRouter()
router.register(r"", ShopViewSet, basename="shop")

urlpatterns = [
    path("search/", ShopSearchView.as_view(), name="shop_search"),
    path("", include(router.urls)),
]
