from .models import dataLatih as dataLatih

def setQ(vk, kriteria, p):
    dl = dataLatih
    # penyampaian materi 
    if kriteria == 'penyampaian_materi':
        if p == 'tinggi':
            return dl.objects.filter(penyampaian_materi=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(penyampaian_materi=vk).filter(pemahaman='Rendah').count()
    # Media pembelajaran 
    if kriteria == 'media_pembelajaran':
        if p == 'tinggi':
            return dl.objects.filter(media_pembelajaran=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(media_pembelajaran=vk).filter(pemahaman='Rendah').count()
    # Suasana belajar 
    if kriteria == 'suasana_belajar':
        if p == 'tinggi':
            return dl.objects.filter(suasana_belajar=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(suasana_belajar=vk).filter(pemahaman='Rendah').count()
    # tugas 
    if kriteria == 'tugas':
        if p == 'tinggi':
            return dl.objects.filter(tugas=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(tugas=vk).filter(pemahaman='Rendah').count()
    # kehadiran 
    if kriteria == 'kehadiran':
        if p == 'tinggi':
            return dl.objects.filter(kehadiran=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(kehadiran=vk).filter(pemahaman='Rendah').count()
    # praktikum
    if kriteria == 'praktikum':
        if p == 'tinggi':
            return dl.objects.filter(praktikum=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(praktikum=vk).filter(pemahaman='Rendah').count()
    # uts 
    if kriteria == 'uts':
        if p == 'tinggi':
            return dl.objects.filter(uts=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(uts=vk).filter(pemahaman='Rendah').count()
    # uas 
    if kriteria == 'uas':
        if p == 'tinggi':
            return dl.objects.filter(uas=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(uas=vk).filter(pemahaman='Rendah').count()
    # matematika 
    if kriteria == 'matematika':
        if p == 'tinggi':
            return dl.objects.filter(matematika=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(matematika=vk).filter(pemahaman='Rendah').count()
    # bahasa indonesia 
    if kriteria == 'bindo':
        if p == 'tinggi':
            return dl.objects.filter(bindo=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(bindo=vk).filter(pemahaman='Rendah').count()
    # bahasa inggris 
    if kriteria == 'bing':
        if p == 'tinggi':
            return dl.objects.filter(bing=vk).filter(pemahaman='Tinggi').count()
        if p == 'rendah':
            return dl.objects.filter(bing=vk).filter(pemahaman='Rendah').count()