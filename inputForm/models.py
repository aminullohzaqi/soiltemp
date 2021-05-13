from django.db import models
from .validators import *

# Create your models here.

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
    suhu        = models.FloatField(
        blank=False,
        validators = [validate_temp]
    )
    kelembaban  = models.FloatField(
        blank=False,
        validators = [validate_humidity]
    )
    tekanan     = models.FloatField(
        blank=False,
        validators = [validate_press]
    )
    radiasi_matahari = models.FloatField(
        blank=False,
        validators = [validate_SR]
    )
    wind_speed  = models.FloatField(
        blank=False,
        validators = [validate_WS]
    )
    rain_fall   = models.FloatField(
        blank=False,
        validators = [validate_rainfall]
    )
    cm_5        = models.FloatField(blank=False)
    cm_10       = models.FloatField(blank=False)
    cm_20       = models.FloatField(blank=False)
    cm_50       = models.FloatField(blank=False)
    cm_100      = models.FloatField(blank=False)
    
    published   = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)

    
class SoilTempModelCilacap(models.Model):
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
    suhu        = models.FloatField(
        blank=False,
        validators = [validate_temp]
    )
    kelembaban  = models.FloatField(
        blank=False,
        validators = [validate_humidity]
    )
    tekanan     = models.FloatField(
        blank=False,
        validators = [validate_press]
    )
    radiasi_matahari = models.FloatField(
        blank=False,
        validators = [validate_SR]
    )
    wind_speed  = models.FloatField(
        blank=False,
        validators = [validate_WS]
    )
    rain_fall   = models.FloatField(
        blank=False,
        validators = [validate_rainfall]
    )
    cm_0        = models.FloatField(blank=False)
    cm_2        = models.FloatField(blank=False)
    cm_10       = models.FloatField(blank=False)
    cm_20       = models.FloatField(blank=False)
    cm_50       = models.FloatField(blank=False)
    
    published   = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)