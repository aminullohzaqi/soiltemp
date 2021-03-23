from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_name(value):
    nama_input = value
    if nama_input == "ucok":
        message = "Maaf, " + nama_input + " dilarang Posting"
        raise ValidationError(message)

class SoilTempModel(models.Model):
    tanggal     = models.DateField()
    JAM         = {
        ('00:00', '00:00'),
        ('03:00', '03:00'),
        ('06:00', '06:00'),
        ('09:00', '09:00'),
        ('12:00', '12:00'),
    }
    jam         = models.CharField(
        max_length = 10,
        choices = JAM,
        default = '00:00',
    )
    suhu        = models.FloatField(blank=False)
    kelembaban  = models.FloatField(blank=False)
    tekanan     = models.FloatField(blank=False)
    radiasi_matahari = models.FloatField(blank=False)
    wind_speed  = models.FloatField(blank=False)
    rain_fall   = models.FloatField(blank=False)
    cm_5        = models.FloatField(blank=False)
    cm_10       = models.FloatField(blank=False)
    cm_20       = models.FloatField(blank=False)
    cm_50       = models.FloatField(blank=False)
    cm_100      = models.FloatField(blank=False)
    
    published   = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)
    