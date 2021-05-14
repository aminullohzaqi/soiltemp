from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from .forms import SoilTempForm, SoilTempFormCilacap
from .models import SoilTempModel, SoilTempModelCilacap
from keras.models import load_model
import numpy as np

# Create your views here.
def modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall):
    model = load_model('ml_model_36_9_27.h5')
    model2= load_model('ml_model_(50_100)_11_42_46_17.h5')

    X = [[suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall]]

    print(X)
    pred = model.predict(X)
    pred = np.array_split(pred[0], 3)

    pred2= model2.predict(X)
    pred2= np.array_split(pred2[0], 2)

    cm_5    = (float(pred[0])*(50-20))+20
    cm_10   = (float(pred[1])*(50-20))+20
    cm_20   = (float(pred[2])*(50-20))+20
    cm_50   = (float(pred2[0])*(50-20))+20
    cm_100  = (float(pred2[1])*(50-20))+20

    return cm_5, cm_10, cm_20, cm_50, cm_100

def modelPredictionCilacap(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall):
    model = load_model('ml_model_cilacap_20_49_27_21.h5')

    X = [[suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall]]

    print(X)
    pred = model.predict(X)
    pred = np.array_split(pred[0], 5)

    cm_0    = (float(pred[0])*(50-20))+20
    cm_2    = (float(pred[1])*(50-20))+20
    cm_10   = (float(pred[2])*(50-20))+20
    cm_20   = (float(pred[3])*(50-20))+20
    cm_50   = (float(pred[4])*(50-20))+20

    return cm_0, cm_2, cm_10, cm_20, cm_50

def inputform(request):
    admin_group = Group.objects.get(name='administrator')
    staklim_group = Group.objects.get(name='staff_staklim')
    stamet_group = Group.objects.get(name='staff_stamet')
    all_group  = request.user.groups.all()
    
    template_name = None
    soiltemp_form_staklim = None
    soiltemp_form_stamet  = None
    if request.user.is_authenticated:
        if stamet_group in all_group:
            template_name = 'input/inputstamet.html'

            soiltemp_form_stamet = SoilTempFormCilacap(request.POST or None)
            error = ""
            if request.method == 'POST':
                if soiltemp_form_stamet.is_valid():
                    suhu                = (float(request.POST.get('suhu')) - 20)/(40-20)
                    kelembaban          = (float(request.POST.get('kelembaban')) - 0)/(100-0)
                    tekanan             = (float(request.POST.get('tekanan')) - 1000)/(1015-1000)
                    radiasi_matahari    = (float(request.POST.get('radiasi_matahari')) - 0)/(1300-0)
                    wind_speed          = (float(request.POST.get('wind_speed')) - 0)/(20-0)
                    rain_fall           = (float(request.POST.get('rain_fall')) - 0)/(120-0)
                    
                    cm_final    = modelPredictionCilacap(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)
                    cm_0_final  = cm_final[0]
                    cm_2_final  = cm_final[1]
                    cm_10_final = cm_final[2]
                    cm_20_final = cm_final[3]
                    cm_50_final = cm_final[4]
                    
                    SoilTempModelCilacap.objects.create(
                        tanggal     = request.POST.get('tanggal'),
                        jam         = request.POST.get('jam'),
                        suhu        = request.POST.get('suhu'),
                        kelembaban  = request.POST.get('kelembaban'),
                        tekanan     = request.POST.get('tekanan'),
                        radiasi_matahari = request.POST.get('radiasi_matahari'),
                        wind_speed  = request.POST.get('wind_speed'),
                        rain_fall   = request.POST.get('rain_fall'),
                        cm_0        = float("{:.2f}".format(cm_0_final)),
                        cm_2        = float("{:.2f}".format(cm_2_final)),
                        cm_10       = float("{:.2f}".format(cm_10_final)),
                        cm_20       = float("{:.2f}".format(cm_20_final)),
                        cm_50       = float("{:.2f}".format(cm_50_final)),
                    )
                    #contact_form.save()
                    return redirect('dashboard')
                
                else :
                    error = soiltemp_form_stamet.errors

        elif staklim_group in all_group:
            template_name = 'input/inputstaklim.html'

            soiltemp_form_staklim = SoilTempForm(request.POST or None)
            error = ""
            if request.method == 'POST':
                if soiltemp_form_staklim.is_valid():
                    suhu                = (float(request.POST.get('suhu')) - 20)/(40-20)
                    kelembaban          = (float(request.POST.get('kelembaban')) - 0)/(100-0)
                    tekanan             = (float(request.POST.get('tekanan')) - 1000)/(1015-1000)
                    radiasi_matahari    = (float(request.POST.get('radiasi_matahari')) - 0)/(1300-0)
                    wind_speed          = (float(request.POST.get('wind_speed')) - 0)/(20-0)
                    rain_fall           = (float(request.POST.get('rain_fall')) - 0)/(120-0)
                    
                    cm_final    = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)
                    cm_5_final  = cm_final[0]
                    cm_10_final = cm_final[1]
                    cm_20_final = cm_final[2]
                    cm_50_final = cm_final[3]
                    cm_100_final= cm_final[4]
                    
                    SoilTempModel.objects.create(
                        tanggal     = request.POST.get('tanggal'),
                        jam         = request.POST.get('jam'),
                        suhu        = request.POST.get('suhu'),
                        kelembaban  = request.POST.get('kelembaban'),
                        tekanan     = request.POST.get('tekanan'),
                        radiasi_matahari = request.POST.get('radiasi_matahari'),
                        wind_speed  = request.POST.get('wind_speed'),
                        rain_fall   = request.POST.get('rain_fall'),
                        cm_5        = float("{:.2f}".format(cm_5_final)),
                        cm_10       = float("{:.2f}".format(cm_10_final)),
                        cm_20       = float("{:.2f}".format(cm_20_final)),
                        cm_50       = float("{:.2f}".format(cm_50_final)),
                        cm_100      = float("{:.2f}".format(cm_100_final)),
                    )
                    #contact_form.save()
                    return redirect('dashboard')
                
                else :
                    error = soiltemp_form_staklim.errors

        else:
            return redirect('index')

    context = {
        'judul': 'Sltera | Input',
        'soiltemp_form_staklim': soiltemp_form_staklim,
        'soiltemp_form_stamet': soiltemp_form_stamet,
        'error': error,
    }
    
    return render(request, template_name, context)