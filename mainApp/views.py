
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import uuid
from math import log
from .models import dataSiswa as dataSiswaTbl
from .models import dataLatih as dataLatih

# Create your views here.
def homePage(request):
    return render(request, 'home.html')

def importDataSiswa(request):
    fileExcel = pd.read_excel('ladun/file_import/DATA_SISWA.xlsx')
    dataSiswa = fileExcel.iloc[:, 0:3]
    dataSiswaArray = dataSiswa.to_numpy()
    
    dataSiswaTbl.objects.all().delete()

    for x in dataSiswaArray:
        username = uuid.uuid4()
        querySimpan = dataSiswaTbl.objects.create(username=username, email='-', nama_lengkap=x[1], kelas=x[2])
        querySimpan.save()
        # print(username)
        # print(x[1])

    context = {
        'status' : 'sukses import data'
    }
    return JsonResponse(context, safe=False)

def importDataLatih(request):
    fileExcel = pd.read_excel('ladun/file_import/DATA_SISWA.xlsx')
    dataSiswa = fileExcel.iloc[:, 0:15]
    dataSiswaArray = dataSiswa.to_numpy()

    siswa = []

    dataLatih.objects.all().delete()

    for x in dataSiswaArray:
        kd = uuid.uuid4()
        qSimpan = dataLatih.objects.create(
            kdAlternatif = kd, 
            namaAlternatif = x[1], 
            kelas = x[2], 
            penyampaian_materi = x[3], 
            media_pembelajaran = x[4],
            suasana_belajar = x[5],
            tugas = x[6],
            kehadiran = x[7],
            praktikum = x[8],
            uts = x[9],
            uas = x[10],
            matematika = x[11],
            bindo = x[12],
            bing = x[13],
            pemahaman = x[14]
        )
        qSimpan.save()

    context = {
        'siswa' : siswa
    }
    return JsonResponse(context, safe=False)

