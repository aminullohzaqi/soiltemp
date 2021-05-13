from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from inputForm import models
from keras.models import load_model
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
import json

# Create your views here.

def modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall):
    model = load_model('ml_model_36_9_27.h5')
    model2= load_model('ml_model_(50_100)_11_42_46_17.h5')

    X = [[suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall]]

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

def AWS():
    tgl = datetime.now()
    tgl_mulai = tgl - timedelta(days=1)
    tgl_selesai = tgl.strftime("%Y")+"-"+tgl.strftime("%m")+"-"+tgl.strftime("%d")
    kode_stasiun = '5000000060' #'1000000002' #'5000000060' #'5000000064'

    range = pd.date_range(start=tgl_mulai,end=tgl_selesai)
    try:
        for day in range:
            tanggal     = day + timedelta(1)
            jam_before  = day - timedelta(hours=7, minutes=10)
            jam_now     = day - timedelta(hours=7)
            print("Download data : ", jam_before, " sd ", jam_now)

            r = requests.get('http://202.90.199.132/aws-new/data/station/'+ kode_stasiun + '/' + 
                            str(tanggal.date()) + '/' + str(jam_before.strftime("%H:%M:%S")) + '/' + 
                            str(tanggal.date()) +'/' + str(jam_now.strftime("%H:%M:%S"))
                            )
            data = json.loads(r.text)
            df = pd.DataFrame(data['aaData'])
            time = df.iloc[-1:,0:1].values
            par = df.iloc[-1:,1:8].values
            par = par.astype(np.float)
            
            time = [x[:-3] for x in time[:,0]]
            time = ''.join(time)
            hour_time   = time[11:]
            year_time   = time[6:10]
            month_time  = time[3:5]
            date_time   = time[:2]
            fix_time    = year_time+"-"+month_time+"-"+date_time
            
            time = np.array([fix_time, hour_time])
            time = time.reshape(1,2)

        suhu_db                = float(''.join(str(e) for e in par[:,2]))
        kelembaban_db          = float(''.join(str(e) for e in par[:,3]))
        tekanan_db             = float(''.join(str(e) for e in par[:,4]))
        radiasi_matahari_db    = float(''.join(str(e) for e in par[:,6]))
        wind_speed_db          = float(''.join(str(e) for e in par[:,0]))
        rain_fall_db           = float(''.join(str(e) for e in par[:,5]))    

        par[:,0] = (par[:,2] - 20)/(40-20)
        par[:,1] = (par[:,3] - 0)/(100-0)
        par[:,2] = (par[:,4] - 1000)/(1015-1000)
        par[:,3] = (par[:,6] - 0)/(1300-0)  
        par[:,4] = (par[:,0] - 0)/(20-0)
        par[:,5] = (par[:,5] - 0)/(120-0)

        suhu                = float(''.join(str(e) for e in par[:,0]))
        kelembaban          = float(''.join(str(e) for e in par[:,1]))
        tekanan             = float(''.join(str(e) for e in par[:,2]))
        radiasi_matahari    = float(''.join(str(e) for e in par[:,3]))
        wind_speed          = float(''.join(str(e) for e in par[:,4]))
        rain_fall           = float(''.join(str(e) for e in par[:,5]))

        cm_final    = modelPrediction(suhu, kelembaban, tekanan, radiasi_matahari, wind_speed, rain_fall)
        cm_0_final  = cm_final[0]
        cm_2_final  = cm_final[1]
        cm_10_final = cm_final[2]
        cm_20_final = cm_final[3]
        cm_50_final = cm_final[4]

        models.SoilTempModelCilacap.objects.create(
            tanggal     = fix_time,
            jam         = hour_time,
            suhu        = float("{:.2f}".format(suhu_db)),
            kelembaban  = float("{:.2f}".format(kelembaban_db)),
            tekanan     = float("{:.2f}".format(tekanan_db)),
            radiasi_matahari = float("{:.2f}".format(radiasi_matahari_db)),
            wind_speed  = float("{:.2f}".format(wind_speed_db)),
            rain_fall   = float("{:.2f}".format(rain_fall_db)),
            cm_0        = float("{:.2f}".format(cm_0_final)),
            cm_2        = float("{:.2f}".format(cm_2_final)),
            cm_10       = float("{:.2f}".format(cm_10_final)),
            cm_20       = float("{:.2f}".format(cm_20_final)),
            cm_50       = float("{:.2f}".format(cm_50_final)),
        )
    
    except:
        siteOffline = 'Site Offline'
        print("Site Offline")
        return siteOffline
        #raise


def graph(request) :
    admin_group     = Group.objects.get(name='administrator')
    staklim_group   = Group.objects.get(name='staff_staklim')
    stamet_group    = Group.objects.get(name='staff_stamet')
    
    all_group  = request.user.groups.all()

    sidenav = None
    template_name = None
    error = None

    if request.user.is_authenticated:
        if admin_group in all_group:
            template_name = "dashboard/graphstamet.html"
            sidenav = "dashboard/snippets/sidenav_dashboard.html"

        elif staklim_group in all_group:
            template_name = "dashboard/graphstaklim.html"
            sidenav = "dashboard/snippets/sidenav_dashboard.html"

            gauge_data = models.SoilTempModel.objects.order_by('-published')[0:1]
            graph_data = models.SoilTempModel.objects.order_by('-published')[:20:-1]

        elif stamet_group in all_group:
            template_name = "dashboard/graphstamet.html"
            sidenav = "dashboard/snippets/sidenav_dashboard.html"

            AWS()
            
            gauge_data = models.SoilTempModelCilacap.objects.order_by('-published')[0:1]
            gauge_data2 = models.SoilTempModelCilacap.objects.order_by('-published')[1:2]

            if gauge_data[0].jam == gauge_data2[0].jam:
                models.SoilTempModelCilacap.objects.order_by('-published').first().delete()

            graph_data = models.SoilTempModelCilacap.objects.order_by('-published')[:20:-1]

    else:
        return redirect('index')

    context = {
        'judul': 'Graph Data',
        'graph_data': graph_data,
        'gauge_data': gauge_data,
        'all_group': all_group,
        'admin_group': admin_group,
        'staklim_group': staklim_group,
        'stamet_group': stamet_group,
        'sidenav': sidenav,
        'error': error,
    }
    return render(request, template_name, context)