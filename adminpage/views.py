import calendar
import json
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.db.models import Count, Sum
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from adminpage.forms import (BannerTopFormset, BannerTopFormsetSecond,
                             CinemaForm, ContanctPageForm, ContanctPageFormset,
                             ContanctPageFormsetSecond, EventsNewsPageForm,
                             GalleryFormSet, GalleryFormSetSecond, HallForm,
                             MainPageForm, MovieForm, PagesForm, SeoForm, BannerNewsEventsFormset,
                             BannerNewsEventsFormsetSecond, BackBanner)
from adminpage.models import EmailTemplate
from authy.models import CustomUser
from cinema.models import (Banner, Cinema, CinemaHall, Contacts, Gallery,
                           GalleryImage, MainPage, MovieCard, NewsEvents,
                           Pages, Reservation, SeoBlock, BannerSettings, BackgroundBanner)

from .tasks import send_email_task


def stats_page(request):
    return render(request, 'admin_page/stats_page.html')


def user_page(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_page/users.html', {'users': users})


def user_save_data(request, user_pk):
    user = get_object_or_404(CustomUser, pk=user_pk)
    user.name = request.POST.get('name')
    user.second_name = request.POST.get('second_name')
    user.nickname = request.POST.get('nickname')
    user.city = request.POST.get('city')
    birth_date_str = request.POST.get('birth_date')
    user.birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
    user.email = request.POST.get('email')
    user.phone_number = request.POST.get('phone_number')
    user.save()
    return JsonResponse({'message': 'Данные сохранены'})


def delete_user(request, user_pk):
    user = get_object_or_404(CustomUser, pk=user_pk)
    user.delete()
    return redirect('adminpage:user_page')


def films_page(request):
    films_now = MovieCard.objects.filter(status=True)
    film_soon = MovieCard.objects.filter(status=False)

    context = {
        'films_now': films_now,
        'films_soon': film_soon
    }

    return render(request, 'admin_page/films.html', context)


class FilmPage(View):
    template_name = 'admin_page/film_detail.html'

    def get(self, request, movie_id=None, *args, **kwargs):
        film_instance = get_object_or_404(MovieCard, id=movie_id) if movie_id else None

        if movie_id:
            form = MovieForm(instance=film_instance)
            seo_form = SeoForm(prefix='seo-form', instance=film_instance.seo_block)
            formset = GalleryFormSetSecond(queryset=GalleryImage.objects.filter(gallery=film_instance.gallery),
                                           prefix='gallery-formset')
        else:
            form = MovieForm()
            seo_form = SeoForm(prefix='seo-form')
            formset = GalleryFormSet(queryset=GalleryImage.objects.none(), prefix='gallery-formset')

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset,
            'movie_id': movie_id
        }
        return render(request, self.template_name, context)

    def post(self, request, movie_id=None, *args, **kwargs):
        formset = GalleryFormSetSecond(request.POST, request.FILES, prefix='gallery-formset')
        form = MovieForm(request.POST, request.FILES)
        seo_form = SeoForm(request.POST, prefix='seo-form')

        if form.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title_uk']
            title_en = form.cleaned_data['title_en']
            desc = form.cleaned_data['desc_uk']
            desc_en = form.cleaned_data['desc_en']
            trailer_url = form.cleaned_data['trailer_url']
            main_image = form.cleaned_data['main_image']
            seo, created = SeoBlock.objects.get_or_create(url=seo_form.cleaned_data['url'],
                                                          title=seo_form.cleaned_data['title'],
                                                          desc=seo_form.cleaned_data['desc'],
                                                          keywords=seo_form.cleaned_data['keywords'])

            counter = 1
            if movie_id:
                page = get_object_or_404(MovieCard, id=movie_id)
                if page.title != title:
                    page.gallery.title = title
                    page.gallery.save()
                page.title_uk = title
                page.title_en = title_en
                page.trailer_url = trailer_url
                page.desc_uk = desc
                page.desc_en = desc_en
                if main_image:
                    page.main_image = main_image

                for form in formset:
                    if form.is_valid() and form.has_changed():
                        gallery_image = form.save(commit=False)
                        if form.cleaned_data.get('image_id_to_replace'):
                            existing_image = GalleryImage.objects.get(id=form.cleaned_data['image_id_to_replace'])
                            existing_image.title = gallery_image.title
                            existing_image.image = gallery_image.image
                            existing_image.save()
                        else:
                            form.instance.gallery = page.gallery
                            form.save()

                for form in formset.deleted_forms:
                    if form.instance.id:
                        form.instance.delete()

                page.seo_block = seo
                page.save()
                return redirect('adminlte:films_page')
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery = Gallery.objects.filter(title=title_en).first()

                    if not gallery:
                        # Если галереи с указанным заголовком не существует, создаем новую галерею
                        gallery, created = Gallery.objects.create(title=title_en)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    movie_args = {
                        'title_en': title_en,
                        'desc_en': desc_en,
                        'trailer_url': trailer_url,
                        'main_image': main_image,
                        'seo_block': seo,
                        'gallery': gallery,
                        'data': datetime.now(),
                        'url': "-".join(seo.url.split()).lower()
                    }

                    if title:
                        movie_args['title_uk'] = title
                    if desc:
                        movie_args['desc_uk'] = desc

                    about_film = MovieCard.objects.create(**movie_args)

                return redirect('adminlte:films_page')

        else:
            return redirect('adminlte:films_page')


