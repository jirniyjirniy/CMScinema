import os
import random
import sys
from datetime import timedelta
from random import randrange

import django
from django.utils import timezone
from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from authy.models import CustomUser
from cinema.models import *

fake = Faker()


def create_fake_users(num):
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
    User.objects.create_superuser(username='admin2', email='admin2@example.com', password='admin')
    User.objects.create_superuser(username='jirniy', email='jirniy@example.com', password='sonya2013')

    for _ in range(num):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, email=email, password=password)
        CustomUser.objects.create(
            user=user,
            name=fake.first_name(),
            second_name=fake.last_name(),
            nickname=fake.user_name(),
            email=email,
            language=fake.random_element(elements=('EN', 'UA')),
            gender=fake.random_element(elements=('MALE', 'FEMALE')),
            card=fake.credit_card_number(),
            phone_number=fake.phone_number(),
            birth_date=fake.date_of_birth(),
            city=fake.city(),
            reg_date=fake.date_time_this_decade(),
        )


def create_fake_movies(num):
    for _ in range(num):
        random_gallery = Gallery.objects.create(title=fake.word(), time_delay=10000)
        random_genres = Genre.objects.order_by('?')[:3]

        seo_block = SeoBlock.objects.create(
            url=fake.word(),
            title=fake.text(),
            keywords=fake.words(),
            desc=fake.text(),
        )

        movie = MovieCard.objects.create(
            title=fake.name(),
            data=fake.date_this_decade(),
            desc=fake.text(),
            main_image='images/image.png',
            gallery=random_gallery,
            trailer_url=fake.words(),
            url=fake.slug(),
            budget=fake.random_number(),
            age=fake.random_int(min=1, max=120),
            time=fake.random_int(min=60, max=300),
            melodist=fake.name(),
            director=fake.name(),
            artist=fake.name(),
            screenwriter=fake.name(),
            status=fake.boolean(),
            seo_block=seo_block,
        )

        GalleryImage.objects.create(
            title=fake.word(),
            image='images/image.png',
            gallery=random_gallery
        )

        for genre in random_genres:
            movie.genre.add(genre)


def create_fake_cinemas(num):
    for _ in range(num):
        gallery_title = fake.word()
        random_gallery, created = Gallery.objects.get_or_create(title=gallery_title, defaults={'time_delay': 10000})
        if created:
            cinema = Cinema.objects.create(
                title=fake.company(),
                desc=fake.text(max_nb_chars=4000),
                conditions=fake.text(max_nb_chars=4000),
                logo='images/image.png',
                top_banner='images/image.png',
                gallery=random_gallery
            )
        else:
            create_fake_cinemas(1)
            return
        city = CinemaCity.objects.create(name=fake.city())
        cinema.city = city
        cinema.save()

        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())
        cinema.seo_block = seo_block
        cinema.save()


def create_fake_cinema_halls(num):
    for _ in range(num):
        random_gallery = Gallery.objects.create(title=fake.word(), time_delay=10000)
        random_cinema = Cinema.objects.order_by('?').first()
        if random_cinema:
            cinema_hall = CinemaHall.objects.create(
                number=randrange(1, 50),
                cinema=random_cinema,
                desc=fake.text(max_nb_chars=5000),
                scheme='images/image.png',
                top_banner='images/image.png',
                gallery=random_gallery
            )
            seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3),
                                                keywords=fake.words(),
                                                desc=fake.text())
            cinema_hall.seo_block = seo_block
            cinema_hall.save()

        GalleryImage.objects.create(
            title=fake.word(),
            image='images/image.png',
            gallery=random_gallery
        )


def random_past_or_future_date():
    random_days = random.randint(-365, 365)
    return timezone.now() + timedelta(days=random_days)


def create_fake_movie_sessions(num):
    for _ in range(num):
        movie = MovieCard.objects.order_by('?').first()
        cinema_hall = CinemaHall.objects.order_by('?').first()
        session_date = random_past_or_future_date()
        movie_session = MovieSes.objects.create(
            time=session_date,
            movie=movie,
            cinema_hall=cinema_hall,
            price=fake.random_int(min=1, max=999),
            type=fake.random_element(elements=('3D', '2D', 'IMAX')),
        )


