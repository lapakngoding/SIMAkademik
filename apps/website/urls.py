from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Halaman Utama
    path('', views.home, name='home'),
    
    # Halaman Blog/Berita
    path('blog/', views.blog_list, name='blog_list'),
    
    # Detail Halaman Statis (contoh: /page/profil-sekolah/)
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    
    # Detail Berita (contoh: /post/juara-lomba-sains/)
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
