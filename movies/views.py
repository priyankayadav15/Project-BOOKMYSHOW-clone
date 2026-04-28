import json
from datetime import timedelta

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count, Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import Movie, Theater, Seat, Booking

stripe.api_key = settings.STRIPE_SECRET_KEY


# 🎬 MOVIE LIST
def movie_list(request):
    movies = Movie.objects.all()

    genre = request.GET.get('genre')
    language = request.GET.get('language')
    search_query = request.GET.get('search')

    if genre and genre != "All":
        movies = movies.filter(genre__iexact=genre)

    if language and language != "All":
        movies = movies.filter(language__iexact=language)

    if search_query:
        movies = movies.filter(name__icontains=search_query)

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'selected_genre': genre,
        'selected_language': language,
        'search_query': search_query,
    })


# 🎭 THEATER LIST
def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)

    return render(request, 'movies/theater_list.html', {
        'movie': movie,
        'theaters': theaters
    })


# 💺 BOOK SEATS
@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)

    # AUTO RELEASE
    Seat.objects.filter(
        theater=theater,
        reserved_until__lt=timezone.now(),
        is_booked=False
    ).update(reserved_until=None)

    seats = Seat.objects.filter(theater=theater)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theater,
                'seats': seats,
                'error': "No seat selected"
            })

        seat_numbers = []

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)

            if seat.is_booked or seat.is_reserved():
                return render(request, "movies/seat_selection.html", {
                    'theater': theater,
                    'seats': seats,
                    'error': f"Seat {seat.seat_number} already taken."
                })

            seat.reserved_until = timezone.now() + timedelta(minutes=5)
            seat.save()

            seat_numbers.append(seat.seat_number)

        total_price = theater.ticket_price * len(seat_numbers)

        request.session['seat_numbers'] = ", ".join(seat_numbers)
        request.session['total_price'] = float(total_price)

        return redirect('payment_page', booking_id=theater.id)

    return render(request, 'movies/seat_selection.html', {
        'theater': theater,
        'seats': seats
    })


# 💳 PAYMENT PAGE
@login_required(login_url='/login/')
def payment_page(request, booking_id):
    theater = get_object_or_404(Theater, id=booking_id)
    total_price = request.session.get('total_price')

    if not total_price:
        return redirect('movie_list')

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f"{theater.movie.name} - {theater.name}",
                    },
                    'unit_amount': int(float(total_price) * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('booking_success', args=[booking_id])
            ),
            cancel_url=request.build_absolute_uri(
                reverse('payment_failed', args=[booking_id])
            ),
        )
        stripe_session_id = session.id
    except Exception:
        stripe_session_id = None  # fallback

    return render(request, "movies/payment_page.html", {
        "movie_name": theater.movie.name,
        "theater_name": theater.name,
        "seat_numbers": request.session.get('seat_numbers'),
        "ticket_price": theater.ticket_price,
        "total_price": total_price,
        "booking_id": booking_id,
        "STRIPE_SESSION_ID": stripe_session_id,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    })


# ✅ SUCCESS
@login_required(login_url='/login/')
def booking_success(request, booking_id):
    theater = get_object_or_404(Theater, id=booking_id)

    seat_numbers = request.session.get('seat_numbers', "").split(", ")
    booking_list = []

    for seat_number in seat_numbers:
        seat = Seat.objects.get(seat_number=seat_number, theater=theater)

        if seat.reserved_until and seat.reserved_until > timezone.now() and not seat.is_booked:
            booking = Booking.objects.create(
                user=request.user,
                seat=seat,
                movie=theater.movie,
                theater=theater
            )

            seat.is_booked = True
            seat.reserved_until = None
            seat.save()

            booking_list.append(booking)

    return render(request, "movies/booking_success.html", {
        "booking_list": booking_list,
        "seat_numbers": ", ".join(seat_numbers),
        "total_price": request.session.get('total_price'),
    })


# ❌ FIXED (THIS WAS YOUR ERROR)
@login_required(login_url='/login/')
def payment_failed(request, booking_id):
    theater = get_object_or_404(Theater, id=booking_id)

    return render(request, "movies/payment_failed.html", {
        "movie_name": theater.movie.name,
        "theater_name": theater.name,
        "seat_numbers": request.session.get('seat_numbers', ""),
        "total_price": request.session.get('total_price'),
    })


# 📊 REAL ANALYTICS DASHBOARD
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    total_movies = Movie.objects.count()

    total_revenue = Booking.objects.aggregate(
        revenue=Sum(F('theater__ticket_price'))
    )['revenue'] or 0

    # 📈 BOOKINGS LAST 7 DAYS
    last_7_days = []
    bookings_per_day = []
    revenue_per_day = []

    for i in range(7):
        day = timezone.now().date() - timedelta(days=i)

        bookings = Booking.objects.filter(booked_at__date=day)
        count = bookings.count()

        revenue = bookings.aggregate(
            total=Sum(F('theater__ticket_price'))
        )['total'] or 0

        last_7_days.append(day.strftime("%d %b"))
        bookings_per_day.append(count)
        revenue_per_day.append(float(revenue))

    last_7_days.reverse()
    bookings_per_day.reverse()
    revenue_per_day.reverse()

    # 🔥 TOP MOVIES
    popular_movies = Movie.objects.annotate(
        total_bookings=Count('booking')
    ).order_by('-total_bookings')[:5]

    movie_labels = [m.name for m in popular_movies]
    movie_data = [m.total_bookings for m in popular_movies]

    # 🔥 TOP THEATERS
    top_theaters = Theater.objects.annotate(
        total_bookings=Count('booking')
    ).order_by('-total_bookings')[:5]

    theater_labels = [t.name for t in top_theaters]
    theater_data = [t.total_bookings for t in top_theaters]

    # 🆕 RECENT BOOKINGS
    recent_bookings = Booking.objects.select_related(
        'user', 'movie', 'theater', 'seat'
    ).order_by('-booked_at')[:5]

    context = {
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_movies": total_movies,
        "total_revenue": total_revenue,

        # 📊 Charts
        "booking_labels": mark_safe(json.dumps(last_7_days)),
        "booking_data": mark_safe(json.dumps(bookings_per_day)),
        "revenue_data": mark_safe(json.dumps(revenue_per_day)),

        "movie_labels": mark_safe(json.dumps(movie_labels)),
        "movie_data": mark_safe(json.dumps(movie_data)),

        "theater_labels": mark_safe(json.dumps(theater_labels)),
        "theater_data": mark_safe(json.dumps(theater_data)),

        # 📋 Table
        "recent_bookings": recent_bookings,
    }

    return render(request, "movies/admin_dashboard.html", context)