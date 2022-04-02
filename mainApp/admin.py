from django.contrib import admin

# Register your models here.
from .models import dataLatih

class dlAdmin(admin.ModelAdmin):
    list_display = [
        'namaAlternatif', 
        'kelas', 
        'penyampaian_materi', 
        'media_pembelajaran',
        'suasana_belajar', 
        'tugas',
        'kehadiran',
        'praktikum',
        'uts',
        'uas',
        'matematika',
        'bindo',
        'bing',
        'pemahaman',
    ]
    list_per_page = 30

admin.site.register(dataLatih, dlAdmin)    