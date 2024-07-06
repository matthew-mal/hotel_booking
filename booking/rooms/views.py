from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .filters import RoomFilter
from .models import Booking, MyUser, Room
from .permissons import AdminOnlyPermission, IsOwner, IsOwnerOrStaff
from .serializers import BookingSerializer, MyUserSerializer, RoomSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MyUser.objects.all()
        return MyUser.objects.filter(id=user.id)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RoomFilter
    filterset_fields = ["price_per_day", "capacity"]
    ordering_fields = ["price_per_day", "capacity"]

    permission_classes = [AdminOnlyPermission]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related("user", "room")
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Booking.objects.all().select_related("user", "room")
        return Booking.objects.filter(user=user.id).select_related("user", "room")

    # Про метод cancel
    # Я видимо не совсем правильно понял пункт про отмену из тз, подумал, что при отмене пользователем,
    # букинг все равно остается в бд, а удаление записи уже остается за админом/стафом
