import json
from datetime import datetime, timedelta
from itertools import groupby

from django.db.models import DateField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import View

from .models import (Cinema, CinemaCity, CinemaHall, Gallery, GalleryImage,
                     MovieCard, MovieSes, NewsEvents, Reservation)


class MovieSessionsAjaxView(View):
    template_name = 'cinema/session_partial.html'

    def get(self, request, *args, **kwargs):
        movie_id = request.GET.get('movie_id')
        city_id = request.GET.get('city_id')
        movie_type = request.GET.get('movie_type')

        now = timezone.now()
        movie_ses_queryset = MovieSes.objects.filter(time__gte=now.date(), movie_id=movie_id)

        if city_id != "all":
            cinemas_in_city = Cinema.objects.filter(city_id=city_id)
            movie_ses_queryset = movie_ses_queryset.filter(cinema_hall__cinema__in=cinemas_in_city)

        if movie_type != "all":
            movie_ses_queryset = movie_ses_queryset.filter(type=movie_type)

        grouped_sessions = {}
        for session in movie_ses_queryset:
            date_str = session.time.date()
            if date_str not in grouped_sessions:
                grouped_sessions[date_str] = []
            grouped_sessions[date_str].append({
                'session_id': session.id,
                'movie_id': movie_id,
                'time': session.time.strftime("%H:%M"),
                'type': session.type,
                'cinema_hall_number': session.cinema_hall.number,
            })

        return render(request, self.template_name, {'grouped_sessions': grouped_sessions})


def index(request):
    query = request.GET.get('q')
    movies_now = MovieCard.objects.filter(status=True)
    movies_soon = MovieCard.objects.filter(status=False)
    galley = GalleryImage.objects.filter(gallery__title='На главной вверх')

    if query:
        movies_now = movies_now.filter(title__icontains=query)
        movies_soon = movies_soon.filter(title__icontains=query)

    context = {
        'movies_now': movies_now,
        'movies_soon': movies_soon,
        'gallery_images': galley,
        'query': query
    }
    return render(request, 'cinema/index.html', context)


def about_cinema(request):
    return render(request, 'cinema/about_cinema.html')


def afisha(request):
    movies = MovieCard.objects.filter(status=True)

    context = {
        'movies': movies,
    }
    return render(request, 'cinema/afisha.html', context)


def bar_page(request):
    return render(request, 'cinema/bar.html')


def cinema_card(request, cinema_id):
    cinema = Cinema.objects.get(id=cinema_id)
    halls = CinemaHall.objects.filter(cinema_id=cinema_id)
    gallery = get_object_or_404(Gallery, cinema__id=cinema_id)
    gallery_images = gallery.galleryimage_set.all()
    now = timezone.now()
    end_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    sessions_today = MovieSes.objects.filter(time__gte=now, time__lt=end_of_today, cinema_hall__cinema__id=cinema_id)

    context = {
        'cinema': cinema,
        'halls': halls,
        'halls_count': halls.count(),
        'sessions_today': sessions_today,
        'gallery_images': gallery_images,
    }
    return render(request, 'cinema/cinema_car.html', context)


def cinema_contacts(request):
    return render(request, 'cinema/cinema_contacts.html')


def cinemas(request):
    cinema = Cinema.objects.all()
    return render(request, 'cinema/cinemas.html', {'cinema': cinema})


def event_card(request, event_id, event_slug):
    events = NewsEvents.objects.filter(id=event_id, url=event_slug)
    gallery = get_object_or_404(Gallery, newsevents=event_id)
    gallery_images = gallery.galleryimage_set.all()
    return render(request, 'cinema/event_card.html', {'events': events, 'gallery_images': gallery_images})


def events(request):
    events = NewsEvents.objects.filter(status=True, type=NewsEvents.Type.EVENTS)
    return render(request, 'cinema/events.html', context={'events': events})


def movie_detail(request, movie_id, slug):
    movie = get_object_or_404(MovieCard, id=movie_id, url=slug)
    genres = movie.genre.all()
    now = timezone.now()
    sessions_today = MovieSes.objects.filter(time__gte=now.date(), movie_id=movie_id)
    movie_gallery = get_object_or_404(Gallery, id=movie.gallery.id)
    gallery_images = movie_gallery.galleryimage_set.all()
    first_session = sessions_today.first()
    city = CinemaCity.objects.all()

    grouped_sessions = {}
    for session in sessions_today:
        date_str = session.time.date()
        if date_str not in grouped_sessions:
            grouped_sessions[date_str] = []
        grouped_sessions[date_str].append({
            'session_id': session.id,
            'movie_id': movie.id,
            'movie_slug': movie.url,
            'time': session.time.strftime("%H:%M"),
            'type': session.type,
            'cinema_hall_number': session.cinema_hall.number,
        })

    context = {
        'movie': movie,
        'sessions_today': sessions_today,
        'movie_gallery': movie_gallery,
        'gallery_images': gallery_images,
        'cities': city,
        'grouped_sessions': grouped_sessions,
        'first_session': first_session,
        'genres': genres,
    }
    return render(request, 'cinema/film_card.html', context)


def hall_card(request, hall_id):
    hall = get_object_or_404(CinemaHall, id=hall_id)
    gallery = get_object_or_404(Gallery, id=hall.gallery.id)
    gallery_images = gallery.galleryimage_set.all()
    now = timezone.now()
    end_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    sessions_today = MovieSes.objects.filter(time__gte=now, time__lt=end_of_today, cinema_hall=hall_id)
    context = {
        'hall': hall,
        'gallery_images': gallery_images,
        'sessions_today': sessions_today,
    }
    return render(request, 'cinema/hall_card.html', context)


