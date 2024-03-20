from django.urls import path

from .views import user_page, user_save_data, delete_user, films_page, \
    film_details, CinemaListView, CinemaAddView, delete_cinema, CinemaHallView, delete_hall, NewsView, NewsList, \
    delete_news, EventListView, EventView, PageView, BannerPageView, TopBannerView, PagesView, MainPageView, \
    ContactPageView, EmailSenderView, upload_template, delete_template, process_form

app_name = 'adminlte'

urlpatterns = [
    path('banner_page/', BannerPageView.as_view(), name='banner_page'),
    path('users/', user_page, name='user_page'),
    path('save_user/<int:user_pk>/', user_save_data, name='user_save'),
    path('delete_user/<int:user_pk>/', delete_user, name='delete_user'),
    path('films_page/', films_page, name='films_page'),
    path('films_detail/<str:film_title>/<int:film_id>/', film_details, name='film_details'),
    path('cinemas/', CinemaListView.as_view(), name='cinema_list'),
    path('cinema_add/', CinemaAddView.as_view(), name='cinema_add'),
    path('cinema_edit/<int:cinema_id>/', CinemaAddView.as_view(), name='cinema_edit'),
    path('cinema_delete/<int:cinema_pk>/', delete_cinema, name='cinema_delete'),
    path('hall_card/add/<int:cinema_id>/', CinemaHallView.as_view(), name='hall_add'),
    path('hall_card/<int:cinema_id>/<int:hall_id>/', CinemaHallView.as_view(), name='hall_card'),
    path('hall_delete/<int:hall_id>/<int:cinema_id>/', delete_hall, name='hall_delete'),
    path('news/add/', NewsView.as_view(), name='news_add'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/edit/<int:new_id>/', NewsView.as_view(), name='news_edit'),
    path('news/delete/<int:news_id>/', delete_news, name='delete_news'),
    path('events/', EventListView.as_view(), name='events_list'),
    path('events/add/', EventView.as_view(), name='event_add'),
    path('events/edit/<int:event_id>', EventView.as_view(), name='event_edit'),
    path('page-detail/<int:page_id>/', PageView.as_view(), name='page_detail'),
    path('top_banner/', TopBannerView.as_view(), name='top_banner'),
    path('pages/', PagesView.as_view(), name='pages'),
    path('page-add/', PageView.as_view(), name='page_add'),
    path('page/main-page/', MainPageView.as_view(), name='main_page'),
    path('page/contacts/', ContactPageView.as_view(), name='contact_page'),
    path('sender/', EmailSenderView.as_view(), name='sender'),
    path('upload_template/', upload_template, name='upload_template'),
    path('delete_template/<int:template_id>', delete_template, name='delete_template'),
    path('test/', process_form, name='process_form'),
]
