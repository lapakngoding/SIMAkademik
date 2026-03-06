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
    # Ganti TextField jadi CKEditor5Field
    content = CKEditor5Field('Content', config_name='default')
    published_at = models.DateTimeField()

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

