# apps/website/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Page, Post, Banner
from ..forms import PostForm, PageForm

def home(request):
    # Mengambil 3 post terbaru untuk ditampilkan di section blog depan
    banners = Banner.objects.filter(is_active=True).order_by('order')
    recent_posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')[:3]
    
    context = {
        'banners': banners,
        'posts': recent_posts,
    }
    
    return render(request, 'website/index.html', context)

def page_detail(request, slug):
    # Mencari halaman berdasarkan slug
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'website/page_detail.html', {'page': page})
    
def blog_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'website/blog_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published_at__isnull=False)
    # Ambil 5 berita terbaru lainnya untuk sidebar
    sidebar_posts = Post.objects.filter(published_at__isnull=False).exclude(id=post.id).order_by('-published_at')[:5]
    
    return render(request, 'website/post_detail.html', {
        'post': post,
        'sidebar_posts': sidebar_posts
    })

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'dashboard/website/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website:post_list')
    else:
        form = PostForm()
    
    return render(request, 'dashboard/website/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('website:post_list')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'dashboard/website/post_form.html', {'form': form, 'edit_mode': True})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('website:post_list')
    return render(request, 'dashboard/website/post_confirm_delete.html', {'post': post})

@login_required
def page_list(request):
    pages = Page.objects.all().order_by('title')
    return render(request, 'dashboard/website/page_list.html', {'pages': pages})

@login_required
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website:page_list')
    else:
        form = PageForm()
    return render(request, 'dashboard/website/page_form.html', {'form': form})

@login_required
def page_edit(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('website:page_list')
    else:
        form = PageForm(instance=page)
    return render(request, 'dashboard/website/page_form.html', {'form': form, 'edit_mode': True})

@login_required
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('website:page_list')
    return render(request, 'dashboard/website/page_confirm_delete.html', {'page': page})