class CinemaListView(ListView):
    model = Cinema
    template_name = 'admin_page/cinemas.html'
    queryset = Cinema.objects.all()
    context_object_name = 'cinemas'


class CinemaAddView(View):
    template_name = 'admin_page/cinema_detail.html'

    def get(self, request, cinema_id=None, *args, **kwargs):
        cinema_instance = get_object_or_404(Cinema, id=cinema_id) if cinema_id else None
        cinema_hall = CinemaHall.objects.filter(cinema=cinema_instance)

        if cinema_instance:
            formset = GalleryFormSetSecond(prefix='gallery-formset',
                                           queryset=GalleryImage.objects.filter(gallery=cinema_instance.gallery))
            form = CinemaForm(instance=cinema_instance)
            seo_form = SeoForm(instance=cinema_instance.seo_block, prefix='seo-form')
        else:
            formset = GalleryFormSet(prefix='gallery-formset', queryset=GalleryImage.objects.none())
            form = CinemaForm()
            seo_form = SeoForm(prefix='seo-form')

        context = {
            'formset': formset,
            'form': form,
            'seo_form': seo_form,
            'cinema_id': cinema_id,
            'cinema_hall': cinema_hall,
        }

        return render(request, self.template_name, context)

    def post(self, request, cinema_id=None, *args, **kwargs):
        formset = GalleryFormSet(request.POST, request.FILES, prefix='gallery-formset')
        form = CinemaForm(request.POST, request.FILES)
        seo_form = SeoForm(request.POST, prefix='seo-form')

        if form.is_valid() and seo_form.is_valid():

            # formset.save()

            title = form.cleaned_data['title_uk']
            title_en = form.cleaned_data['title_en']
            description = form.cleaned_data['desc_uk']
            description_en = form.cleaned_data['desc_en']
            conditions = form.cleaned_data['conditions_uk']
            conditions_en = form.cleaned_data['conditions_en']
            logo = form.cleaned_data['logo']
            top_banner = form.cleaned_data['top_banner']
            seo_url = seo_form.cleaned_data['url']
            seo_title = seo_form.cleaned_data['title']
            seo_keywords = seo_form.cleaned_data['keywords']
            seo_description = seo_form.cleaned_data['desc']
            # print(seo_url, seo_keywords, seo_description, seo_url)
            seo_cinema, created = SeoBlock.objects.get_or_create(title=seo_title, desc=seo_description,
                                                                 keywords=seo_keywords, url=seo_url)
            counter = 1

            if cinema_id:
                cinema = get_object_or_404(Cinema, id=cinema_id)
                if cinema.title != title:
                    cinema.gallery.title = title_en
                    cinema.gallery.save()
                cinema.title_uk = title
                cinema.desc_uk = description
                cinema.conditions_uk = conditions
                cinema.title_en = title_en
                cinema.desc_en = description_en
                cinema.conditions_en = conditions_en
                if logo:
                    cinema.logo = logo
                else:
                    cinema.logo = cinema.logo
                if top_banner:
                    cinema.top_banner = top_banner
                else:
                    cinema.top_banner = cinema.top_banner

                for form in formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE', False):
                            continue
                        else:
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = cinema.gallery
                            gallery_image.save()

                print('----------------------------------------')
                print(formset.deleted_forms)
                for form in formset.deleted_forms:
                    print(formset.deleted_forms)
                    if form.instance.id:
                        form.instance.delete()

                cinema.seo_block = seo_cinema
                cinema.save()
                return redirect('adminlte:cinema_list')
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery, created = Gallery.objects.get_or_create(title=title_en)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    cinema_args = {
                        'title_en': title_en,
                        'desc_en': description_en,
                        'conditions_en': conditions_en
                    }

                    if title:
                        cinema_args['title_uk'] = title
                    if description:
                        cinema_args['desc_uk'] = description

                    Cinema.objects.create(conditions=conditions, logo=logo,
                                          top_banner=top_banner, gallery=gallery, seo_block=seo_cinema, **cinema_args)
                return redirect('adminlte:cinema_list')
        else:
            return redirect('adminlte:cinema_list')

        # return render(request, self.template_name, {'formset': formset, 'form': form, 'seo_form': seo_form})


