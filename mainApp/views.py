
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import uuid
from math import log
from .models import dataSiswa as dataSiswaTbl
from .models import dataLatih as dataLatih
from .models import nilaiGain as nilaiGain
from .F_Helper import setQ

# Create your views here.
def homePage(request):
    return render(request, 'home.html')

def dataSiswa(request):
    ds = dataLatih.objects.all()
    context = {
        'dataSiswa' : ds
    }
    return render(request, 'data-siswa.html', context)

def dataLatihPage(request):
    ds = dataLatih.objects.all()
    context = {
        'dataLatih' : ds
    }
    return render(request, 'data-latih.html', context)

def prediksiPage(request):
    return render(request, 'prediksi.html')

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
    pm['serius']['tinggi'] = setQ('Serius','penyampaian_materi','tinggi')
    pm['serius']['rendah'] = setQ('Serius','penyampaian_materi','rendah')
    pm['serius']['entropy'] = cse(pm['serius']['tinggi'], totalRecord) + cse(pm['serius']['rendah'], totalRecord)
    pm['santai']['tinggi'] = setQ('Santai','penyampaian_materi','tinggi')
    pm['santai']['rendah'] = setQ('Santai','penyampaian_materi','rendah')
    pm['santai']['entropy'] = cse(pm['santai']['tinggi'], totalRecord) + cse(pm['santai']['rendah'], totalRecord)
    pm['serius_santai']['tinggi'] = setQ('Serius Santai','penyampaian_materi','tinggi')
    pm['serius_santai']['rendah'] = setQ('Serius Santai','penyampaian_materi','rendah')
    pm['serius_santai']['entropy'] = cse(pm['serius_santai']['tinggi'], totalRecord) + cse(pm['serius_santai']['rendah'], totalRecord)
    pm['membosankan']['tinggi'] = setQ('Membosankan','penyampaian_materi','tinggi')
    pm['membosankan']['rendah'] = setQ('Membosankan','penyampaian_materi','rendah')
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
    mp['pdf']['tinggi'] = setQ('PDF','media_pembelajaran','tinggi')
    mp['pdf']['rendah'] = setQ('PDF','media_pembelajaran','rendah')
    mp['pdf']['entropy'] = cse(mp['pdf']['tinggi'], totalRecord) + cse(mp['pdf']['rendah'], totalRecord)
    mp['video']['tinggi'] = setQ('Video','media_pembelajaran','tinggi')
    mp['video']['rendah'] = setQ('Video','media_pembelajaran','rendah')
    mp['video']['entropy'] = cse(mp['video']['tinggi'], totalRecord) + cse(mp['video']['rendah'], totalRecord)
    mp['ppt']['tinggi'] = setQ('PPT','media_pembelajaran','tinggi')
    mp['ppt']['rendah'] = setQ('PPT','media_pembelajaran','rendah')
    mp['ppt']['entropy'] = cse(mp['ppt']['tinggi'], totalRecord) + cse(mp['ppt']['rendah'], totalRecord)
    mp['ebook']['tinggi'] = setQ('EBOOK','media_pembelajaran','tinggi')
    mp['ebook']['rendah'] = setQ('EBOOK','media_pembelajaran','rendah')
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
    sb['mendukung']['tinggi'] = setQ('Mendukung','suasana_belajar','tinggi')
    sb['mendukung']['rendah'] = setQ('Mendukung','suasana_belajar','rendah')
    sb['mendukung']['entropy'] = cse(sb['mendukung']['tinggi'], totalRecord) + cse(sb['mendukung']['rendah'], totalRecord)
    sb['tidak_mendukung']['tinggi'] = setQ('Tidak Mendukung','suasana_belajar','tinggi')
    sb['tidak_mendukung']['rendah'] = setQ('Tidak Mendukung','suasana_belajar','rendah')
    sb['tidak_mendukung']['entropy'] = cse(sb['tidak_mendukung']['tinggi'], totalRecord) + cse(sb['tidak_mendukung']['rendah'], totalRecord)
    sb['gain'] = dp['entropy'] - (((sb['mendukung']['tinggi'] + sb['mendukung']['rendah']) / totalRecord) * sb['mendukung']['entropy'])\
        - (((sb['tidak_mendukung']['tinggi'] + sb['tidak_mendukung']['rendah']) / totalRecord) * sb['tidak_mendukung']['entropy'])

    # tugas 
    tg = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }

    tg['baik']['tinggi'] = setQ('Baik','tugas','tinggi')
    tg['baik']['rendah'] = setQ('Baik','tugas','rendah')
    tg['baik']['entropy'] = cse(tg['baik']['tinggi'], totalRecord) + cse(tg['baik']['rendah'], totalRecord)
    tg['cukup']['tinggi'] = setQ('Cukup','tugas','tinggi')
    tg['cukup']['rendah'] = setQ('Cukup','tugas','rendah')
    tg['cukup']['entropy'] = cse(tg['cukup']['tinggi'], totalRecord) + cse(tg['cukup']['rendah'], totalRecord)
    tg['sangat_baik']['tinggi'] = setQ('Sangat Baik','tugas','tinggi')
    tg['sangat_baik']['rendah'] = setQ('Sangat Baik','tugas','rendah')
    tg['sangat_baik']['entropy'] = cse(tg['sangat_baik']['tinggi'], totalRecord) + cse(tg['sangat_baik']['rendah'], totalRecord)
    tg['kurang']['tinggi'] = setQ('Kurang','tugas','tinggi')
    tg['kurang']['rendah'] = setQ('Kurang','tugas','rendah')
    tg['kurang']['entropy'] = cse(tg['kurang']['tinggi'], totalRecord) + cse(tg['kurang']['rendah'], totalRecord)
    tg['gain'] = dp['entropy'] - (((tg['baik']['tinggi'] + tg['baik']['rendah']) / totalRecord) * tg['baik']['entropy'])\
        - (((tg['cukup']['tinggi'] + tg['cukup']['rendah']) / totalRecord) * tg['cukup']['entropy'])\
            - (((tg['sangat_baik']['tinggi'] + tg['sangat_baik']['rendah']) / totalRecord) * tg['sangat_baik']['entropy'])\
                - (((tg['kurang']['tinggi'] + tg['kurang']['rendah']) / totalRecord) * tg['kurang']['entropy'])

    # kehadiran 
    kh = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain' : 0
    }
    kh['baik']['tinggi'] = setQ('Baik', 'kehadiran', 'tinggi')
    kh['baik']['rendah'] = setQ('Baik', 'kehadiran', 'rendah')
    kh['baik']['entropy'] = cse(kh['baik']['tinggi'], totalRecord) + cse(kh['baik']['rendah'], totalRecord)
    kh['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'kehadiran', 'tinggi')
    kh['sangat_baik']['rendah'] = setQ('Sangat Baik', 'kehadiran', 'rendah')
    kh['sangat_baik']['entropy'] = cse(kh['sangat_baik']['tinggi'], totalRecord) + cse(kh['sangat_baik']['rendah'], totalRecord)
    kh['cukup']['tinggi'] = setQ('Cukup', 'kehadiran', 'tinggi')
    kh['cukup']['rendah'] = setQ('Cukup', 'kehadiran', 'rendah')
    kh['cukup']['entropy'] = cse(kh['cukup']['tinggi'], totalRecord) + cse(kh['cukup']['rendah'], totalRecord)
    kh['gain'] = dp['entropy'] - (((kh['baik']['tinggi'] + kh['baik']['rendah']) / totalRecord) * kh['baik']['entropy'])\
        - (((kh['sangat_baik']['tinggi'] + kh['sangat_baik']['rendah']) / totalRecord) * kh['sangat_baik']['entropy'])\
            - (((kh['cukup']['tinggi'] + kh['cukup']['rendah']) / totalRecord) * kh['cukup']['entropy'])

    # praktikum 
    pk = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain' : 0
    }
    pk['baik']['tinggi'] = setQ('Baik', 'praktikum', 'tinggi')
    pk['baik']['rendah'] = setQ('Baik', 'praktikum', 'rendah')
    pk['baik']['entropy'] = cse(pk['baik']['tinggi'], totalRecord) + cse(pk['baik']['rendah'], totalRecord)
    pk['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'praktikum', 'tinggi')
    pk['sangat_baik']['rendah'] = setQ('Sangat Baik', 'praktikum', 'rendah')
    pk['sangat_baik']['entropy'] = cse(pk['sangat_baik']['tinggi'], totalRecord) + cse(pk['sangat_baik']['rendah'], totalRecord)
    pk['cukup']['tinggi'] = setQ('Cukup', 'praktikum', 'tinggi')
    pk['cukup']['rendah'] = setQ('Cukup', 'praktikum', 'rendah')
    pk['cukup']['entropy'] = cse(pk['cukup']['tinggi'], totalRecord) + cse(pk['cukup']['rendah'], totalRecord)
    pk['kurang']['tinggi'] = setQ('Kurang', 'praktikum', 'tinggi')
    pk['kurang']['rendah'] = setQ('Kurang', 'praktikum', 'rendah')
    pk['kurang']['entropy'] = cse(pk['kurang']['tinggi'], totalRecord) + cse(pk['kurang']['rendah'], totalRecord)
    pk['gain'] = dp['entropy'] - (((pk['baik']['tinggi'] + pk['baik']['rendah']) / totalRecord) * pk['baik']['entropy'])\
        - (((pk['sangat_baik']['tinggi'] + pk['sangat_baik']['rendah']) / totalRecord) * pk['sangat_baik']['entropy'])\
            - (((pk['cukup']['tinggi'] + pk['cukup']['rendah']) / totalRecord) * pk['cukup']['entropy'])\
                - (((pk['kurang']['tinggi'] + pk['kurang']['rendah']) / totalRecord) * pk['kurang']['entropy'])

    # uts 
    uts = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }
    uts['baik']['tinggi'] = setQ('Baik', 'uts', 'tinggi')
    uts['baik']['rendah'] = setQ('Baik', 'uts', 'rendah')
    uts['baik']['entropy'] = cse(uts['baik']['tinggi'], totalRecord) + cse(uts['baik']['rendah'], totalRecord)
    uts['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'uts', 'tinggi')
    uts['sangat_baik']['rendah'] = setQ('Sangat Baik', 'uts', 'rendah')
    uts['sangat_baik']['entropy'] = cse(uts['sangat_baik']['tinggi'], totalRecord) + cse(uts['sangat_baik']['rendah'], totalRecord)
    uts['cukup']['tinggi'] = setQ('Cukup', 'uts', 'tinggi')
    uts['cukup']['rendah'] = setQ('Cukup', 'uts', 'rendah')
    uts['cukup']['entropy'] = cse(uts['cukup']['tinggi'], totalRecord) + cse(uts['cukup']['rendah'], totalRecord)
    uts['kurang']['tinggi'] = setQ('Kurang', 'uts', 'tinggi')
    uts['kurang']['rendah'] = setQ('Kurang', 'uts', 'rendah')
    uts['kurang']['entropy'] = cse(uts['kurang']['tinggi'], totalRecord) + cse(uts['kurang']['rendah'], totalRecord)
    uts['gain'] = dp['entropy'] - (((uts['baik']['tinggi'] + uts['baik']['rendah']) / totalRecord) * uts['baik']['entropy'])\
        - (((uts['sangat_baik']['tinggi'] + uts['sangat_baik']['rendah']) / totalRecord) * uts['sangat_baik']['entropy'])\
            - (((uts['cukup']['tinggi'] + uts['cukup']['rendah']) / totalRecord) * uts['cukup']['entropy'])\
                - (((uts['kurang']['tinggi'] + uts['kurang']['rendah']) / totalRecord) * uts['kurang']['entropy'])

    # uas 
    uas = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }
    uas['baik']['tinggi'] = setQ('Baik', 'uas', 'tinggi')
    uas['baik']['rendah'] = setQ('Baik', 'uas', 'rendah')
    uas['baik']['entropy'] = cse(uas['baik']['tinggi'], totalRecord) + cse(uas['baik']['rendah'], totalRecord)
    uas['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'uas', 'tinggi')
    uas['sangat_baik']['rendah'] = setQ('Sangat Baik', 'uas', 'rendah')
    uas['sangat_baik']['entropy'] = cse(uas['sangat_baik']['tinggi'], totalRecord) + cse(uas['sangat_baik']['rendah'], totalRecord)
    uas['cukup']['tinggi'] = setQ('Cukup', 'uas', 'tinggi')
    uas['cukup']['rendah'] = setQ('Cukup', 'uas', 'rendah')
    uas['cukup']['entropy'] = cse(uas['cukup']['tinggi'], totalRecord) + cse(uas['cukup']['rendah'], totalRecord)
    uas['kurang']['tinggi'] = setQ('Kurang', 'uas', 'tinggi')
    uas['kurang']['rendah'] = setQ('Kurang', 'uas', 'rendah')
    uas['kurang']['entropy'] = cse(uas['kurang']['tinggi'], totalRecord) + cse(uas['kurang']['rendah'], totalRecord)
    uas['gain'] = dp['entropy'] - (((uas['baik']['tinggi'] + uas['baik']['rendah']) / totalRecord) * uas['baik']['entropy'])\
        - (((uas['sangat_baik']['tinggi'] + uas['sangat_baik']['rendah']) / totalRecord) * uas['sangat_baik']['entropy'])\
            - (((uas['cukup']['tinggi'] + uas['cukup']['rendah']) / totalRecord) * uas['cukup']['entropy'])\
                - (((uas['kurang']['tinggi'] + uas['kurang']['rendah']) / totalRecord) * uas['kurang']['entropy'])

    # matematika 
    mat = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }
    mat['baik']['tinggi'] = setQ('Baik', 'matematika', 'tinggi')
    mat['baik']['rendah'] = setQ('Baik', 'matematika', 'rendah')
    mat['baik']['entropy'] = cse(mat['baik']['tinggi'], totalRecord) + cse(mat['baik']['rendah'], totalRecord)
    mat['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'matematika', 'tinggi')
    mat['sangat_baik']['rendah'] = setQ('Sangat Baik', 'matematika', 'rendah')
    mat['sangat_baik']['entropy'] = cse(mat['sangat_baik']['tinggi'], totalRecord) + cse(mat['sangat_baik']['rendah'], totalRecord)
    mat['cukup']['tinggi'] = setQ('Cukup', 'matematika', 'tinggi')
    mat['cukup']['rendah'] = setQ('Cukup', 'matematika', 'rendah')
    mat['cukup']['entropy'] = cse(mat['cukup']['tinggi'], totalRecord) + cse(mat['cukup']['rendah'], totalRecord)
    mat['kurang']['tinggi'] = setQ('Kurang', 'matematika', 'tinggi')
    mat['kurang']['rendah'] = setQ('Kurang', 'matematika', 'rendah')
    mat['kurang']['entropy'] = cse(mat['kurang']['tinggi'], totalRecord) + cse(mat['kurang']['rendah'], totalRecord)
    mat['gain'] = dp['entropy'] - (((mat['baik']['tinggi'] + mat['baik']['rendah']) / totalRecord) * mat['baik']['entropy'])\
        - (((mat['sangat_baik']['tinggi'] + mat['sangat_baik']['rendah']) / totalRecord) * mat['sangat_baik']['entropy'])\
            - (((mat['cukup']['tinggi'] + mat['cukup']['rendah']) / totalRecord) * mat['cukup']['entropy'])\
                - (((mat['kurang']['tinggi'] + mat['kurang']['rendah']) / totalRecord) * mat['kurang']['entropy'])

    # bahasa indonesia 
    bindo = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }
    bindo['baik']['tinggi'] = setQ('Baik', 'bindo', 'tinggi')
    bindo['baik']['rendah'] = setQ('Baik', 'bindo', 'rendah')
    bindo['baik']['entropy'] = cse(bindo['baik']['tinggi'], totalRecord) + cse(bindo['baik']['rendah'], totalRecord)
    bindo['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'bindo', 'tinggi')
    bindo['sangat_baik']['rendah'] = setQ('Sangat Baik', 'bindo', 'rendah')
    bindo['sangat_baik']['entropy'] = cse(bindo['sangat_baik']['tinggi'], totalRecord) + cse(bindo['sangat_baik']['rendah'], totalRecord)
    bindo['cukup']['tinggi'] = setQ('Cukup', 'bindo', 'tinggi')
    bindo['cukup']['rendah'] = setQ('Cukup', 'bindo', 'rendah')
    bindo['cukup']['entropy'] = cse(bindo['cukup']['tinggi'], totalRecord) + cse(bindo['cukup']['rendah'], totalRecord)
    bindo['kurang']['tinggi'] = setQ('Kurang', 'bindo', 'tinggi')
    bindo['kurang']['rendah'] = setQ('Kurang', 'bindo', 'rendah')
    bindo['kurang']['entropy'] = cse(bindo['kurang']['tinggi'], totalRecord) + cse(bindo['kurang']['rendah'], totalRecord)
    bindo['gain'] = dp['entropy'] - (((bindo['baik']['tinggi'] + bindo['baik']['rendah']) / totalRecord) * bindo['baik']['entropy'])\
        - (((bindo['sangat_baik']['tinggi'] + bindo['sangat_baik']['rendah']) / totalRecord) * bindo['sangat_baik']['entropy'])\
            - (((bindo['cukup']['tinggi'] + bindo['cukup']['rendah']) / totalRecord) * bindo['cukup']['entropy'])\
                - (((bindo['kurang']['tinggi'] + bindo['kurang']['rendah']) / totalRecord) * bindo['kurang']['entropy'])

    # bahasa inggris 
    bing = {
        'baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'sangat_baik' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'cukup' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'kurang' : {'tinggi':0, 'rendah':0, 'entropy':0},
        'gain': 0
    }
    bing['baik']['tinggi'] = setQ('Baik', 'bing', 'tinggi')
    bing['baik']['rendah'] = setQ('Baik', 'bing', 'rendah')
    bing['baik']['entropy'] = cse(bing['baik']['tinggi'], totalRecord) + cse(bing['baik']['rendah'], totalRecord)
    bing['sangat_baik']['tinggi'] = setQ('Sangat Baik', 'bing', 'tinggi')
    bing['sangat_baik']['rendah'] = setQ('Sangat Baik', 'bing', 'rendah')
    bing['sangat_baik']['entropy'] = cse(bing['sangat_baik']['tinggi'], totalRecord) + cse(bing['sangat_baik']['rendah'], totalRecord)
    bing['cukup']['tinggi'] = setQ('Cukup', 'bing', 'tinggi')
    bing['cukup']['rendah'] = setQ('Cukup', 'bing', 'rendah')
    bing['cukup']['entropy'] = cse(bing['cukup']['tinggi'], totalRecord) + cse(bing['cukup']['rendah'], totalRecord)
    bing['kurang']['tinggi'] = setQ('Kurang', 'bing', 'tinggi')
    bing['kurang']['rendah'] = setQ('Kurang', 'bing', 'rendah')
    bing['kurang']['entropy'] = cse(bing['kurang']['tinggi'], totalRecord) + cse(bing['kurang']['rendah'], totalRecord)
    bing['gain'] = dp['entropy'] - (((bing['baik']['tinggi'] + bing['baik']['rendah']) / totalRecord) * bing['baik']['entropy'])\
        - (((bing['sangat_baik']['tinggi'] + bing['sangat_baik']['rendah']) / totalRecord) * bing['sangat_baik']['entropy'])\
            - (((bing['cukup']['tinggi'] + bing['cukup']['rendah']) / totalRecord) * bing['cukup']['entropy'])\
                - (((bing['kurang']['tinggi'] + bing['kurang']['rendah']) / totalRecord) * bing['kurang']['entropy'])


    # simpan nilai gain 
    nilaiGain.objects.all().delete()
    nilaiGain.objects.create(namaGain='penyampaian_materi', nilaiGain=pm['gain'])
    nilaiGain.objects.create(namaGain='media_pembelajaran', nilaiGain=mp['gain'])
    nilaiGain.objects.create(namaGain='suasana_belajar', nilaiGain=sb['gain'])
    nilaiGain.objects.create(namaGain='tugas', nilaiGain=tg['gain'])
    nilaiGain.objects.create(namaGain='kehadiran', nilaiGain=kh['gain'])
    nilaiGain.objects.create(namaGain='praktikum', nilaiGain=pk['gain'])
    nilaiGain.objects.create(namaGain='uts', nilaiGain=uts['gain'])
    nilaiGain.objects.create(namaGain='uas', nilaiGain=uas['gain'])
    nilaiGain.objects.create(namaGain='matematika', nilaiGain=mat['gain'])
    nilaiGain.objects.create(namaGain='bindo', nilaiGain=bindo['gain'])
    nilaiGain.objects.create(namaGain='bing', nilaiGain=bing['gain'])

    # ambil nilai gain 
    dg = nilaiGain.objects.all().order_by('-nilaiGain')

    dGain = []
    ordGain = 1
    for x in dg:
        lsd = {'nama':'', 'nilai':0, 'ranking':0}
        lsd['nama'] = x.namaGain
        lsd['nilai'] = x.nilaiGain
        lsd['ranking'] = ordGain
        ordGain += 1
        dGain.append(lsd)

    context = {
        'dataPemahaman' : dp,
        'penyampaianMateri' : pm,
        'mediaPembelajaran' : mp,
        'suasanaBelajar' : sb,
        'tugas' : tg,
        'kehadiran' : kh,
        'praktikum' : pk,
        'uts' : uts,
        'uas' : uas,
        'matematika' : mat,
        'bindo' : bindo,
        'bing' : bing,
        'dGain' : dGain
    }

    # return JsonResponse(context, safe=False)
    return render(request, 'prediksi.html', context)

def chartTree(request):
    return render(request, 'chart.html')

def getTotalValue(vk, kriteria, p):
    dl = dataLatih
    if kriteria == 'kehadiran':
        if p == 'tinggi':
            return dl.objects.filter(kehadiran=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(kehadiran=vk).filter(pemahaman='Rendah').count()


def cse(nKriteria, totalData):
    if nKriteria == 0:
        nKriteria = 1
    
    result = -(nKriteria / totalData) * (log(nKriteria / totalData) / log(2))
    return result