def news_card(request, news_id, news_slug):
    news = NewsEvents.objects.filter(id=news_id, url=news_slug)
    gallery = get_object_or_404(Gallery, newsevents=news_id)
    gallery_images = gallery.galleryimage_set.all()
    return render(request, 'cinema/event_card.html', {'news': news, 'gallery_images': gallery_images})


def news(request):
    news = NewsEvents.objects.filter(status=True, type=NewsEvents.Type.NEWS)
    return render(request, 'cinema/news.html', context={'news': news})


class ScheduleAjaxFilter(View):
    def get(self, request):
        cinema_id = request.GET.get('cinema_id')
        date_id = request.GET.get('date_id')
        film_id = request.GET.get('film_id')
        hall_id = request.GET.get('hall_id')
        movie_type = request.GET.get('movie_type')

        hall_id = hall_id.split(' ')

        if date_id != 'all':
            date_object = datetime.strptime(date_id, '%b. %d, %Y')
        else:
            date_object = None

        now = timezone.now()
        movie_ses_queryset = MovieSes.objects.filter(time__gte=now.date(), movie__status=True)

        if movie_type != 'all':
            movie_ses_queryset = movie_ses_queryset.filter(type=movie_type)

        if cinema_id != 'all':
            movie_ses_queryset = movie_ses_queryset.filter(cinema_hall__cinema__id=cinema_id)

        if date_id != 'all':
            date_object = timezone.make_aware(date_object, timezone.get_current_timezone())
            movie_ses_queryset = movie_ses_queryset.filter(time__date=date_object.date())

        if film_id != 'all':
            movie_ses_queryset = movie_ses_queryset.filter(movie_id=film_id)

        if hall_id != 'all' and len(hall_id) > 1:
            movie_ses_queryset = movie_ses_queryset.filter(cinema_hall__id=hall_id[1])

        grouped_sessions = {}
        for session in movie_ses_queryset:
            date = session.time.date()
            if date not in grouped_sessions:
                grouped_sessions[date] = []
            grouped_sessions[date].append(session)

        for sessions in grouped_sessions.values():
            sessions.sort(key=lambda s: s.time.date())

        response_data = {
            'html': render(request, 'cinema/schedule_ajax_result.html',
                           {'grouped_sessions': grouped_sessions}).content.decode('utf-8')
        }
        return JsonResponse(response_data)


def schedule(request):
    now = timezone.now()
    movie_list = MovieCard.objects.filter(status=True)
    cinema_list = Cinema.objects.all()
    hall_list = CinemaHall.objects.all()

    movie_sessions = MovieSes.objects.filter(
        movie__in=movie_list,
        time__gte=now.date(),
    ).order_by('time')

    unique_dates = (MovieSes.objects.filter(movie__in=movie_list).annotate(date=Cast('time', DateField()))
                    .values_list('date', flat=True)
                    .distinct()
                    .order_by('date')
                    )

    grouped_sessions = {}
    for date, sessions in groupby(movie_sessions, key=lambda session: session.time.date()):
        grouped_sessions[date] = list(sessions)

    context = {
        'grouped_sessions': grouped_sessions,
        'movie_list': movie_list,
        'cinema_list': cinema_list,
        'hall_list': hall_list,
        'unique_dates': unique_dates,
    }
    return render(request, 'cinema/schedule.html', context)


def soon(request):
    movies_soon = MovieCard.objects.filter(status=False)

    context = {
        'movies_soon': movies_soon,
    }

    return render(request, 'cinema/soon.html', context)


def user_page(request):
    return render(request, 'cinema/user_page.html')


def ticket_booking(request, session_id, movie_id, movie_slug, ses_time):
    reserved_seats = Reservation.objects.filter(session=session_id)
    reserved_seats_json = json.dumps([
        {'row': seat.row, 'seat': seat.seat} for seat in reserved_seats
    ])
    movie = MovieCard.objects.get(id=movie_id)
    session_m = MovieSes.objects.get(id=session_id)

    context = {
        'movie': movie,
        'session_m': session_m,
        'reserved_seats': reserved_seats_json,
    }

    return render(request, 'cinema/ticket_booking.html', context)


def reserve_seats(request):
    if request.method == 'POST':
        selected_seats_json = request.POST.get('selected_seats')
        seat_price = request.POST.get('seat_price')
        selected_seats = json.loads(selected_seats_json)
        user = request.user
        movie_ses_id = request.POST.get('movie_ses_id')
        movie_ses = get_object_or_404(MovieSes, id=movie_ses_id)

        # total_cost = len(selected_seats) * float(seat_price)
        total_cost = 0

        reservations = []
        for seat_info in selected_seats:
            row = int(seat_info['row'])
            seat = int(seat_info['seat'])
            total_cost = int(seat_price)
            reservation = Reservation(user=user, row=row, seat=seat, total_price=total_cost, session=movie_ses)
            reservation.save()
            reservations.append(reservation)

        movie_ses.reserved_seats.set(reservations)

        return JsonResponse({'message': 'Места успешно забронированы!'})

    return JsonResponse({'error': 'Ошибка при бронировании мест.'})


def user_tickets(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'cinema/user_tickets.html', {'reservations': reservations})
