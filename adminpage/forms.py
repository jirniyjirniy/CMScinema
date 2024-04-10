from django import forms
from django.forms import formset_factory, modelformset_factory

from adminpage.models import EmailTemplate
from cinema.models import (BackgroundBanner, Banner, Cinema, CinemaHall,
                           Contacts, Gallery, GalleryImage, MainPage,
                           MovieCard, NewsEvents, Pages, SeoBlock, BannerSettings)


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


class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieCard
        fields = [
            'title_uk',
            'title_en',
            'desc_uk',
            'desc_en',
            'main_image',
            'trailer_url'
        ]
        widgets = {
            'title_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
            'desc_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Писать сюда...'}),
            'desc_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write here...'}),
            'main_image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}),
            'trailer_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            'title_uk',
            'title_en',
            'desc_uk',
            'desc_en',
            'conditions_uk',
            'conditions_en',
            'logo',
            'top_banner'
        ]

        widgets = {
            'title_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
            'desc_uk': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'desc_en': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
            'conditions_uk': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда'}),
            'conditions_en': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'top_banner': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width:50%'})
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})}


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


# class HallForm(forms.Form):
#     hall_number = forms.CharField(label='Номер зала',
#                                   widget=forms.TextInput(
#                                       attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
#     desc_uk = forms.CharField(label='Описание',
#                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}))
#     desc_en = forms.CharField(label='Описание',
#                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here...'}))
#     scheme = forms.ImageField(label='Схема зала',
#                               widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
#                               required=False)
#     top_banner = forms.ImageField(label='Фото верхнего баннера', widget=forms.ClearableFileInput(
#         attrs={'class': 'form-control', 'style': 'width: 50%;'}), required=False)

class HallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall  # Указываем модель, с которой связана форма
        fields = ['number', 'desc_uk', 'desc_en', 'scheme', 'top_banner']  # Указываем поля, которые хотим включить в форму

        labels = {
            'number': 'Номер зала',
            'desc_uk': 'Описание (українською)',
            'desc_en': 'Описание (англійською)',
            'scheme': 'Схема зала',
            'top_banner': 'Фото верхнього банера',
        }

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'desc_uk': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Писать сюда...'}),
            'desc_en': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here...'}),
            'scheme': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'top_banner': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }


class EventsNewsPageForm(forms.ModelForm):
    class Meta:
        model = NewsEvents
        fields = ['status', 'title_uk', 'title_en', 'date', 'desc_uk', 'desc_en', 'main_image', 'url']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),

            'title_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write here...',
                'type': 'text',
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Писать сюда...'
            }),
            'desc_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'desc_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write here...'
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
        fields = ['status', 'title_uk', 'title_en', 'desc_uk', 'desc_en', 'main_image']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
            'title_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'desc_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'desc_en': forms.Textarea(attrs={
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
                # 'id': 'topPreview'
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


BannerTopFormset = modelformset_factory(Banner, form=BannerForm, extra=1, can_delete=True)
BannerTopFormsetSecond = modelformset_factory(Banner, form=BannerForm, extra=0, can_delete=True)

BannerNewsEventsFormset = modelformset_factory(Banner, form=BannerForm, extra=1, can_delete=True)
BannerNewsEventsFormsetSecond = modelformset_factory(Banner, form=BannerForm, extra=0, can_delete=True)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['phone_number', 'seo_text_uk', 'seo_text_en', 'status']

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Писать сюда...',
                'type': 'text',
            }),
            'seo_text_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Писать сюда...'
            }),
            'seo_text_en': forms.Textarea(attrs={
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


class BackBanner(forms.ModelForm):
    class Meta:
        model = BackgroundBanner
        fields = [
            'image',
            'type',
        ]
        widgets = {
            'image': forms.FileInput(attrs={
                'id': 'photoFile',
                'style': 'display: none;'
            }),
            'type': forms.RadioSelect(attrs={
                'id': 'photoSelection',
                'class': 'radio-buttons',
            }),
        }


class BannerSettings(forms.ModelForm):
    class Meta:
        model = BannerSettings
        fields = ['status', ]

        widgets = {
            'status': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch',
                       'id': 'flexSwitchCheckDefault'}),
        }
