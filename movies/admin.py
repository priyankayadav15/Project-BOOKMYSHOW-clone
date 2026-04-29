from django.contrib import admin
from .models import Movie, Theater, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'language', 'rating']
    search_fields = ['name', 'genre']
    list_filter = ['genre', 'language']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time', 'ticket_price']
    list_filter = ['movie']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']
    list_filter = ['is_booked']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'theater', 'seat', 'booked_at']