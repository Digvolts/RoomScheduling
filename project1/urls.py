"""
URL configuration for project1 project.

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

from . import views

def is_admin(user):
    return user.is_superuser

admin.site.site_url = '/accounts/login/'  # Removes the 'View Site' link
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.index_view, name='home'),
    path('popup/', views.pesan_ruangan, name='popup'),
    path('accounts/login/', user_passes_test(is_admin)(views.home_admin_view), name='admin_home'),
    path('tambah-ruangan/', user_passes_test(is_admin)(views.tambah_ruangan), name='tambah_ruangan'),
    path('', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('pesan/', views.list_pemesanan, name='list_pemesanan'),

    path('update_Status_Ruangan/<int:ruangan_id>/', views.update_Status_Ruangan, name='update_Status_Ruangan'),
    path('history/',user_passes_test(is_admin)(views.History),name='history'),
    path('edit_ruangan/<int:ruangan_id>/', views.edit_ruangan, name='edit_ruangan'),
    path('ruangan/<int:ruangan_id>/delete/', views.delete_ruangan, name='delete_ruangan'),
    path('update_alasan/<int:pesanan_id>/', views.update_alasan, name='update_alasan'),
    path('user_calendar/', views.user_calendar_view, name='user_calendar_view'),
    path('admin_calendar/', views.admin_calendar_view, name='admin_calendar_view'),
    path('approval_calendar/', views.approval_calendar_view, name='approval_calendar_view'),
    
    path('approval_home/', views.approval_view, name='approval_home'),
    path('approval_list/', views.approval_list, name='approval_list'),
]

