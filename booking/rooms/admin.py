from django.contrib import admin
from .models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_day', 'capacity', 'room_type', 'is_available')
    list_filter = ('is_available', 'room_type')
    search_fields = ('name', 'room_type')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'cost')
    list_filter = ('user__username', 'room__room_type',)
    search_fields = ('user__username', 'room__room_type')
