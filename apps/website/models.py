from django.conf import settings
from bs4 import BeautifulSoup
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    # Ganti TextField jadi CKEditor5Field
    content = CKEditor5Field('Content', config_name='default') 
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    # Ganti TextField jadi CKEditor5Field
    content = CKEditor5Field('Content', config_name='default')
    published_at = models.DateTimeField()

    @property
    def get_thumbnail(self):
        # 1. Prioritas Utama: Featured Image
        if self.image:
            return self.image.url
        
        # 2. Prioritas Kedua: Gambar pertama di CKEditor
        if self.content:
            soup = BeautifulSoup(self.content, 'html.parser')
            img_tag = soup.find('img')
            
            if img_tag:
                src = img_tag.get('src')
                # Jika src adalah link internal (tidak diawali http) 
                # dan tidak diawali /media/, tambahkan prefix media
                if not src.startswith(('http', settings.MEDIA_URL)):
                    # Pastikan tidak double slash
                    return f"{settings.MEDIA_URL.rstrip('/')}/{src.lstrip('/')}"
                return src

        # 3. Prioritas Terakhir: Placeholder jika tidak ada gambar sama sekali
        return "https://via.placeholder.com/600x400?text=No+Image"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Judul Banner")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    image = models.ImageField(upload_to='portal/banners/', verbose_name="Foto Banner")
    url = models.CharField(max_length=255, blank=True, verbose_name="Link URL (CTA)")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title

