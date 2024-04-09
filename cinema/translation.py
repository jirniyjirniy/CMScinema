from modeltranslation.translator import register, TranslationOptions
from .models import MovieCard, Cinema, CinemaHall, NewsEvents


@register(MovieCard)
class MovieCardTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', )


@register(Cinema)
class MovieCardTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', 'conditions')


@register(CinemaHall)
class MovieCardTranslationOptions(TranslationOptions):
    fields = ('desc',)


@register(NewsEvents)
class MovieCardTranslationOptions(TranslationOptions):
    fields = ('title', 'desc')