def delete_cinema(self, cinema_pk):
    cinema = get_object_or_404(Cinema, pk=cinema_pk)
    cinema.delete()
    return redirect('adminlte:cinema_list')


class CinemaHallView(View):
    template_name = 'admin_page/hall_card.html'

    def get(self, request, cinema_id, hall_id=None, *args, **kwargs):
        hall_instance = get_object_or_404(CinemaHall, id=hall_id) if hall_id else None

        if hall_id:
            seo_block_instance = hall_instance.seo_block
            form = HallForm(instance=hall_instance)
            formset = GalleryFormSetSecond(prefix='hall-formset',
                                           queryset=GalleryImage.objects.filter(gallery=hall_instance.gallery))
            seo_form = SeoForm(prefix='seo-form', instance=seo_block_instance)

        else:
            form = HallForm()
            formset = GalleryFormSet(prefix='hall-formset', queryset=GalleryImage.objects.none())
            seo_form = SeoForm(prefix='seo-form')

        context = {
            'form': form,
            'formset': formset,
            'seo_form': seo_form,
            'cinema_id': cinema_id,
            'hall_id': hall_id
        }

        return render(request, self.template_name, context)

    def post(self, request, cinema_id, hall_id=None, *args, **kwargs):
        form = HallForm(request.POST, request.FILES)
        formset = GalleryFormSet(request.POST, request.FILES, prefix='hall-formset')
        seo_form = SeoForm(request.POST, prefix='seo-form')

        if form.is_valid() and seo_form.is_valid():
            hall_number = form.cleaned_data['number']
            desc = form.cleaned_data['desc_uk']
            desc_en = form.cleaned_data['desc_en']
            scheme = form.cleaned_data['scheme']
            top_banner = form.cleaned_data['top_banner']
            seo_url = seo_form.cleaned_data['url']
            seo_title = seo_form.cleaned_data['title']
            seo_keywords = seo_form.cleaned_data['keywords']
            seo_description = seo_form.cleaned_data['desc']
            seo_hall, created = SeoBlock.objects.get_or_create(title=seo_title, desc=seo_description,
                                                               keywords=seo_keywords, url=seo_url)

            cinema = Cinema.objects.get(id=cinema_id)
            counter = 1

            if hall_id:
                hall = get_object_or_404(CinemaHall, id=hall_id)
                if hall.number != hall_number:
                    hall.gallery.title = f'{cinema.title} - {hall_number}'
                    hall.gallery.save()
                hall.number = hall_number
                hall.desc_uk = desc
                print(hall.desc_uk)
                hall.desc_en = desc_en
                print(hall.desc_en)
                if scheme:
                    hall.scheme = scheme
                else:
                    hall.scheme = hall.scheme
                if top_banner:
                    hall.top_banner = top_banner
                else:
                    hall.top_banner = hall.top_banner

                for form in formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE', False):
                            continue
                        else:
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = hall.gallery
                            gallery_image.save()

                for form in formset.deleted_forms:
                    if form.instance.id:
                        form.instance.delete()

                hall.seo_block = seo_hall
                hall.save()
                return redirect('adminlte:cinema_edit', cinema_id=cinema_id)
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery, created = Gallery.objects.get_or_create(title=hall_number)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    CinemaHall.objects.create(number=hall_number, desc_en=desc_en, desc_uk=desc if desc else None,
                                              scheme=scheme, top_banner=top_banner,
                                              gallery=gallery, seo_block=seo_hall, cinema=cinema)

            return redirect("adminlte:cinema_edit", cinema_id=cinema_id)

        return redirect("adminlte:cinema_edit", cinema_id=cinema_id)


def delete_hall(self, hall_id, cinema_id):
    hall = get_object_or_404(CinemaHall, id=hall_id)
    hall.delete()
    return redirect("adminlte:cinema_edit", cinema_id=cinema_id)


class NewsList(ListView):
    model = NewsEvents
    template_name = 'admin_page/news_page.html'
    queryset = NewsEvents.objects.filter(type='NEWS')
    context_object_name = 'news'


