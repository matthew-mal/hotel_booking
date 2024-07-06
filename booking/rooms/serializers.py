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
    class Meta:
        model = Booking
        fields = ("user", "room", "start_date", "end_date", "cost", "canceled")

    def validate(self, data):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        if user != data["user"]:
            raise serializers.ValidationError("You can't book for somebody else")

        room = data["room"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        if start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date")

        conflicting_bookings = Booking.objects.filter(
            room=room, start_date__lt=end_date, end_date__gt=start_date
        )

        if conflicting_bookings.exists():
            raise serializers.ValidationError(
                "Room is already booked for the specified dates"
            )

        return data
