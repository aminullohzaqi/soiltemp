from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from .forms import SoilTempForm
from .models import SoilTempModel
from keras.models import load_model
import tensorflow as tf
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

def inputform(request):
    soiltemp_form = SoilTempForm(request.POST or None)
    
    error = ""
    if request.method == 'POST':
        if soiltemp_form.is_valid():
            suhu                = (float(request.POST.get('suhu')) - 20)/(40-20)
            kelembaban          = (float(request.POST.get('kelembaban')) - 0)/(100-0)
            tekanan             = (float(request.POST.get('tekanan')) - 1000)/(1015-1000)
            radiasi_matahari    = (float(request.POST.get('radiasi_matahari')) - 0)/(1300-0)
            wind_speed          = (float(request.POST.get('wind_speed')) - 0)/(20-0)
            rain_fall           = (float(request.POST.get('rain_fall')) - 0)/(120-0)
            
            cm_5_final  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[0]
            print(cm_5_final)
            
            cm_10_final = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[1]
            print(cm_10_final)
            
            cm_20_final = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[2]
            print(cm_20_final)

            cm_50_final = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[3]
            print(cm_50_final)

            cm_100_final= modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[4]
            print(cm_100_final)
            
            
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
            error = soiltemp_form.errors
    
    context = {
        'judul': 'Input Data',
        'soiltemp_form': soiltemp_form,
        'error': error,
    }
    
    admin_group = Group.objects.get(name='administrator')
    staff_group = Group.objects.get(name='staff_stasiun')
    all_group  = request.user.groups.all()
    
    template_name = None
    if admin_group or staff_group in all_group:
        template_name = 'input/input.html'
    else:
        return redirect('index')
    
    return render(request, template_name, context)