from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from authy.models import CustomUser


class MovieCard(models.Model):
    title = models.CharField(max_length=150)
    genre = models.ManyToManyField('Genre', null=True, blank=True)
    data = models.DateField()
    desc = models.TextField(max_length=5000)
    main_image = models.ImageField(upload_to='cinema_image/main_images/movie/%Y/%m/%d/', blank=True)
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE)
    trailer_url = models.CharField(max_length=1000)
    url = models.SlugField(max_length=250)
    budget = models.IntegerField(default=0)
    age = models.PositiveSmallIntegerField(default=16)
    time = models.PositiveSmallIntegerField(default=120)
    melodist = models.CharField(max_length=250)
    director = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    screenwriter = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cinema:film_card', args=[self.id, self.url])


class Genre(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    time_delay = models.PositiveSmallIntegerField(default=10000)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cinema_image/gallery/%Y/%m/%d/')
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Cinema(models.Model):
    title = models.CharField(max_length=150)
    city = models.ForeignKey('CinemaCity', on_delete=models.CASCADE, null=True, blank=True)
    desc = models.TextField(max_length=5000)
    conditions = models.TextField(max_length=5000)
    logo = models.ImageField(upload_to='cinema_image/main_images/%Y/%m/%d/', blank=True)
    top_banner = models.ImageField(upload_to='cinema_image/main_images/%Y/%m/%d/', blank=True)
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE)
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cinema:cinema_card', args=[self.id])


class CinemaCity(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    number = models.SmallIntegerField(default=1)
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE)
    desc = models.TextField(max_length=5000)
    scheme = models.ImageField(upload_to='cinema_image/main_images/cinema_hall/%Y/%m/%d', blank=True)
    top_banner = models.ImageField(upload_to='cinema_image/main_images/cinema_hall/%Y/%m/%d', blank=True)
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.cinema.title} - Хол №{str(self.number)}'

    def get_absolute_url(self):
        return reverse('cinema:hall_card', args=[self.id])


class MovieSes(models.Model):
    class MovieType(models.TextChoices):
        ThreeD = '3D', '3D'
        TwoD = '2D', '2D'
        IMAX = 'IMAX', 'IMAX'

    time = models.DateTimeField(blank=True, null=True)
    movie = models.ForeignKey(MovieCard, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    type = models.CharField(max_length=6, choices=MovieType.choices, default=MovieType.ThreeD)
    reserved_seats = models.ManyToManyField('Reservation', blank=True, null=True)

    def __str__(self):
        return f'{self.movie}| {self.type} - {self.cinema_hall} - {self.time}'

    def get_absolute_url(self):
        return reverse('cinema:ticket_booking', args=[self.id, self.movie.id, self.movie.url, self.time])


class Pages(models.Model):
    class PageType(models.TextChoices):
        VIP = 'VIP', 'Vip'
        CHILD = 'CHILD', 'Child'
        ADS = 'ADS', 'Ads'
        CINEMA = 'CINEMA', 'About Cinema'

    title = models.CharField(max_length=150)
    desc = models.TextField()
    main_image = models.ImageField(upload_to='cinema_image/main_images/pages/%Y/%m/%d/', blank=True)
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=PageType.choices, default=PageType.VIP)
    status = models.BooleanField(default=True)
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {self.type}'


class NewsEvents(models.Model):
    class Type(models.TextChoices):
        NEWS = 'NEWS', 'News'
        EVENTS = 'EVENTS', 'Events'

    title = models.CharField(max_length=150)
    desc = models.TextField(max_length=5000)
    main_image = models.ImageField(upload_to='cinema_image/main_images/news_events/%Y/%m/%d/', blank=True)
    gallery = models.OneToOneField('Gallery', on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    status = models.BooleanField(default=False)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=6, choices=Type.choices, default=Type.NEWS)
    date = models.DateField()
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.type}'

    def get_absolute_url(self):
        return reverse('cinema:event_card', args=[self.id, self.url])


class MainPage(models.Model):
    phone_number = models.CharField(max_length=30)
    seo_text = models.TextField()
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'Main page - {self.phone_number} - {self.seo_text}'


class Contacts(models.Model):
    title = models.CharField(max_length=150)
    address = models.TextField()
    coords = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='cinema_image/main_images/contacts/%Y/%m/%d/', blank=True)
    status = models.BooleanField(default=True)
    seo_block = models.ForeignKey('SeoBlock', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.address}'


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()
    total_price = models.DecimalField(default=10, max_digits=5, decimal_places=2)
    session = models.ForeignKey(MovieSes, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)

    def __str__(self):
        return f"Reservation| {self.user.first_name} {self.user.last_name} - Row: {self.row}, Seat: {self.seat}, Total Price: {self.total_price}"


class SeoBlock(models.Model):
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    keywords = models.CharField(max_length=250)
    desc = models.TextField()

    def __str__(self):
        return f'{self.title}'


class Banner(models.Model):
    class Types(models.TextChoices):
        TOP_BANNER = 'TOP', 'Top banner'
        MAIN_NEWS = 'MAIN_NEWS', 'Main news'

    image = models.ImageField(upload_to='cinema_image/main_images/banner/%Y/%m/%d/')
    url = models.CharField(max_length=250)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.TOP_BANNER)

    def __str__(self):
        return self.type


class BannerSettings(models.Model):
    rotation_speed = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=True)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)

    def __str__(self):
        return self.banner.type


class BackgroundBanner(models.Model):
    class Type(models.TextChoices):
        PHOTO = 'PHOTO', 'Фото на фон'
        JUST = 'JUST', "Просто фон"

    type = models.CharField(max_length=5, choices=Type.choices, default=Type.PHOTO)
    image = models.ImageField(upload_to='cinema_image/main_images/background_banner/%Y/%m/%d/')

    def __str__(self):
        return f'Background banner {self.type}'
