from django.urls import path
from .views import lock_screen, unlock_screen, profile_view

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('lock/', lock_screen, name='lock_screen'),
    path('unlock/', unlock_screen, name='unlock_screen'),
]

