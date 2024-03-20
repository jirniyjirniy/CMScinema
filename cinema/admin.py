from django.contrib import admin
from django.contrib.auth.models import User

from .models import MovieCard, Gallery, GalleryImage, Cinema, CinemaHall, MovieSes, Pages, \
    NewsEvents, MainPage, Contacts, Genre, CinemaCity, Reservation, SeoBlock, Banner, BannerSettings

from adminpage.models import EmailTemplate

admin.site.register(MovieCard)
admin.site.register(Gallery)
admin.site.register(GalleryImage)
admin.site.register(Cinema)
admin.site.register(CinemaHall)
admin.site.register(MovieSes)
admin.site.register(Pages)
admin.site.register(NewsEvents)
admin.site.register(MainPage)
admin.site.register(Contacts)
admin.site.register(Genre)
admin.site.register(CinemaCity)
admin.site.register(Reservation)
admin.site.register(SeoBlock)
admin.site.register(Banner)
admin.site.register(BannerSettings)
admin.site.register(EmailTemplate)