class NewsView(View):
    template_name = "admin_page/news_page_detail.html"

    def get(self, request, new_id=None, *args, **kwargs):
        new_instance = get_object_or_404(NewsEvents, id=new_id) if new_id else None

        if new_instance:
            form = EventsNewsPageForm(instance=new_instance)
            formset = GalleryFormSetSecond(prefix='gallery-formset',
                                           queryset=GalleryImage.objects.filter(gallery=new_instance.gallery))
            seo_form = SeoForm(prefix='seo-form', instance=new_instance.seo_block)
        else:
            form = EventsNewsPageForm()
            seo_form = SeoForm(prefix='seo-form')
            formset = GalleryFormSet(prefix='gallery-formset', queryset=GalleryImage.objects.none())

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset,
            'new_id': new_id
        }
        return render(request, self.template_name, context)

    def post(self, request, new_id=None, *args, **kwargs):
        form = EventsNewsPageForm(request.POST, request.FILES)
        seo_form = SeoForm(request.POST, prefix='seo-form')
        formset = GalleryFormSet(request.POST, request.FILES, prefix='gallery-formset')

        print(f"Formset errors: {formset.errors}")
        print(f"Form errors: {form.errors}")
        print(f"Seo form errors: {seo_form.errors}")

        if form.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title_uk']
            title_en = form.cleaned_data['title_en']
            date = form.cleaned_data['date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['desc_uk']
            description_en = form.cleaned_data['desc_en']
            image = form.cleaned_data['main_image']
            url = form.cleaned_data['url']
            seo_url = seo_form.cleaned_data['url']
            seo_title = seo_form.cleaned_data['title']
            seo_keywords = seo_form.cleaned_data['keywords']
            seo_description = seo_form.cleaned_data['desc']
            seo_news, created = SeoBlock.objects.get_or_create(title=seo_title, desc=seo_description,
                                                               keywords=seo_keywords, url=seo_url)

            counter = 1
            if new_id:
                new = get_object_or_404(NewsEvents, id=new_id)
                if new.title != title:
                    new.gallery.title = title_en
                    new.gallery.save()
                new.title_uk = title
                new.title_en = title_en
                new.date = date
                new.status = status
                new.desc_uk = description
                new.desc_en = description_en
                if image:
                    new.main_image = image
                else:
                    new.main_image = new.main_image
                new.url = url

                for form in formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE', False):
                            continue
                        else:
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = new.gallery
                            gallery_image.save()

                for form in formset.deleted_forms:
                    if form.instance.id:
                        form.instance.delete()

                new.seo_block = seo_news
                new.save()
                return redirect('adminlte:news_list')
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery, created = Gallery.objects.get_or_create(title=title_en)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    news = NewsEvents.objects.create(title_en=title_en, title_uk=title if title else None,
                                                     desc_en=description_en,
                                                     desc_uk=description if description else None,
                                                     main_image=image, gallery=gallery,
                                                     date=date, type='NEWS', url=url, status=status,
                                                     cinema=Cinema.objects.first(), seo_block=seo_news)

                return redirect("adminlte:news_list")

        return redirect("adminlte:news_list")


def delete_news(request, news_id):
    new = get_object_or_404(NewsEvents, id=news_id)

    new.delete()

    if new.gallery:
        new.gallery.delete()

    if new.seo_block:
        new.seo_block.delete()

    return redirect("adminlte:events_list")


class EventListView(ListView):
    model = NewsEvents
    template_name = 'admin_page/events_page.html'
    queryset = NewsEvents.objects.filter(type='EVENTS')
    context_object_name = 'events'


class EventView(View):
    template_name = 'admin_page/events_page_detail.html'

    def get(self, request, event_id=None, *args, **kwargs):
        event_instance = get_object_or_404(NewsEvents, id=event_id) if event_id else None

        if event_id:
            form = EventsNewsPageForm(instance=event_instance)
            seo_form = SeoForm(instance=event_instance.seo_block, prefix='seo-form')
            formset = GalleryFormSetSecond(queryset=GalleryImage.objects.filter(gallery=event_instance.gallery),
                                           prefix='gallery-formset')
        else:
            form = EventsNewsPageForm()
            formset = GalleryFormSet(prefix='gallery-formset', queryset=GalleryImage.objects.none())
            seo_form = SeoForm(prefix='seo-form')

        context = {
            'form': form,
            'formset': formset,
            'seo_form': seo_form,
            'event_id': event_id
        }
        return render(request, self.template_name, context)

    def post(self, request, event_id=None, *args, **kwargs):
        form = EventsNewsPageForm(request.POST, request.FILES)
        formset = GalleryFormSet(request.POST, request.FILES, prefix='gallery-formset')
        seo_form = SeoForm(request.POST, prefix='seo-form')

        print(f"Formset errors: {formset.errors}")
        print(f"Form errors: {form.errors}")
        print(f"Seo form errors: {seo_form.errors}")

        if form.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title_uk']
            title_en = form.cleaned_data['title_en']
            date = form.cleaned_data['date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['desc_uk']
            description_en = form.cleaned_data['desc_en']
            image = form.cleaned_data['main_image']
            url = form.cleaned_data['url']
            seo_url = seo_form.cleaned_data['url']
            seo_title = seo_form.cleaned_data['title']
            seo_keywords = seo_form.cleaned_data['keywords']
            seo_description = seo_form.cleaned_data['desc']
            seo_news, created = SeoBlock.objects.get_or_create(title=seo_title, desc=seo_description,
                                                               keywords=seo_keywords, url=seo_url)

            counter = 1
            if event_id:
                event = get_object_or_404(NewsEvents, id=event_id)
                if event.title != title:
                    event.gallery.title = title_en
                    event.gallery.save()
                event.title_uk = title
                event.title_en = title_en
                event.date = date
                event.status = status
                event.desc_uk = description
                event.desc_en = description_en
                if image:
                    event.main_image = image
                else:
                    event.main_image = event.main_image
                event.url = url
                gallery, created = Gallery.objects.get_or_create(title=title_en)

                for form in formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE', False):
                            continue
                        else:
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = event.gallery
                            gallery_image.save()

                for form in formset.deleted_forms:
                    if form.instance.id:
                        form.instance.delete()

                event.seo_block = seo_news
                event.save()
                return redirect('adminlte:events_list')
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery, created = Gallery.objects.get_or_create(title=title_en)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    events = NewsEvents.objects.create(title_en=title_en, desc_en=description_en,
                                                       title_uk=title if title else None,
                                                       desc_uk=description if description else None,
                                                       main_image=image, gallery=gallery,
                                                       date=date, type='EVENTS', url=url, status=status,
                                                       cinema=Cinema.objects.first(), seo_block=seo_news)

                return redirect("adminlte:events_list")

        return redirect("adminlte:events_list")


def delete_events(request, event_id):
    event = get_object_or_404(NewsEvents, id=event_id)

    event.delete()

    if event.gallery:
        event.gallery.delete()

    if event.seo_block:
        event.seo_block.delete()

    return redirect("adminlte:events_list")


class PagesView(ListView):
    model = Pages
    template_name = 'admin_page/pages.html'
    context_object_name = 'pages'

    def get_queryset(self):
        pages_all = Pages.objects.filter(can_delete=True)
        pages_main = Pages.objects.filter(can_delete=False)
        main_page = MainPage.objects.first()
        contact_page = Contacts.objects.first()

        return pages_all, pages_main, main_page, contact_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages_all, pages_main, main_page, contact_page = self.get_queryset()
        context['pages_all'] = pages_all
        context['pages_main'] = pages_main
        context['main_page'] = main_page
        context['contact_page'] = contact_page

        return context


class PageView(View):
    template_name = 'admin_page/about_cinema.html'

    def get(self, request, page_id=None, *args, **kwargs):
        page_instance = get_object_or_404(Pages, id=page_id) if page_id else None

        if page_id:
            form = PagesForm(instance=page_instance)
            seo_form = SeoForm(prefix='seo-form', instance=page_instance.seo_block)
            formset = GalleryFormSetSecond(queryset=GalleryImage.objects.filter(gallery=page_instance.gallery),
                                           prefix='gallery-formset')
        else:
            form = PagesForm()
            seo_form = SeoForm(prefix='seo-form')
            formset = GalleryFormSet(queryset=GalleryImage.objects.none(), prefix='gallery-formset')

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset,
            'page_id': page_id
        }
        return render(request, self.template_name, context)

    def post(self, request, page_id=None, *args, **kwargs):
        formset = GalleryFormSet(request.POST, request.FILES, prefix='gallery-formset')
        form = PagesForm(request.POST, request.FILES)
        seo_form = SeoForm(request.POST, prefix='seo-form')

        if form.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title']
            status = form.cleaned_data['status']
            desc = form.cleaned_data['desc']
            main_image = form.cleaned_data['main_image']
            seo, created = SeoBlock.objects.get_or_create(url=seo_form.cleaned_data['url'],
                                                          title=seo_form.cleaned_data['title'],
                                                          desc=seo_form.cleaned_data['desc'],
                                                          keywords=seo_form.cleaned_data['keywords'])

            counter = 1
            if page_id:
                page = get_object_or_404(Pages, id=page_id)
                if page.title != title:
                    page.gallery.title = title
                    page.gallery.save()
                page.title = title
                page.status = status
                page.desc = desc
                if main_image:
                    page.main_image = main_image
                else:
                    page.main_image = page.main_image
                gallery, _ = Gallery.objects.get_or_create(title=title)

                for form in formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE', False):
                            continue
                        else:
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = page.gallery
                            gallery_image.save()

                for form in formset.deleted_forms:
                    if form.instance.id:
                        form.instance.delete()

                page.seo_block = seo
                page.save()
                return redirect('adminlte:pages')
            else:
                if any(forms.has_changed() for forms in formset):
                    gallery, created = Gallery.objects.get_or_create(title=title)

                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            gallery_image = form.save(commit=False)
                            gallery_image.gallery = gallery
                            gallery_image.save()

                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    about_cinema = Pages.objects.create(title=title, status=status, desc=desc, main_image=main_image,
                                                        type='CINEMA',
                                                        seo_block=seo, gallery=gallery)

                return redirect('adminlte:pages')

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset
        }

        return render(request, self.template_name, context)


