from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import RoomFilter
from .models import Room, Booking, MyUser
from .permissons import IsOwnerOrStaff
from .serializers import RoomSerializer, BookingSerializer, MyUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MyUser.objects.all()
        return MyUser.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RoomFilter
    filterset_fields = ['price_per_day', 'capacity']
    ordering_fields = ['price_per_day', 'capacity']

    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user.id)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        room_id = request.data.get('room')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if not room.is_available:
            return Response({'error': 'Room is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(user=request.user, room=room, start_date=start_date,
                                         end_date=end_date)

        room.is_available = False
        room.save()

        serializer = self.get_serializer(booking)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel_booking(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        if booking.canceled:
            return Response({'error': 'Booking already canceled'}, status=status.HTTP_400_BAD_REQUEST)

        booking.canceled = True

        booking.save()

        booking.room.is_available = True
        booking.room.save()

        serializer = self.get_serializer(booking)

        return Response(f'Booking {serializer.data} was successfully canceled', status=status.HTTP_200_OK)
