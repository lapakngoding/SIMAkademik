from django import forms
from .models import Post
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tambahkan class Bootstrap agar seragam dengan dashboard guru/siswa
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['published_at'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})

    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="extends"
            )
        }
