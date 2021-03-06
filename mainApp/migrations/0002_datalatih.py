# Generated by Django 3.2.5 on 2022-03-31 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dataLatih',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kdAlternatif', models.CharField(max_length=80)),
                ('namaAlternatif', models.CharField(max_length=200)),
                ('kelas', models.CharField(max_length=20)),
                ('penyampaian_materi', models.CharField(max_length=100)),
                ('media_pembelajaran', models.CharField(max_length=100)),
                ('suasana_belajar', models.CharField(max_length=100)),
                ('tugas', models.CharField(max_length=100)),
                ('kehadiran', models.CharField(max_length=100)),
                ('praktikum', models.CharField(max_length=100)),
                ('uts', models.CharField(max_length=100)),
                ('uas', models.CharField(max_length=100)),
                ('matematika', models.CharField(max_length=100)),
                ('bindo', models.CharField(max_length=100)),
                ('bing', models.CharField(max_length=100)),
                ('pemahaman', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_data_latih',
            },
        ),
    ]