def olahData(request):
    dl = dataLatih
    totalRecord = dl.objects.count()
    # data pemahaman 
    dp = {'tinggi':0, 'rendah':0, 'total':0, 'entropy':0}
    dp['tinggi'] = dl.objects.filter(pemahaman='Tinggi').count()
    dp['rendah'] = dl.objects.filter(pemahaman='Rendah').count()
    dp['total'] = totalRecord
    dp['entropy'] = cse(dp['tinggi'], dp['total']) + cse(dp['rendah'], dp['total'])

    # penyampaian materi 
    pm = {
        'serius' : {'tinggi': 0, 'rendah' : 0, 'entropy':0},
        'santai' : {'tinggi': 0, 'rendah' : 0, 'entropy':0},
        'serius_santai' : {'tinggi': 0, 'rendah' : 0, 'entropy':0},
        'membosankan' : {'tinggi': 0, 'rendah' : 0, 'entropy':0},
        'gain' : 0
    }
    pm['serius']['tinggi'] = dl.objects.filter(penyampaian_materi='Serius').filter(pemahaman='Tinggi').count()
    pm['serius']['rendah'] = dl.objects.filter(penyampaian_materi='Serius').filter(pemahaman='Rendah').count()
    pm['serius']['entropy'] = cse(pm['serius']['tinggi'], totalRecord) + cse(pm['serius']['rendah'], totalRecord)
    pm['santai']['tinggi'] = dl.objects.filter(penyampaian_materi='Santai').filter(pemahaman='Tinggi').count()
    pm['santai']['rendah'] = dl.objects.filter(penyampaian_materi='Santai').filter(pemahaman='Rendah').count()
    pm['santai']['entropy'] = cse(pm['santai']['tinggi'], totalRecord) + cse(pm['santai']['rendah'], totalRecord)
    pm['serius_santai']['tinggi'] = dl.objects.filter(penyampaian_materi='Serius Santai').filter(pemahaman='Tinggi').count()
    pm['serius_santai']['rendah'] = dl.objects.filter(penyampaian_materi='Serius Santai').filter(pemahaman='Rendah').count()
    pm['serius_santai']['entropy'] = cse(pm['serius_santai']['tinggi'], totalRecord) + cse(pm['serius_santai']['rendah'], totalRecord)
    pm['membosankan']['tinggi'] = dl.objects.filter(penyampaian_materi='Membosankan').filter(pemahaman='Tinggi').count()
    pm['membosankan']['rendah'] = dl.objects.filter(penyampaian_materi='Membosankan').filter(pemahaman='Rendah').count()
    pm['membosankan']['entropy'] = cse(pm['membosankan']['tinggi'], totalRecord) + cse(pm['membosankan']['rendah'], totalRecord)
    pm['gain'] = dp['entropy']-(((pm['membosankan']['tinggi'] + pm['membosankan']['rendah']) / totalRecord) * pm['membosankan']['entropy']) \
        - (((pm['serius_santai']['tinggi'] + pm['serius_santai']['rendah']) / totalRecord) * pm['serius_santai']['entropy']) \
            - (((pm['santai']['tinggi'] + pm['santai']['rendah']) / totalRecord) * pm['santai']['entropy']) \
                - (((pm['serius']['tinggi'] + pm['serius']['rendah']) / totalRecord) * pm['serius']['entropy'])

    # media pembelajaran 
    mp = {
        'pdf' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'video' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'ppt' :  {'tinggi':0, 'rendah':0, 'entropy':0},
        'ebook' :  {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain' : 0
    }
    mp['pdf']['tinggi'] = dl.objects.filter(media_pembelajaran='PDF').filter(pemahaman='Tinggi').count()
    mp['pdf']['rendah'] = dl.objects.filter(media_pembelajaran='PDF').filter(pemahaman='Rendah').count()
    mp['pdf']['entropy'] = cse(mp['pdf']['tinggi'], totalRecord) + cse(mp['pdf']['rendah'], totalRecord)
    mp['video']['tinggi'] = dl.objects.filter(media_pembelajaran='Video').filter(pemahaman='Tinggi').count()
    mp['video']['rendah'] = dl.objects.filter(media_pembelajaran='Video').filter(pemahaman='Rendah').count()
    mp['video']['entropy'] = cse(mp['video']['tinggi'], totalRecord) + cse(mp['video']['rendah'], totalRecord)
    mp['ppt']['tinggi'] = dl.objects.filter(media_pembelajaran='PPT').filter(pemahaman='Tinggi').count()
    mp['ppt']['rendah'] = dl.objects.filter(media_pembelajaran='PPT').filter(pemahaman='Rendah').count()
    mp['ppt']['entropy'] = cse(mp['ppt']['tinggi'], totalRecord) + cse(mp['ppt']['rendah'], totalRecord)
    mp['ebook']['tinggi'] = dl.objects.filter(media_pembelajaran='EBOOK').filter(pemahaman='Tinggi').count()
    mp['ebook']['rendah'] = dl.objects.filter(media_pembelajaran='EBOOK').filter(pemahaman='Rendah').count()
    mp['ebook']['entropy'] = cse(mp['ebook']['tinggi'], totalRecord) + cse(mp['ebook']['rendah'], totalRecord)
    mp['gain'] = dp['entropy']-(((mp['pdf']['tinggi'] + mp['pdf']['rendah']) / totalRecord) * mp['pdf']['entropy']) \
        - (((mp['video']['tinggi'] + mp['video']['rendah']) / totalRecord) * mp['video']['entropy']) \
            - (((mp['ppt']['tinggi'] + mp['ppt']['rendah']) / totalRecord) * mp['ppt']['entropy']) \
                - (((mp['ebook']['tinggi'] + mp['ebook']['rendah']) / totalRecord) * mp['ebook']['entropy'])


    # suasana belajar 
    sb = {
        'mendukung' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'tidak_mendukung' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain' : 0
    }
    sb['mendukung']['tinggi'] = dl.objects.filter(suasana_belajar='Mendukung').filter(pemahaman='Tinggi').count()
    sb['mendukung']['rendah'] = dl.objects.filter(suasana_belajar='Mendukung').filter(pemahaman='Rendah').count()
    sb['mendukung']['entropy'] = cse(sb['mendukung']['tinggi'], totalRecord) + cse(sb['mendukung']['rendah'], totalRecord)
    sb['tidak_mendukung']['tinggi'] = dl.objects.filter(suasana_belajar='Tidak Mendukung').filter(pemahaman='Tinggi').count()
    sb['tidak_mendukung']['rendah'] = dl.objects.filter(suasana_belajar='Tidak Mendukung').filter(pemahaman='Rendah').count()
    sb['tidak_mendukung']['entropy'] = cse(sb['tidak_mendukung']['tinggi'], totalRecord) + cse(sb['tidak_mendukung']['rendah'], totalRecord)
    sb['gain'] = dp['entropy'] - (((sb['mendukung']['tinggi'] + sb['mendukung']['rendah']) / totalRecord) * sb['mendukung']['entropy'])\
        - (((sb['tidak_mendukung']['tinggi'] + sb['tidak_mendukung']['rendah']) / totalRecord) * sb['tidak_mendukung']['entropy'])

    context = {
        'dataPemahaman' : dp,
        'penyampaianMateri' : pm,
        'mediaPembelajaran' : mp,
        'suasanaBelajar' : sb
    }
    return JsonResponse(context, safe=False)


def cse(nKriteria, totalData):
    if nKriteria == 0:
        nKriteria = 1
    
    result = -(nKriteria / totalData) * (log(nKriteria / totalData) / log(2))
    return result