class BannerPageView(View):
    template_name = 'admin_page/banner.html'

    def get(self, request, *args, **kwargs):
        top_formset = BannerTopFormset(prefix='top-banner-formset',
                                       queryset=Banner.objects.filter(type="TOP"))
        top_banner_settings = BannerSettings.objects.filter(banner__type='TOP').first()

        bot_formset = BannerNewsEventsFormset(prefix='bot-banner-formset',
                                              queryset=Banner.objects.filter(type='MAIN_NEWS'))
        bot_banner_settings = BannerSettings.objects.filter(banner__type='MAIN_NEWS').first()

        back_banner = BackBanner(instance=BackgroundBanner.objects.first())

        return render(request, self.template_name, {'top_formset': top_formset, 'bot_formset': bot_formset,
                                                    'top_banner_settings': top_banner_settings,
                                                    'bot_banner_settings': bot_banner_settings,
                                                    'back_banner': back_banner})


class TopBannerView(View):
    def post(self, request, *args, **kwargs):
        formset = BannerTopFormset(request.POST, request.FILES, prefix='top-banner-formset')
        top_banner_settings = BannerSettings.objects.filter(banner__type='TOP').first()

        for form in formset.forms:
            if form.is_valid() and form.has_changed():
                if top_banner_settings:
                    banner = form.save()
                    BannerSettings.objects.create(banner=banner, rotation_speed=top_banner_settings.rotation_speed)
                else:
                    banner = form.save()
                    BannerSettings.objects.create(banner=banner, rotation_speed=1000)

        for form in formset.deleted_forms:
            if form.instance.id:
                print(f"Deleting form with id {form.instance.id}")
                form.instance.delete()

        return redirect('adminlte:banner_page')


