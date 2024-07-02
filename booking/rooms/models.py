from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Room(models.Model):
    STANDARD = 'standard'
    DELUXE = 'deluxe'
    SUITE = 'suite'

    ROOM_TYPE_CHOICES = [
        (STANDARD, 'Standard'),
        (DELUXE, 'Deluxe'),
        (SUITE, 'Suite'),
    ]

    name = models.PositiveSmallIntegerField(verbose_name='Номер')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за сутки')
    capacity = models.IntegerField(verbose_name='Количество мест')
    is_available = models.BooleanField(default=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default=STANDARD)

    def __str__(self):
        return f'{self.name} - {self.room_type}'


class Booking(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.room.name} - {self.user.username} ({self.start_date} to {self.end_date})'

    def calculate_cost(self, start_date, end_date):
        duration = end_date - start_date
        days = duration.days
        cost_per_day = self.room.price_per_day
        cost = days * cost_per_day
        return cost
