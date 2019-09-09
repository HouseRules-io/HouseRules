"""houserules URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from hr import views
from django.conf.urls.static import static
from django.conf import settings

 
urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('', views.index, name = 'index'),
    path('accounts/', include('django.contrib.auth.urls'), name = 'accounts'),
    path('hw/', views.HelloWorld),

    path('signup', views.signup, name = 'signup'),
    path('dev', views.dev, name = 'dev'),


    path('house/<str:House_hex>/', views.house, name = 'house'),
    path('house/new', views.newHouse, name = 'new_house'),
    path('rulebook/<int:Rulebook_id>/', views.rulebook, name = 'rulebook'),
    path('rulebook/new/', views.newRulebook, name = 'new_rulebook'),
    path('rule/<int:Rule_id>/', views.rule, name = 'rule'),
    path('rule/new/', views.newRule, name = 'new_rule'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
