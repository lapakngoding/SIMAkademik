from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Halaman Utama
    path('', views.home, name='home'),
    # Halaman Blog/Berita
    path('blog/', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posting/', views.post_list, name='post_list'),
    path('add/', views.post_create, name='post_create'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('dashboard/pages/', views.page_list, name='page_list'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('pages/add/', views.page_create, name='page_create'),
    path('pages/edit/<int:pk>/', views.page_edit, name='page_edit'),
    path('pages/delete/<int:pk>/', views.page_delete, name='page_delete'),
]
