from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 🎬 MOVIE
class Movie(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, default="Unknown")
    language = models.CharField(max_length=100, default="Unknown")
    trailer_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# 🎭 THEATER
class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2, default=200.00)

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'


# 💺 SEAT
class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    reserved_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['theater', 'seat_number']  # 🔥 prevents duplicate seats

    def is_reserved(self):
        return self.reserved_until and self.reserved_until > timezone.now()

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'


# 🎟 BOOKING
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number}'


# ============================================================
# 🔥 AUTO CREATE 50 SEATS PER THEATER (IMPORTANT FEATURE)
# ============================================================

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Theater)
def create_seats(sender, instance, created, **kwargs):
    if created:
        seats = []
        for i in range(1, 51):  # 50 seats
            seats.append(
                Seat(
                    theater=instance,
                    seat_number=f"S{i}"
                )
            )
        Seat.objects.bulk_create(seats)