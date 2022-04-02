from django.db import models
from numpy import choose

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
    PEMAHAMAN = (('Tinggi', 'Tinggi'), ('Rendah', 'Rendah'))
    PENYAMPAIAN_MATERI = (('Serius Santai', 'Serius Santai'), ('Santai', 'Santai'), ('Serius', 'Serius'), ('Membosankan', 'Membosankan'))
    MEDIA_PEMBELAJARAN = (('PDF', 'PDF'), ('Video', 'Video'), ('PPT', 'PPT'), ('EBOOK', 'EBOOK'))
    SUASANA_BELAJAR = (('Mendukung', 'Mendukung'), ('Tidak Mendukung', 'Tidak Mendukung'))
    TUGAS = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    KEHADIRAN = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'))
    PRAKTIKUM = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    UTS = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    UAS = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    MATEMATIKA = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    BINDO = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    BING = (('Baik', 'Baik'), ('Cukup', 'Cukup'), ('Sangat Baik', 'Sangat Baik'), ('Kurang', 'Kurang'))
    kdAlternatif = models.CharField(max_length=80)
    namaAlternatif = models.CharField(max_length=200)
    kelas = models.CharField(max_length=20)
    penyampaian_materi = models.CharField(max_length=100, choices=PENYAMPAIAN_MATERI)
    media_pembelajaran = models.CharField(max_length=100, choices=MEDIA_PEMBELAJARAN)
    suasana_belajar = models.CharField(max_length=100, choices=SUASANA_BELAJAR)
    tugas = models.CharField(max_length=100, choices=TUGAS)
    kehadiran = models.CharField(max_length=100, choices=KEHADIRAN)
    praktikum = models.CharField(max_length=100, choices=PRAKTIKUM)
    uts = models.CharField(max_length=100, choices=UTS)
    uas = models.CharField(max_length=100, choices=UAS)
    matematika = models.CharField(max_length=100, choices=MATEMATIKA)
    bindo = models.CharField(max_length=100, choices=BINDO)
    bing = models.CharField(max_length=100, choices=BING)
    pemahaman = models.CharField(max_length=100, choices=PEMAHAMAN)
    class Meta:
        db_table = "tbl_data_latih"
    # def __str__(self):
    #     return "{}".format(self.namaAlternatif)

class nilaiGain(models.Model):
    namaGain = models.CharField(max_length=80)
    nilaiGain = models.FloatField(max_length=40)
    class Meta:
        db_table = "tbl_nilai_gain"
