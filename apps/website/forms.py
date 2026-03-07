from django import forms
from django.utils import timezone
from .models import Post, Page, Banner, SchoolProfile
from django_ckeditor_5.widgets import CKEditor5Widget

class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = ['name', 'address', 'google_maps_url', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'Contoh: RA. Al-Marzuqiyah'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '0812-xxxx-xxxx'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'kontak@sekolah.sch.id'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Alamat lengkap sekolah...'
            }),
            'google_maps_url': forms.TextInput(attrs={
                'class': 'form-control text-primary', 
                'placeholder': 'Paste link src iframe di sini...'
            }),
        }

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        # Pastikan format initial value-nya benar-benar bersih (hanya Tahun-Bulan-HariTJam:Menit)
        if not self.instance.pk:
            self.initial['published_at'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        else:
            # Jika sedang EDIT, pastikan data lama diformat ulang agar bisa dibaca input HTML5
            if self.instance.published_at:
                self.initial['published_at'] = self.instance.published_at.strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = ['title', 'content', 'image','published_at']
        widgets = {
            'published_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60', # Ini kuncinya! '60' artinya kelipatan 60 detik (1 menit).
                },
                format='%Y-%m-%dT%H:%M'
            ),
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="extends"
            )
        }

class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # Page biasanya tidak butuh published_at karena sifatnya statis, 
        # tapi pastikan is_published bisa dicentang dengan rapi
        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Page
        fields = ['title', 'content', 'is_published']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="extends"
            )
        }
        
class BannerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Memberikan class bootstrap untuk semua field
        for field_name, field in self.fields.items():
            if field_name != 'is_active':  # Checkbox punya class sendiri di Bootstrap
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Banner
        fields = ['title', 'description', 'image', 'url', 'is_active', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Masukkan deskripsi singkat banner...'}),
            'url': forms.TextInput(attrs={'placeholder': 'Contoh: https://google.com atau /blog/'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
        help_texts = {
            'image': 'Disarankan ukuran 1920x600 px untuk hasil maksimal.',
            'url': 'Gunakan URL lengkap (dengan https://) untuk link luar, atau path (seperti /blog/) untuk link internal.',
        }
