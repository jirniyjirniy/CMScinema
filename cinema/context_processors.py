from cinema.models import Pages, SeoBlock, MainPage


def all_page(request):
    pages = Pages.objects.all()
    seo_information = MainPage.objects.get(pk=1)
    return {'pages': pages, 'seo_information': seo_information}