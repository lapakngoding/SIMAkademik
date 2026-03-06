from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Banner
from ..forms import BannerForm # Pastikan sudah membuat BannerForm di forms.py

@login_required
def banner_list(request):
    banners = Banner.objects.all().order_by('order')
    return render(request, 'dashboard/website/banner_list.html', {'banners': banners})

@login_required
def banner_create(request):
    if request.method == 'POST':
        # Tambahkan request.FILES untuk menangani upload gambar
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner baru berhasil ditambahkan.")
            return redirect('website:banner_list')
    else:
        form = BannerForm()
    return render(request, 'dashboard/website/banner_form.html', {'form': form})

@login_required
def banner_edit(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        # Sertakan instance dan request.FILES
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner berhasil diperbarui.")
            return redirect('website:banner_list')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'dashboard/website/banner_form.html', {'form': form, 'edit_mode': True})

@login_required
def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, "Banner telah dihapus.")
        return redirect('website:banner_list')
    return render(request, 'dashboard/website/banner_confirm_delete.html', {'object': banner})
