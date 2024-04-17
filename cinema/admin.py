from django.contrib import admin
from django.contrib.auth.models import User
from modeltranslation.admin import TranslationAdmin

from adminpage.models import EmailTemplate

from .models import (BackgroundBanner, Banner, BannerSettings, Cinema,
                     CinemaCity, CinemaHall, Contacts, Gallery, GalleryImage,
                     Genre, MainPage, MovieCard, MovieSes, NewsEvents, Pages,
                     Reservation, SeoBlock)


@admin.register(MovieCard)
class MovieCardAdmin(TranslationAdmin):
    list_display = ('title', 'budget', 'status')


admin.site.register(Gallery)
admin.site.register(GalleryImage)
admin.site.register(Cinema, TranslationAdmin)
admin.site.register(CinemaHall, TranslationAdmin)
admin.site.register(MovieSes)
admin.site.register(Pages)
admin.site.register(NewsEvents, TranslationAdmin)
admin.site.register(MainPage)
admin.site.register(Contacts)
admin.site.register(Genre)
admin.site.register(CinemaCity)
admin.site.register(Reservation)
admin.site.register(SeoBlock)
admin.site.register(Banner)
admin.site.register(BannerSettings)
admin.site.register(EmailTemplate)
admin.site.register(BackgroundBanner)