class MiddleBanner(View):
    def post(self, request, *args, **kwargs):
        back_banner = get_object_or_404(BackgroundBanner, pk=1)

        form = BackBanner(request.POST, request.FILES, instance=back_banner)
        if form.is_valid():
            form.save()
            return redirect('adminlte:banner_page')

        type_data = request.POST.get('type')
        if type_data:
            back_banner.type = type_data
            back_banner.save()
            return redirect('adminlte:banner_page')

        image_data = request.FILES.get('image')
        if image_data:
            back_banner.image = image_data
            back_banner.save()
            return redirect('adminlte:banner_page')

        messages.error(request, 'Не было передано данных для обновления')
        return redirect('adminlte:banner_page')


def delete_middle_image(request):
    back_banner = get_object_or_404(BackgroundBanner, pk=1)
    default_image_path = 'images/icon-image-not-found-free-vector.jpg'
    back_banner.image = default_image_path
    back_banner.type = 'JUST'
    back_banner.save()
    return redirect('adminlte:banner_page')


class NewsEventsBanner(View):
    def post(self, request, *args, **kwargs):
        formset = BannerNewsEventsFormset(request.POST, request.FILES, prefix='bot-banner-formset')
        bot_banner_settings = BannerSettings.objects.filter(banner__type='MAIN_NEWS').first()

        for form in formset.forms:
            if form.is_valid() and form.has_changed():
                form.instance.type = Banner.Types.MAIN_NEWS
                if bot_banner_settings:
                    banner = form.save()
                    BannerSettings.objects.create(banner=banner, rotation_speed=bot_banner_settings.rotation_speed)
                else:
                    banner = form.save()
                    BannerSettings.objects.create(banner=banner, rotation_speed=1000)

        for form in formset.deleted_forms:
            if form.instance.id:
                form.instance.delete()

        return redirect('adminlte:banner_page')


