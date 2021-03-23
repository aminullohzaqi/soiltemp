import xlwt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from keras.models import load_model
import numpy as np
from inputForm import models
from inputForm import forms

# Create your views here.
#@login_required
def logdata(request) :
    filter_form = forms.FilterForm(request.GET or None)
    filter_data = models.SoilTempModel.objects.order_by('-published')
    #error = ""
    if request.method == 'GET':
        if filter_form.is_valid():
            filter_data=models.SoilTempModel.objects.filter(tanggal__range=[request.GET.get('start_date'),request.GET.get('end_date')])
            
    elif request.method == 'POST':
        print(request.POST)
        if request.POST["download"] == "Download Data":
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Data_Pencarian.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Data')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Tanggal', 'Jam', 'Suhu', 'Kelembaban', 'Tekanan', 'Radiasi Matahari', 'Curah Hujan', 'Kecepatan Angin', 'cm_5', 'cm_10', 'cm_20', 'cm_50', 'cm_100',]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            
            if filter_form.is_valid():
                filter_data=models.SoilTempModel.objects.filter(tanggal__range=[request.GET.get('start_date'),request.GET.get('end_date')])
                rows = filter_data.values_list('tanggal', 'jam', 'suhu', 'kelembaban', 'tekanan', 'radiasi_matahari', 'rain_fall', 'wind_speed', 'cm_5', 'cm_10', 'cm_20', 'cm_50', 'cm_100')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)

                wb.save(response)
                return response
            else:
                filter_data = models.SoilTempModel.objects.order_by('-tanggal')
                rows = filter_data.values_list('tanggal', 'jam', 'suhu', 'kelembaban', 'tekanan', 'radiasi_matahari', 'rain_fall', 'wind_speed', 'cm_5', 'cm_10', 'cm_20', 'cm_50', 'cm_100')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            
    else:
        filter_data = models.SoilTempModel.objects.order_by('-tanggal') 
    
    admin_group = Group.objects.get(name='administrator')
    staff_group = Group.objects.get(name='staff_stasiun')
    visitor_group = Group.objects.get(name='user_visit')
    
    all_group  = request.user.groups.all()

    template_name = None
    sidenav = None

    if request.user.is_authenticated:
        if admin_group in all_group:
            sidenav = "logdata/snippets/sidenav_logdata.html"
            template_name = 'logdata/logdata.html'
        elif staff_group in all_group:
            sidenav = "logdata/snippets/sidenav_logdata.html"
            template_name = 'logdata/logdata.html'
        elif visitor_group in all_group:
            sidenav = "logdata/snippets/sidenav_logdata_user.html"
            template_name = 'logdata/logdata_user.html'
    else:
        return redirect('index')

    context = {
        'judul': 'Log Data',
        'filter_form': filter_form,
        'filter_data': filter_data,
        'all_group': all_group,
        'admin_group': admin_group,
        'staff_group': staff_group,
        'visitor_group': visitor_group,
        'sidenav': sidenav,
    }
    
    return render(request, template_name, context)

@login_required
def delete(request, delete_id):
    models.SoilTempModel.objects.filter(id=delete_id).delete()
    return redirect('logdata')

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

@login_required
def update(request, update_id):
    soiltemp_form = models.SoilTempModel.objects.get(id=update_id)
    
    data = {
        'tanggal'           : soiltemp_form.tanggal,
        'jam'               : soiltemp_form.jam,
        'suhu'              : soiltemp_form.suhu,
        'kelembaban'        : soiltemp_form.kelembaban,
        'tekanan'           : soiltemp_form.tekanan,
        'radiasi_matahari'  : soiltemp_form.radiasi_matahari,
        'wind_speed'        : soiltemp_form.wind_speed,
        'rain_fall'         : soiltemp_form.rain_fall,
    }
    update_form = forms.SoilTempForm(request.POST or None, initial = data, instance=soiltemp_form)
    
    if request.method == 'POST':
        if update_form.is_valid():
            suhu                = (float(request.POST.get('suhu')) - 20)/(40-20)
            kelembaban          = (float(request.POST.get('kelembaban')) - 0)/(100-0)
            tekanan             = (float(request.POST.get('tekanan')) - 1000)/(1015-1000)
            radiasi_matahari    = (float(request.POST.get('radiasi_matahari')) - 0)/(1300-0)
            wind_speed          = (float(request.POST.get('wind_speed')) - 0)/(20-0)
            rain_fall           = (float(request.POST.get('rain_fall')) - 0)/(120-0)

            cm_5_update  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[0]
            print(cm_5_update)
            soiltemp_form.cm_5 = float("{:.2f}".format(cm_5_update))
            
            cm_10_update  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[1]
            print(cm_10_update)
            soiltemp_form.cm_10 = float("{:.2f}".format(cm_10_update))

            cm_20_update  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[2]
            print(cm_20_update)
            soiltemp_form.cm_20 = float("{:.2f}".format(cm_20_update))
            
            cm_50_update  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[3]
            print(cm_50_update)
            soiltemp_form.cm_50 = float("{:.2f}".format(cm_50_update))
            
            cm_100_update  = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)[4]
            print(cm_100_update)
            soiltemp_form.cm_100 = float("{:.2f}".format(cm_100_update))


            update_form.save()
            
            return redirect('logdata')
        
        else :
            error = soiltemp_form.errors
    
    context = {
        'judul': 'Edit Data',
        'update_form': update_form,
    }
    
    return render(request, 'logdata/update.html', context)