from django.db import models

# Create your models here.
class dataSiswa(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    nama_lengkap = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    class Meta:
        db_table = "tbl_data_siswa"

class dataKriteria(models.Model):
    kdKriteria = models.CharField(max_length=20)
    namaKriteria = models.CharField(max_length=200)
    class Meta:
        db_table = "tbl_data_kriteria"


class dataNilaiKriteria(models.Model):
    kdNilai = models.CharField(max_length=80)
    kdKriteria = models.CharField(max_length=20)
    nilai = models.CharField(max_length=100)
    class Meta:
        db_table = "tbl_data_nilai_kriteria"

class dataLatih(models.Model):
    kdAlternatif = models.CharField(max_length=80)
    namaAlternatif = models.CharField(max_length=200)
    kelas = models.CharField(max_length=20)
    penyampaian_materi = models.CharField(max_length=100)
    media_pembelajaran = models.CharField(max_length=100)
    suasana_belajar = models.CharField(max_length=100)
    tugas = models.CharField(max_length=100)
    kehadiran = models.CharField(max_length=100)
    praktikum = models.CharField(max_length=100)
    uts = models.CharField(max_length=100)
    uas = models.CharField(max_length=100)
    matematika = models.CharField(max_length=100)
    bindo = models.CharField(max_length=100)
    bing = models.CharField(max_length=100)
    pemahaman = models.CharField(max_length=100)
    class Meta:
        db_table = "tbl_data_latih"

class nilaiGain(models.Model):
    namaGain = models.CharField(max_length=80)
    nilaiGain = models.FloatField(max_length=40)
    class Meta:
        db_table = "tbl_nilai_gain"
