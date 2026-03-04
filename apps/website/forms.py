from django import forms
from django.utils import timezone
from .models import Post, Page
from django_ckeditor_5.widgets import CKEditor5Widget

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
        fields = ['title', 'content', 'published_at']
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
