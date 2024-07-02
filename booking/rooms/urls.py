from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet, UserViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