def update_rotation_speed(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        rotation_speed = data.get('rotation_speed')
        banner_type = data.get('banner_type')

        if rotation_speed and banner_type:
            if banner_type == 'TOP':
                top_banners = Banner.objects.filter(type='TOP')
                if top_banners.exists():
                    for banner in top_banners:
                        banner_settings, created = BannerSettings.objects.get_or_create(banner=banner, defaults={
                            'rotation_speed': rotation_speed})
                        if not created:
                            banner_settings.rotation_speed = rotation_speed
                            banner_settings.save()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({'success': False, 'error': 'No top banners found'})
            elif banner_type == 'BOT':
                bot_banners = Banner.objects.filter(type='MAIN_NEWS')
                if bot_banners.exists():
                    for banner in bot_banners:
                        banner_settings, created = BannerSettings.objects.get_or_create(banner=banner, defaults={
                            'rotation_speed': rotation_speed})
                        if not created:
                            banner_settings.rotation_speed = rotation_speed
                            banner_settings.save()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({'success': False, 'error': 'No bot banners found'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid banner type'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request parameters'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        status = data.get('status')
        banner_type = data.get('banner_type')
        top_banner_settings = BannerSettings.objects.filter(banner__type='TOP')[0]
        bot_banner_settings = BannerSettings.objects.filter(banner__type='MAIN_NEWS')[0]

        if status is not None:
            if status == 'ВКЛ':
                for banner in [bot_banner_settings if banner_type == 'bot' else top_banner_settings]:
                    banner.status = True
                    banner.save()
            else:
                for banner in [bot_banner_settings if banner_type == 'bot' else top_banner_settings]:
                    banner.status = False
                    banner.save()

            return JsonResponse({"success": True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request parameters'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


class MainPageView(View):
    template_name = 'admin_page/main_page.html'

    def get(self, request, *args, **kwargs):
        main_page_instance = get_object_or_404(MainPage, id=1)

        form = MainPageForm(instance=main_page_instance)
        seo_form = SeoForm(instance=main_page_instance.seo_block, prefix='seo-form')

        context = {
            'form': form,
            'seo_form': seo_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        main_page_instance = get_object_or_404(MainPage, id=1)

        form = MainPageForm(request.POST, instance=main_page_instance)
        seo_form = SeoForm(request.POST, prefix='seo-form', instance=main_page_instance.seo_block)

        if form.is_valid() and seo_form.is_valid():
            form_instance = form.save(commit=False)
            seo_block_instance = seo_form.save()

            form_instance.seo_block = seo_block_instance
            form_instance.save()

            return redirect('adminlte:pages')

        context = {
            'form': form,
            'seo_form': seo_form
        }
        return render(request, self.template_name, context)


class ContactPageView(View):
    template_name = 'admin_page/contacts.html'

    def get(self, request, *args, **kwargs):
        contact_instance = Contacts.objects.first()

        if contact_instance:
            form = ContanctPageForm(instance=contact_instance)
            seo_block = SeoForm(instance=contact_instance.seo_block, prefix='seo_block')
            if len(Contacts.objects.all()) >= 2:
                formset = ContanctPageFormsetSecond(prefix='contact-formset',
                                                    queryset=Contacts.objects.exclude(pk=contact_instance.pk))
            else:
                formset = ContanctPageFormset(prefix='contact-formset',
                                              queryset=Contacts.objects.exclude(pk=contact_instance.pk))
        else:
            form = ContanctPageForm()
            formset = ContanctPageFormset(prefix='contact-formset', queryset=Contacts.objects.none())
            seo_block = SeoForm(prefix='seo_block')
        return render(request, self.template_name, {'formset': formset, 'form': form, 'seo_form': seo_block})

    def post(self, request, *args, **kwargs):
        contact_instance = Contacts.objects.first()
        form = ContanctPageForm(request.POST, request.FILES, instance=contact_instance)
        seo_form = SeoForm(request.POST, prefix='seo_block')
        formset = ContanctPageFormset(request.POST, request.FILES, prefix='contact-formset',
                                      queryset=Contacts.objects.all())

        if formset.is_valid() and form.is_valid() and seo_form.is_valid():
            formset.save()
            form.save()

            seo_block = contact_instance.seo_block
            if seo_block:
                seo_block.title = seo_form.cleaned_data['title']
                seo_block.desc = seo_form.cleaned_data['desc']
                seo_block.keywords = seo_form.cleaned_data['keywords']
                seo_block.url = seo_form.cleaned_data['url']
                seo_block.save()

            return redirect('adminlte:contact_page')

        return redirect('adminlte:contact_page')


def delete_contact(request, contact_id):
    if request.method == 'DELETE':
        c_object = Contacts.objects.filter(id=contact_id)
        c_object.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])


class EmailSenderView(View):
    def get(self, request, *args, **kwargs):
        users_list = CustomUser.objects.all()
        templates_list = EmailTemplate.objects.all().order_by('-uploaded_at')[:5]

        context = {
            'users_list': users_list,
            'templates_list': templates_list,
        }
        return render(request, 'admin_page/sender.html', context)


def delete_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)

    if request.method == 'GET':
        template.delete()
    return redirect('adminlte:sender')


def upload_template(request):
    if request.method == 'POST' and request.FILES.get('file'):
        print('Скачан')
        uploaded_file = request.FILES['file']
        name = uploaded_file.name

        template = EmailTemplate(name=name, file=uploaded_file)
        template.save()

        all_templates = EmailTemplate.objects.all()
        if all_templates.count() > 5:
            oldest_template = all_templates.order_by('uploaded_at').first()
            oldest_template.delete()

        return JsonResponse({'success': True, 'filename': name})
    else:
        return JsonResponse({'success': False,
                             'error': 'No file found in request'})


def process_form(request):
    if request.method == 'POST':
        photo_selection = request.POST.get('photoSelection')
        template_selection_id = request.POST.get('templateSelection')
        send_checkbox = request.POST.get('selectedUsers')

        template_content = None
        if template_selection_id:
            selected_template = EmailTemplate.objects.get(id=template_selection_id)
            template_content = selected_template.file.read().decode('utf-8')

        elif 'file' in request.FILES:
            uploaded_file = request.FILES.get('file')
            template_content = uploaded_file.read().decode('utf-8')

        recipient_emails = []
        if photo_selection == 'all_users':
            recipient_emails = list(CustomUser.objects.values_list('email', flat=True))

        elif photo_selection == 'selective':
            if send_checkbox:
                recipient_emails = send_checkbox.split(',')
                recipient_emails = [email.strip(' "[]') for email in recipient_emails]

        if recipient_emails:
            task = send_email_task.delay(recipient_emails, "Тема письма", template_content)
            send_email_task.delay(recipient_emails, "Тема письма", template_content)
            return JsonResponse({'success': True, 'task_id': task.task_id})
        else:
            return JsonResponse({'success': False, 'error': 'No recipients specified'})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})


class StatsPage(View):
    template_name = 'admin_page/stats_page.html'

    def get(self, request, *args, **kwargs):
        movies_with_ticket_count = MovieCard.objects.annotate(ticket_count=Count('movieses__reservations'))

        today = timezone.now().date()

        current_week_start = today - timedelta(days=today.weekday())
        current_week_end = current_week_start + timedelta(days=6)

        previous_week_start = current_week_start - timedelta(days=7)
        previous_week_end = previous_week_start + timedelta(days=6)

        def get_ticket_counts(start_date, end_date):
            ticket_counts = {}
            date = start_date
            while date <= end_date:
                tickets_sold = Reservation.objects.filter(session__time__date=date).count()
                ticket_counts[date.strftime('%Y-%m-%d')] = tickets_sold
                date += timedelta(days=1)
            return ticket_counts

        current_week_ticket_counts = get_ticket_counts(current_week_start, current_week_end)
        previous_week_ticket_counts = get_ticket_counts(previous_week_start, previous_week_end)

        all_users = CustomUser.objects.all().count()

        current_year = timezone.now().year

        current_year_income = Reservation.objects.filter(session__time__year=current_year) \
            .values('session__time__month') \
            .annotate(total_income=Sum('total_price'))

        last_year = current_year - 1
        last_year_income = Reservation.objects.filter(session__time__year=last_year) \
            .values('session__time__month') \
            .annotate(total_income=Sum('total_price'))

        monthly_income_current_year = [0] * 12
        monthly_income_last_year = [0] * 12

        for item in current_year_income:
            monthly_income_current_year[item['session__time__month'] - 1] = item['total_income']

        for item in last_year_income:
            monthly_income_last_year[item['session__time__month'] - 1] = item['total_income']

        current_year_data = monthly_income_current_year
        last_year_data = monthly_income_last_year

        current_year_data = [float(item) if item is not None else 0 for item in current_year_data]
        last_year_data = [float(item) if item is not None else 0 for item in last_year_data]

        total_earnings = Reservation.objects.aggregate(total_earnings=Sum('total_price'))['total_earnings']

        if total_earnings is not None:
            formatted_total_income = '${:,.2f}'.format(total_earnings)
        else:
            formatted_total_income = '$0.00'

        return render(request, self.template_name, context={
            'movies_with_ticket_count': movies_with_ticket_count,
            'all_users': all_users,
            'current_week_ticket_counts': current_week_ticket_counts,
            'previous_week_ticket_counts': previous_week_ticket_counts,
            'current_year_data': current_year_data,
            'last_year_data': last_year_data,
            'formatted_total_income': formatted_total_income
        })
