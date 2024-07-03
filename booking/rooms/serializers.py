from rest_framework import serializers

from .models import Booking, MyUser, Room


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "price_per_day",
            "capacity",
            "room_type",
            "is_available",
        )


class BookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    room_name = serializers.IntegerField(source="room.name")

    class Meta:
        model = Booking
        fields = ("username", "room_name", "start_date", "end_date", "cost", "canceled")
