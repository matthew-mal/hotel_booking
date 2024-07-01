# from rest_framework import serializers
# from .models import Room, Booking
#
#
# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ['id', 'name', 'price_per_day', 'capacity', 'is_available']
#
#
# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['user', 'room', 'start_date', 'end_date', 'cost']
