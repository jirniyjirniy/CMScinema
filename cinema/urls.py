from django.urls import path

from .views import (MovieSessionsAjaxView, ScheduleAjaxFilter, about_cinema,
                    afisha, bar_page, cinema_card, cinema_contacts, cinemas,
                    event_card, events, hall_card, index, movie_detail, news,
                    news_card, reserve_seats, schedule, soon, ticket_booking,
                    user_page, PagesView)

app_name = 'cinema'

urlpatterns = [
    path('', index, name='index'),
    path('about-cinema/', about_cinema, name='about_cinema'),
    path('afisha/', afisha, name='afisha'),
    path('bar/', bar_page, name='bar_page'),
    path('cinema_card/<int:cinema_id>/', cinema_card, name='cinema_card'),
    path('cinema_contacts/', cinema_contacts, name='cinema_contacts'),
    path('cinemas/', cinemas, name='cinemas'),
    path('event_card/<int:event_id>/<slug:event_slug>/', event_card, name='event_card'),
    path('events/', events, name='events'),
    path('film_card/<int:movie_id>/<slug:slug>/', movie_detail, name='film_card'),
    path('hall_card/<int:hall_id>', hall_card, name='hall_card'),
    path('news/', news, name='news'),
    path('news_card/<int:news_id>/<str:news_slug>/', news_card, name='news_card'),
    path('schedule/', schedule, name='schedule'),
    path('schedule_ajax/', ScheduleAjaxFilter.as_view(), name='schedule_ajax'),
    path('soon/', soon, name='soon'),
    path('ticket_booking/<int:session_id>/<int:movie_id>/<str:movie_slug>/<str:ses_time>/', ticket_booking,
         name='ticket_booking'),
    path('user_page/', user_page, name='user_page'),
    path('movie/sessions/ajax/', MovieSessionsAjaxView.as_view(), name='movie_sessions_ajax'),
    path('reserve_seats/', reserve_seats, name='reserve_seats'),
    path('page/<str:url>/', PagesView.as_view(), name='pages'),
]
