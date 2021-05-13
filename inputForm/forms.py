from django import forms
from .models import SoilTempModel, SoilTempModelCilacap

class SoilTempForm(forms.ModelForm):
    class Meta:
        model = SoilTempModel
        fields = [
            'tanggal',
            'jam',
            'suhu',
            'kelembaban',
            'tekanan',
            'radiasi_matahari',
            'wind_speed',
            'rain_fall',
        ]
        widgets = {
            
            'tanggal': forms.DateInput(
                format=('%m/%d/%Y'), 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'Select a date', 
                    'type':'date',
                }
            ),
            
            'jam': forms.Select( 
                attrs={
                    'class': 'form-control col-sm-10',
                }
            ),
            
            'suhu': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'°C',
                }
            ),
            
            'kelembaban': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'%',
                }
            ),
            
            'tekanan': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'HPa',
                }
            ),
            
            'radiasi_matahari': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'W/m2',
                }
            ),
            
            'wind_speed': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'m/s',
                }
            ),
            
            'rain_fall': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'mm',
                }
            ),
           
        }

class SoilTempFormCilacap(forms.ModelForm):
    class Meta:
        model = SoilTempModelCilacap
        fields = [
            'tanggal',
            'jam',
            'suhu',
            'kelembaban',
            'tekanan',
            'radiasi_matahari',
            'wind_speed',
            'rain_fall',
        ]
        widgets = {
            
            'tanggal': forms.DateInput(
                format=('%m/%d/%Y'), 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'Select a date', 
                    'type':'date',
                }
            ),
            
            'jam': forms.Select( 
                attrs={
                    'class': 'form-control col-sm-10',
                }
            ),
            
            'suhu': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'°C',
                }
            ),
            
            'kelembaban': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'%',
                }
            ),
            
            'tekanan': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'HPa',
                }
            ),
            
            'radiasi_matahari': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'W/m2',
                }
            ),
            
            'wind_speed': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'m/s',
                }
            ),
            
            'rain_fall': forms.NumberInput( 
                attrs={
                    'class': 'form-control col-sm-10',
                    'placeholder':'mm',
                }
            ),
           
        }

        
class FilterForm(forms.Form):
    start_date  = forms.DateField(
        widget=forms.DateInput(
            attrs={
            'class': 'form-control',
            'placeholder':'Select a date', 
            'type':'date',
            }
        )
    )
    end_date    = forms.DateField(
        widget=forms.DateInput(
            attrs={
            'class': 'form-control',
            'placeholder':'Select a date', 
            'type':'date',
            }
        )
    )