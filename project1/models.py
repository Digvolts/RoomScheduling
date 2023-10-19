# namaprojek/namaaplikasi/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nama_tim = models.CharField(max_length=100)
    
    # Menambahkan related_name ke relasi groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        related_query_name='custom_user'
    )
    
    # Menambahkan related_name ke relasi user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        related_query_name='custom_user'
    )
    
class Ruangan(models.Model):
    nama_ruangan = models.CharField(max_length=100)
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='static/admin/img')
    Status_Ruangan = models.BooleanField(default=True)

    def __str__(self):
        return self.nama
    
class PemesananRuangan(models.Model):
    WAKTU_PEMINJAMAN_CHOICES = (
        (1, 'Pagi (09:00 - 12:00)'),
        (2, 'Siang (12:00 - 16:00)'),
        (3, 'Sore (16:00 - 19:00)'),
    )
    
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nama_ruangan = models.CharField(max_length=255)
    waktu_peminjaman = models.IntegerField(choices=WAKTU_PEMINJAMAN_CHOICES)
    status = models.CharField(max_length=10, default='Proses')
    tanggal_pakai = models.DateField()
    alasan = models.TextField(null=True, default=None)
    
    def __str__(self):
        return f"{self.nama_ruangan} - {self.get_waktu_peminjaman_display()}"