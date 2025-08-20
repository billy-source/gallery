from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Photo, Profile
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Photo
from .forms import PhotoForm

def gallery(request):
    all_photos = Photo.objects.all()
    tags = Photo.objects.values_list('tags', flat=True).distinct()
    tag_list = set()
    for tag_str in tags:
        for tag in tag_str.split(','):
            tag_list.add(tag.strip())

    selected_tags = request.GET.getlist('tag')
    if selected_tags:
        all_photos = all_photos.filter(tags__icontains=selected_tags[0])
    
    context = {
        'photos': all_photos,
        'tags': sorted(list(tag_list)),
        'selected_tags': selected_tags,
    }
    return render(request, 'gallery.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('gallery')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile.bio = bio
        profile.save()
        messages.success(request, 'Profile updated successfully!')
    return render(request, 'profile.html', {'profile': profile})


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})


@login_required
def like_photo(request, photo_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        photo = get_object_or_404(Photo, id=photo_id)
        is_liked = False
        if request.user in photo.likes.all():
            photo.likes.remove(request.user)
        else:
            photo.likes.add(request.user)
            is_liked = True
        
        return JsonResponse({'is_liked': is_liked, 'likes_count': photo.likes.count()})
    return redirect('gallery')

def gallery_view(request):
    photos = Photo.objects.all().order_by("-uploaded_at") 
    return render(request, "gallery.html", {"photos": photos})


@login_required
def add_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user  # set uploader
            photo.save()
            return redirect("gallery")  # go back to gallery
    else:
        form = PhotoForm()
    return render(request, "add_photo.html", {"form": form})