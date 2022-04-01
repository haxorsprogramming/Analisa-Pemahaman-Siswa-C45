from django.contrib import admin
from django.urls import path

from mainApp import views as mainApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainApp.homePage),
    path('import-data-siswa', mainApp.importDataSiswa),
    path('import-data-latih', mainApp.importDataLatih),
    path('olah-data', mainApp.olahData)
]
