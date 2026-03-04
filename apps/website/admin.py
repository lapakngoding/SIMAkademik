from django.contrib import admin
from .models import Post, Page
from django_ckeditor_5.widgets import CKEditor5Widget # Import ini

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_at')
    exclude = ('slug',)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content':
            # Memaksa penggunaan widget CKEditor 5 secara eksplisit
            kwargs['widget'] = CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name='extends'
            )
        
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        
        # Tetap beri class form-control untuk Title dan Published_at
        if db_field.name in ['title', 'published_at']:
            field.widget.attrs.update({'class': 'form-control'})
            
        return field

    class Media:
        # Tambahkan script inisialisasi manual jika diperlukan
        js = (
            'django_ckeditor_5/dist/bundle.js',
        )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    exclude = ('slug',)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'title':
            field.widget.attrs.update({'class': 'form-control'})
        return field
