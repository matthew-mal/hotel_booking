import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rooms.models import Booking, MyUser, Room


@pytest.fixture
def admin_user():
    return MyUser.objects.create_superuser(
        username="admin", email="admin@example.com", password="admin"
    )


@pytest.fixture
def authenticated_client_admin(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.mark.django_db
class TestRoomAPI:

    def test_room_list_view(self):
        client = APIClient()
        response = client.get("/api/rooms/")
        assert response.status_code == 200

    def test_room_detail_view(self):
        room = Room.objects.create(
            name=101, price_per_day=100.00, capacity=2, room_type="standard"
        )
        client = APIClient()
        response = client.get(f"/api/rooms/{room.id}/")
        assert response.status_code == 200
        assert response.data["name"] == 101

    def test_create_room_api_admin(self, authenticated_client_admin):
        data = {
            "name": 102,
            "price_per_day": "150.00",
            "capacity": 2,
            "room_type": "deluxe",
        }
        url = reverse("rooms-list")
        response = authenticated_client_admin.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Room.objects.filter(name=102).exists()

    def test_create_room_api_non_admin(self):
        MyUser.objects.create_user(
            username="user", email="user@example.com", password="password"
        )
        client = APIClient()

        data = {
            "name": 102,
            "price_per_day": "150.00",
            "capacity": 2,
            "room_type": "deluxe",
        }
        url = reverse("rooms-list")
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Room.objects.filter(name=102).exists()

    def test_update_room_api_not_authorized(self):
        room = Room.objects.create(
            name=103, price_per_day=120.00, capacity=3, room_type="standard"
        )
        client = APIClient()

        data = {
            "name": 103,
            "price_per_day": "130.00",
            "capacity": 3,
            "room_type": "standard",
        }
        url = f"/api/rooms/{room.id}/"
        response = client.put(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_room_api(self):
        room = Room.objects.create(
            name=104, price_per_day=90.00, capacity=2, room_type="deluxe"
        )
        client = APIClient()
        url = f"/api/rooms/{room.id}/"
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_room_api_by_admin(self, admin_user):
        room = Room.objects.create(
            name=104, price_per_day=90.00, capacity=2, room_type="deluxe"
        )
        client = APIClient()
        client.force_authenticate(user=admin_user)
        url = f"/api/rooms/{room.id}/"
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserApi:

    def test_create_user(self):
        client = APIClient()
        url = reverse("users-list")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert MyUser.objects.filter(username="testuser").exists()

    def test_create_user_invalid_data(self):
        client = APIClient()
        url = reverse("users-list")
        data = {"username": "testuser", "password": "testpassword"}
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_update_user_by_owner(self):
        user = MyUser.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("users-detail", args=[user.id])
        data = {"email": "updated_email@example.com"}
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert MyUser.objects.get(id=user.id).email == "updated_email@example.com"

    def test_update_user_by_staff(self):
        admin_user = MyUser.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin"
        )
        user = MyUser.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        client = APIClient()
        client.force_authenticate(user=admin_user)
        url = reverse("users-detail", args=[user.id])
        data = {"email": "updated_email_staff@example.com"}
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert MyUser.objects.get(id=user.id).email == "user1@example.com"

    def test_get_user_detail_as_authenticated_user(self):
        user1 = MyUser.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        user2 = MyUser.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )
        client = APIClient()
        client.force_authenticate(user=user1)
        url = reverse("users-detail", args=[user1.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"username": "user1", "email": "user1@example.com"}

    def test_get_user_list_as_unauthenticated_user(self):
        url = reverse("users-list")
        client = APIClient()
        response = client.get(url)

        assert response.data == []


@pytest.mark.django_db
class TestBookingApi:

    def setup_method(self, method):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.room = Room.objects.create(name="101", capacity=2, price_per_day=100)
        self.booking_data = {
            "user": self.user,
            "room": self.room,
            "start_date": "2024-07-05",
            "end_date": "2024-07-10",
            "canceled": False,
            "cost": 500,
        }
        self.client.force_authenticate(user=self.user)

    def test_create_booking(self):
        url = reverse("bookings-list")
        response = self.client.post(
            url,
            {
                "user": self.user.id,
                "room": self.room.id,
                "start_date": "2024-07-05",
                "end_date": "2024-07-10",
                "canceled": False,
                "cost": 500,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Booking.objects.filter(user=self.user).exists()

    def test_get_booking_list(self):
        Booking.objects.create(**self.booking_data)
        url = reverse("bookings-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_update_booking(self):
        booking = Booking.objects.create(**self.booking_data)
        url = reverse("bookings-detail", args=[booking.id])
        updated_data = {
            "user": self.user.id,
            "room": self.room.id,
            "start_date": "2024-07-05",
            "end_date": "2024-07-10",
            "canceled": False,
            "cost": 600,
        }
        response = self.client.patch(url, updated_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert Booking.objects.get(id=booking.id).cost == 600

    def test_delete_booking(self):
        booking = Booking.objects.create(**self.booking_data)
        url = reverse("bookings-detail", args=[booking.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Booking.objects.filter(id=booking.id).exists()

    def test_get_booking_unauthenticated(self):
        self.client.logout()
        url = reverse("bookings-list")
        response = self.client.get(url)

        assert response.data == []

    def test_partial_update_booking(self):
        booking = Booking.objects.create(**self.booking_data)
        url = reverse("bookings-detail", args=[booking.id])
        response = self.client.patch(url, {"cost": 700}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert Booking.objects.get(id=booking.id).cost == 700
