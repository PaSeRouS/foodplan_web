"""foodplan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from . import settings
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('', include('django.contrib.auth.urls')),
    path('order/', views.order, name='order_page'),
    path('registration/', views.register, name='registration'),
    path('subscriptions/<int:subscription_id>', views.subscription_detail, name='subscription_page'),
    # path('lk/', views.lk, name='lk'),
    path('accounts/profile/', views.lk, name='lk'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
