"""
URL configuration for ocr文本识别系统 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from ocr import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('home', views.home, name='home'),
    path('recent-images/', views.recent_images_view, name='recent_images'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('change-password/', views.change_password_view, name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
