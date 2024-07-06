from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Booking, Room


class RoomFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_date", method="filter_by_date")
    end_date = filters.DateFilter(field_name="end_date", method="filter_by_date")
    room_name = filters.CharFilter(
        field_name="room_name", method="filter_by_room_number"
    )

    class Meta:
        model = Room
        fields = [
            "name",
            "room_type",
            "price_per_day",
            "capacity",
            "start_date",
            "end_date",
        ]

    def filter_by_date(self, queryset, name, value):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        room_name = self.request.query_params.get("room_name")

        if room_name and start_date and end_date:
            # Проверяем конкретную комнату
            is_available = not Booking.objects.filter(
                room_name=room_name,
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).exists()
            return (
                Room.objects.filter(id=room_name)
                if is_available
                else Room.objects.none()
            )

        if start_date and end_date:
            # Получаем комнаты, которые забронированы в указанный интервал
            booked_rooms = Booking.objects.filter(
                Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
            ).values_list("room_id", flat=True)

            # Исключаем забронированные комнаты из общего списка
            queryset = queryset.exclude(id__in=booked_rooms)

        return queryset
