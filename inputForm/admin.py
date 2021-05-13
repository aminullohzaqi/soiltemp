from django.contrib import admin
from .models import SoilTempModel, SoilTempModelCilacap
# Register your models here.

admin.site.register(SoilTempModel)
admin.site.register(SoilTempModelCilacap)