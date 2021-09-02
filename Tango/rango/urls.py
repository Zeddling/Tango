from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('category/add_category', views.add_category, name="add_category"),
    path('category/add_page/<slug:category_name_slug>', views.add_page, name="add_page"),
    path('category/<slug:category_name_slug>', views.show_category, name='show_category'),
    path('goto', views.track_url, name='goto'),
    path('logout', views.user_logout, name='logout'), 
    path('profile/<str:username>', views.profile, name='profile'),
    path('register_profile', views.user_profile, name='register_profile'),
    path('search/<slug:category_name_slug>', views.search, name='search'),
]
