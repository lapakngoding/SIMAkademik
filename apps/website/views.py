# apps/website/views.py
from django.shortcuts import render, get_object_or_404
from .models import Page, Post

def home(request):
    # Mengambil 3 post terbaru untuk ditampilkan di section blog depan
    recent_posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')[:3]
    return render(request, 'website/index.html', {'posts': recent_posts})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'website/page_detail.html', {'page': page})

def blog_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'website/blog_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'website/post_detail.html', {'post': post})
