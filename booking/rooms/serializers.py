from rest_framework import serializers
from .models import Room, Booking, MyUser


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'price_per_day', 'capacity', 'room_type', 'is_available')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('user', 'room', 'start_date', 'end_date', 'cost')