def create_fake_main_pages(num):
    page_types = ['Кафе - Бар', 'VIP - зал', 'Реклама', 'Детская комната']
    page_types_iterator = iter(page_types)

    for _ in range(num):
        try:
            page_type = next(page_types_iterator)
        except StopIteration:
            page_types_iterator = iter(page_types)
            page_type = next(page_types_iterator)

        gallery = Gallery.objects.create(title=fake.word(), time_delay=10000)

        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())

        page = Pages.objects.create(
            title=page_type,
            desc=fake.text(),
            main_image='images/image.png',
            gallery=gallery,
            type='CINEMA',
            seo_block=seo_block,
            created_at=fake.date_time_this_year(),
            status=random.choice([True, False]),
            can_delete=False
        )

        GalleryImage.objects.create(
            title=fake.word(),
            image='images/image.png',
            gallery=gallery
        )


def create_fake_pages(num):
    for _ in range(num):
        gallery = Gallery.objects.create(title=fake.word(), time_delay=10000)
        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())
        page = Pages.objects.create(
            title=fake.sentence(nb_words=3),
            desc=fake.text(),
            main_image='images/image.png',
            gallery=gallery,
            type=fake.random_element(elements=('VIP', 'CHILD', 'ADS', 'CINEMA')),
            seo_block=seo_block,
            status=random.choice([True, False]),
            created_at=fake.date_time_this_year(),
        )

        GalleryImage.objects.create(
            title=fake.word(),
            image='images/image.png',
            gallery=gallery
        )


def create_fake_news_events(num):
    cinemas = Cinema.objects.all()

    for _ in range(num):
        gallery = Gallery.objects.create(title=fake.word(), time_delay=10000)
        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())

        time = timezone.now()

        random_cinema = random.choice(cinemas)

        news_event = NewsEvents.objects.create(
            title=fake.sentence(),
            main_image='images/image.png',
            desc=fake.text(),
            url=fake.word(),
            status=random.choice([True, False]),
            type=fake.random_element(elements=("NEWS", "EVENTS")),
            date=timezone.now(),
            gallery=gallery,
            cinema=random_cinema,
            seo_block=seo_block
        )

        GalleryImage.objects.create(
            title=fake.word(),
            image='images/image.png',
            gallery=gallery
        )


def create_fake_main_page(num):
    for _ in range(num):
        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())
        main_page = MainPage.objects.create(
            phone_number=fake.phone_number(),
            seo_text=fake.text(),
            seo_block=seo_block,
        )


def create_fake_contacts(num):
    for _ in range(num):
        seo_block = SeoBlock.objects.create(url=fake.word(), title=fake.sentence(nb_words=3), keywords=fake.words(),
                                            desc=fake.text())
        contacts = Contacts.objects.create(
            title=fake.company(),
            logo='images/image.png',
            address=fake.address(),
            coords=f"{fake.latitude()}, {fake.longitude()}",
            seo_block=seo_block,
        )


def create_fake_reservations(num):
    for _ in range(num):
        user = User.objects.order_by('?').first()
        future_session = MovieSes.objects.filter(time__gt=timezone.now(), movie__status=True).order_by('?').first()
        if future_session:
            row = fake.random_int(min=1, max=5)
            seat = fake.random_int(min=1, max=10)
            total_price = future_session.price
            Reservation.objects.create(
                user=user,
                row=row,
                seat=seat,
                total_price=total_price,
                session=future_session,
            )


def create_fake_banners(num):
    for _ in range(num):
        banner = Banner.objects.create(
            url=fake.word(),
            image='images/image.png',
            text=fake.text(),
            type=fake.random_element(elements=('TOP', 'MAIN_NEWS')),
        )
        BannerSettings.objects.create(
            rotation_speed = fake.random_element(elements=[1000, 2000, 3000]),
            banner=banner,
        )


def create_fake_background_banners(num):
    for _ in range(num):
        BackgroundBanner.objects.create(
            type=fake.random_element(elements=('PHOTO', 'JUST')),
            image='images/image.png',
        )


def create_fake_gallery_images(num):
    for _ in range(num):
        random_gallery = Gallery.objects.order_by('?').first()
        if random_gallery:
            gallery_image = GalleryImage.objects.create(
                title=fake.word(),
                image='images/image.png',
                gallery=random_gallery
            )


if __name__ == '__main__':
    create_fake_main_pages(4)
    create_fake_users(50)
    create_fake_movies(20)
    create_fake_cinemas(5)
    create_fake_cinema_halls(10)
    create_fake_movie_sessions(60)
    create_fake_pages(3)
    create_fake_news_events(10)
    create_fake_main_page(1)
    create_fake_contacts(1)
    create_fake_reservations(120)
    create_fake_banners(10)
    create_fake_background_banners(1)
    create_fake_gallery_images(30)
