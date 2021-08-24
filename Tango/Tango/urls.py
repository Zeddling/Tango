"""Tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rango import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango', views.index, name='index'),
    path('rango/about', views.about, name='about'),
    path('rango/category/add_category', views.add_category, name="add_category"),
    path('rango/category/add_page/<slug:category_name_slug>', views.add_page, name="add_page"),
    path('rango/category/<slug:category_name_slug>', views.show_category, name='show_category'),
    path('rango/login', views.user_login, name='login'),
    path('rango/logout', views.user_logout, name='logout'),
    path('rango/register', views.register, name='register'),
    path('restricted', views.restricted, name='restricted')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
