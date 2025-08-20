from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("gallery/", views.gallery_view, name="gallery"),
    path("add-photo/", views.add_photo, name="add_photo"),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('like/<int:photo_id>/', views.like_photo, name='like_photo'),
]