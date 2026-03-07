from django.urls import path
#from . import views
from .views import general, banner, dashboard

app_name = 'website'

urlpatterns = [
    # Halaman Utama
    path('', general.home, name='home'),
    # Profil Sekolah
    path('dashboard/ProfileSekolah/', dashboard.edit_profile, name='edit_profile_sekolah'),
    # Halaman Blog/Berita
    path('blog/', general.blog_list, name='blog_list'),
    path('post/<slug:slug>/', general.post_detail, name='post_detail'),
    path('posting/', general.post_list, name='post_list'),
    path('add/', general.post_create, name='post_create'),
    path('edit/<int:pk>/', general.post_edit, name='post_edit'),
    path('delete/<int:pk>/', general.post_delete, name='post_delete'),
    path('dashboard/pages/', general.page_list, name='page_list'),
    path('page/<slug:slug>/', general.page_detail, name='page_detail'),
    path('pages/add/', general.page_create, name='page_create'),
    path('pages/edit/<int:pk>/', general.page_edit, name='page_edit'),
    path('pages/delete/<int:pk>/', general.page_delete, name='page_delete'),
    #banner
    path('banners/', banner.banner_list, name='banner_list'),
    path('banners/create/', banner.banner_create, name='banner_create'),
    path('banners/<int:pk>/edit/', banner.banner_edit, name='banner_edit'),
    path('banners/delete/<int:pk>/', banner.banner_delete, name='banner_delete'),
]
