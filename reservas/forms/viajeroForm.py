from django import forms
from django.core.exceptions import ValidationError
from ..models import Viajero

class ViajeroForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'id':'nombre'}),
                             label="Nombre")
    ci = forms.CharField(max_length=11, min_length=11, required=True, widget=forms.TextInput(attrs={'class': 'form-control my-2', 'id':'ci'}),
                         label="Carnet de Identidad")

    class Meta:
        model = Viajero
        fields = ['nombre', 'ci']
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre[0].isupper():
            raise ValidationError("El nombre debe comenzar con una letra mayúscula.")
        return nombre

    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        if not ci.isdigit():
            raise ValidationError("El Carnet de Identidad debe contener solo números.")
        return ci