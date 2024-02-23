from datetime import datetime

from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from adminpage.forms import GalleryImageForm, MovieForm, GalleryFormSet, CinemaForm, SeoForm, GalleryFormSetSecond, \
    HallForm, EventsNewsPageForm, PagesForm, BannerTopFormset, BannerTopFormsetSecond, MainPageForm, \
    ContanctPageFormset, ContanctPageForm, ContanctPageFormsetSecond
from authy.models import CustomUser
from cinema.models import Gallery, GalleryImage, MovieCard, SeoBlock, Cinema, CinemaHall, NewsEvents, Pages, Banner, \
    MainPage, Contacts


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


def film_details(request, film_title, film_id):
    GalleryImagesFormSet = formset_factory(GalleryImageForm, extra=1)
    movie = get_object_or_404(MovieCard, id=film_id)
    seo, created = SeoBlock.objects.get_or_create(url=movie.trailer_url, title=movie.title,
                                                  keywords=movie.title,
                                                  desc=movie.desc)
    form = MovieForm(initial={'title': movie.title,
                              'description': movie.desc,
                              'trailer_link': movie.trailer_url,
                              'main_image': movie.main_image,
                              'seo_url': seo.url,
                              'seo_title': seo.title,
                              'seo_keywords': seo.keywords,
                              'seo_description': seo.desc}
                     )

    gallery, created = Gallery.objects.get_or_create(title=movie.title)
    images = GalleryImage.objects.filter(gallery=gallery)

    if request.method == 'POST':
        formset = GalleryImagesFormSet(request.POST, request.FILES, prefix='photo')
        movie_form = MovieForm(request.POST, request.FILES)

        if formset.is_valid() and movie_form.is_valid():
            ...
    else:
        movie_form = MovieForm()
        formset = GalleryImagesFormSet(prefix='photo')

    context = {
        'form': form,
        'formset': formset,
        'movie': movie,
        'images': images,
    }

    return render(request, 'admin_page/film_detail.html', context)


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

        print(f"Formset errors: {formset.errors}")
        print(f"Form errors: {form.errors}")
        print(f"Seo form errors: {seo_form.errors}")

        if form.is_valid() and formset.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['desc']
            conditions = form.cleaned_data['conditions']
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
                    cinema.gallery.title = title
                    cinema.gallery.save()
                cinema.title = title
                cinema.desc = description
                cinema.conditions = conditions
                if logo:
                    cinema.logo = logo
                else:
                    cinema.logo = cinema.logo
                if top_banner:
                    cinema.top_banner = top_banner
                else:
                    cinema.top_banner = cinema.top_banner
                gallery, created = Gallery.objects.get_or_create(title=title)
                images = GalleryImage.objects.filter(gallery=gallery).last().title[-1]
                counter += int(images)
                for form in formset.extra_forms:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{title} {counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1
                cinema.gallery = gallery
                cinema.seo_block = seo_cinema
                cinema.save()
                return redirect('adminlte:cinema_list')
            else:
                gallery, created = Gallery.objects.get_or_create(title=title)
                for form in formset:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{title} {counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1

                Cinema.objects.create(title=title, desc=description, conditions=conditions, logo=logo,
                                      top_banner=top_banner, gallery=gallery, seo_block=seo_cinema)

                return redirect('adminlte:cinema_list')

        return render(request, self.template_name, {'formset': formset, 'form': form, 'seo_form': seo_form})


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
            form = HallForm(initial={'hall_number': hall_instance.number, 'desc': hall_instance.desc,
                                     'scheme': hall_instance.scheme, 'top_banner': hall_instance.top_banner})
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
        print(f"Formset errors: {formset.errors}")
        print(f"Form errors: {form.errors}")
        print(f"Seo form errors: {seo_form.errors}")
        if form.is_valid() and seo_form.is_valid() and formset.is_valid():
            hall_number = form.cleaned_data['hall_number']
            desc = form.cleaned_data['desc']
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
                hall.desc = desc
                if scheme:
                    hall.scheme = scheme
                else:
                    hall.scheme = hall.scheme
                if top_banner:
                    hall.top_banner = top_banner
                else:
                    hall.top_banner = hall.top_banner
                gallery, created = Gallery.objects.get_or_create(title=f'{cinema.title} - {hall_number}')
                for form in formset.extra_forms:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{cinema.title}|{hall_number}-{counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1
                hall.gallery = gallery
                hall.seo_block = seo_hall
                hall.save()
                return redirect('adminlte:cinema_edit', cinema_id=cinema_id)
            else:
                gallery, created = Gallery.objects.get_or_create(title=f'{cinema.title} - {hall_number}')

                for form in formset:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{cinema.title}|{hall_number}-{counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1

                CinemaHall.objects.create(number=hall_number, desc=desc, scheme=scheme, top_banner=top_banner,
                                          gallery=gallery, seo_block=seo_hall, cinema=cinema)

            return redirect("adminlte:cinema_edit", cinema_id=cinema_id)

        return render(request, self.template_name,
                      {'formset': formset, 'form': form, 'seo_form': seo_form, 'cinema_id': cinema_id})


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

        if form.is_valid() and seo_form.is_valid() and formset.is_valid():
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['desc']
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
                    new.gallery.title = title
                    new.gallery.save()
                new.title = title
                new.date = date
                new.status = status
                new.desc = description
                if image:
                    new.main_image = image
                else:
                    new.main_image = new.main_image
                new.url = url
                gallery, created = Gallery.objects.get_or_create(title=title)
                for form in formset.extra_forms:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{new.title}|-{counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1
                new.gallery = gallery
                new.seo_block = seo_news
                new.save()
                return redirect('adminlte:news_list')
            else:
                gallery, created = Gallery.objects.get_or_create(title=f'{title}')
                for form in formset:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{title}-{counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1

                news = NewsEvents.objects.create(title=title, desc=description, main_image=image, gallery=gallery,
                                                 date=date, type='NEWS', url=url, status=status,
                                                 cinema=Cinema.objects.first(), seo_block=seo_news)

                return redirect("adminlte:news_list")

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset
        }
        return render(request, self.template_name, context)


def delete_news(request, news_id):
    new = NewsEvents.objects.get(id=news_id)
    new.delete()
    return redirect("adminlte:news_list")


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

        if form.is_valid() and formset.is_valid() and seo_form.is_valid():
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['desc']
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
                    event.gallery.title = title
                    event.gallery.save()
                event.title = title
                event.date = date
                event.status = status
                event.desc = description
                if image:
                    event.main_image = image
                else:
                    event.main_image = event.main_image.url
                event.url = url
                gallery, created = Gallery.objects.get_or_create(title=title)
                for form in formset.extra_forms:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{event.title} - {counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1
                event.gallery = gallery
                event.seo_block = seo_news
                event.save()
                return redirect('adminlte:events_list')
            else:
                gallery, created = Gallery.objects.get_or_create(title=title)
                for form in formset:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{title} - {counter}'
                    GalleryImage.objects.get_or_create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1

                events = NewsEvents.objects.create(title=title, desc=description, main_image=image, gallery=gallery,
                                                   date=date, type='EVENTS', url=url, status=status,
                                                   cinema=Cinema.objects.first(), seo_block=seo_news)

                return redirect("adminlte:events_list")

        context = {
            'form': form,
            'seo_form': seo_form,
            'formset': formset
        }

        return render(request, self.template_name, context)


class PagesView(ListView):
    model = Pages
    template_name = 'admin_page/pages.html'
    context_object_name = 'pages'

    def get_queryset(self):
        pages_all = Pages.objects.filter(can_delete=True)
        pages_main = Pages.objects.filter(can_delete=False)
        main_page = MainPage.objects.first()

        return pages_all, pages_main, main_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages_all, pages_main, main_page = self.get_queryset()
        context['pages_all'] = pages_all
        context['pages_main'] = pages_main
        context['main_page'] = main_page

        return context


class PageView(View):
    template_name = 'admin_page/about_cinema.html'

    def get(self, request, page_id=None, *args, **kwargs):
        page_instance = get_object_or_404(Pages, id=page_id) if page_id else None

        if page_id:
            form = PagesForm(instance=page_instance)
            seo_form = SeoForm(prefix='seo-form', instance=page_instance.seo_block)
            formset = GalleryFormSet(queryset=GalleryImage.objects.filter(gallery=page_instance.gallery),
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

        print('forms error', form.errors)
        print('formset error', formset.errors)
        print('seo_forms error', seo_form.errors)

        if form.is_valid() and seo_form.is_valid() and formset.is_valid():
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
                for form in formset.extra_forms:
                    gallery_image = form.cleaned_data['image']
                    gallery_instance_title = f'{page.title} - {counter}'
                    GalleryImage.objects.create(title=gallery_instance_title, gallery=gallery, image=gallery_image)
                    counter += 1
                page.gallery = gallery
                page.seo_block = seo
                page.save()
                return redirect('adminlte:pages')
            else:
                gallery, created = Gallery.objects.get_or_create(title=title)
                for form in formset:
                    gallery_images = form.cleaned_data['image']
                    gallery_image_title = f'{title} - {counter}'
                    GalleryImage.objects.create(title=gallery_image_title, image=gallery_images, gallery=gallery)
                    counter += 1

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
        if Banner.objects.all():
            top_formset = BannerTopFormsetSecond(prefix='top-banner-formset',
                                                 queryset=Banner.objects.filter(type="TOP"))
        else:
            top_formset = BannerTopFormset(prefix='top-banner-formset')
        return render(request, self.template_name, {'top_formset': top_formset})


class TopBannerView(View):
    def post(self, request, *args, **kwargs):
        formset = BannerTopFormset(request.POST, request.FILES, prefix='top-banner-formset')
        print(formset.errors)

        if formset.is_valid():
            for form in formset.extra_forms:
                form.save()
            formset.save()
            return redirect('adminlte:banner_page')
        return redirect('adminlte:banner_page')


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
            print(len(Contacts.objects.all()))
            if len(Contacts.objects.all()) >= 2:
                formset = ContanctPageFormsetSecond(prefix='contact-formset',
                                                    queryset=Contacts.objects.exclude(pk=contact_instance.pk))
            else:
                formset = ContanctPageFormset(prefix='contact-formset',
                                              queryset=Contacts.objects.exclude(pk=contact_instance.pk))
        else:
            form = ContanctPageForm()
            formset = ContanctPageFormset(prefix='contact-formset', queryset=Contacts.objects.none())
        return render(request, self.template_name, {'formset': formset, 'form': form})

    def post(self, request, *args, **kwargs):
        contact_instance = Contacts.objects.first()
        form = ContanctPageForm(request.POST, request.FILES, instance=contact_instance)

        formset = ContanctPageFormset(request.POST, request.FILES, prefix='contact-formset',
                                      queryset=Contacts.objects.all())

        print('Ошибки в formset', formset.errors)
        print('Ошибки в form', form.errors)

        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            return redirect('adminlte:contact_page')

        context = {
            'formset': formset,
            'form': form,
        }
        return render(request, self.template_name, context)
