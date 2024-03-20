from django import forms
from django.forms import formset_factory, modelformset_factory

from adminpage.models import EmailTemplate
from cinema.models import GalleryImage, Cinema, Gallery, SeoBlock, NewsEvents, Pages, Banner, MainPage, Contacts


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'text']

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True
    )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'style': 'margin: 10px 0; width: 100%; height: 80px; padding: 8px; box-sizing: border-box;',
                'placeholder': 'Введите текст'
            }
        ),
        required=True
    )


class MovieForm(forms.Form):
    title = forms.CharField(label='Название Фильма',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Писать сюда...'}))
    main_image = forms.ImageField(label='Главная картинка', required=False, widget=forms.FileInput(
        attrs={'type': 'file', 'id': 'fileInput', 'class': 'form-control'}))
    gallery_images = forms.FileField(label='Галлерея картинок',
                                     widget=forms.ClearableFileInput(), required=False)
    trailer_link = forms.CharField(label='Ссылка на трейлер', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    movie_type = forms.ChoiceField(label='Тип кино', choices=[('3D', '3D'), ('2D', '2D'), ('IMAX', 'IMAX')],
                                   widget=forms.RadioSelect(
                                       attrs={'class': 'btn-group-toggle', 'data-toggle': 'buttons'}))

    seo_url = forms.CharField(label='URL',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    seo_title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    seo_keywords = forms.CharField(label='Key words', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    seo_description = forms.CharField(label='Description',
                                      widget=forms.Textarea(
                                          attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Писать сюда...'}))


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['title', 'desc', 'conditions', 'logo', 'top_banner']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'top_banner': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width:50%'})
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'galleryPreview'})}


GalleryFormSet = modelformset_factory(GalleryImage, form=GalleryForm, extra=1, can_delete=True)
GalleryFormSetSecond = modelformset_factory(GalleryImage, form=GalleryForm, extra=0, can_delete=True)


class SeoForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['url', 'title', 'keywords', 'desc']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...', 'rows': 4}),
        }


class HallForm(forms.Form):
    hall_number = forms.CharField(label='Номер зала',
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    desc = forms.CharField(label='Описание',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
    scheme = forms.ImageField(label='Схема зала',
                              widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
                              required=False)
    top_banner = forms.ImageField(label='Фото верхнего баннера', widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'style': 'width: 50%;'}), required=False)


class EventsNewsPageForm(forms.ModelForm):
    class Meta:
        model = NewsEvents
        fields = ['status', 'title', 'date', 'desc', 'main_image', 'url']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Писать сюда...'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'main_image': forms.ClearableFileInput(attrs={
                'type': 'file',
                'class': 'd-none'
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Писать сюда...'
            }),
        }


class PagesForm(forms.ModelForm):
    class Meta:
        model = Pages
        fields = ['status', 'title', 'desc', 'main_image']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'main_image': forms.ClearableFileInput(attrs={
                'type': 'file',
                'class': 'd-none'
            }),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'url', 'text']

        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'topPreview'
            }),
            'url': forms.TextInput(attrs={
                'type': 'text',
                'style': 'margin: 10px 0; width: 100%; padding: 8px; box-sizing: border-box',
                'placeholder': 'Ссылка на картинку'
            }),
            'text': forms.Textarea(attrs={
                'style': 'margin: 10px 0; width: 100%; height: 80px; padding: 8px; box-sizing: border-box',
                'placeholder': 'Введите текст'
            })
        }


BannerTopFormset = modelformset_factory(Banner, form=BannerForm, extra=1)
BannerTopFormsetSecond = modelformset_factory(Banner, form=BannerForm, extra=0)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['phone_number', 'seo_text', 'status']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'seo_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
        }


class ContanctPageForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['title', 'address', 'coords', 'logo', 'status']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'coords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'logo': forms.ClearableFileInput(attrs={
                # 'class': 'form-control',
                'type': 'file',
                'id': 'topPreview',
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
        }


ContanctPageFormset = modelformset_factory(Contacts, form=ContanctPageForm, extra=1, can_delete=True)
ContanctPageFormsetSecond = modelformset_factory(Contacts, form=ContanctPageForm, extra=0, can_delete=True)


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'file']
