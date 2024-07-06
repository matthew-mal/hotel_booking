import datetime

import pytest

from ..models import Booking, MyUser, Room


@pytest.mark.django_db
class TestBookingModels:
    def test_booking_creation(self):
        user = MyUser.objects.create(username="testuser", email="test@example.com")
        room = Room.objects.create(name=101, price_per_day=100.00, capacity=2)
        start_date = datetime.date(2024, 7, 11)
        end_date = datetime.date(2024, 7, 15)

        booking = Booking.objects.create(
            user=user, room=room, start_date=start_date, end_date=end_date
        )

        assert booking.user == user
        assert booking.room == room
        assert booking.start_date == start_date
        assert booking.end_date == end_date

    def test_booking_cancellation(self):
        user = MyUser.objects.create(username="testuser", email="test@example.com")
        room = Room.objects.create(name=101, price_per_day=100.00, capacity=2)
        start_date = datetime.date(2024, 7, 11)
        end_date = datetime.date(2024, 7, 15)

        booking = Booking.objects.create(
            user=user, room=room, start_date=start_date, end_date=end_date
        )
        booking.is_canceled = True
        booking.save()

        assert booking.is_canceled is True

    def test_booking_cost_calculation(self):
        user = MyUser.objects.create(username="testuser", email="test@example.com")
        room = Room.objects.create(name=101, price_per_day=100.00, capacity=2)
        start_date = datetime.date(2024, 7, 11)
        end_date = datetime.date(2024, 7, 15)

        booking = Booking.objects.create(
            user=user, room=room, start_date=start_date, end_date=end_date
        )

        assert booking.cost == 400.00


@pytest.mark.django_db
class TestRoomModels:

    def test_room_str_method(self):
        room = Room.objects.create(
            name=101, price_per_day=100.00, capacity=2, room_type="standard"
        )
        assert str(room) == "101 - standard"

    def test_room_capacity(self):
        room = Room.objects.create(
            name=101, price_per_day=100.00, capacity=2, room_type="standard"
        )

        assert room.capacity == 2
