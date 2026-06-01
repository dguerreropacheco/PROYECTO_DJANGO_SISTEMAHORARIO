from django import forms
from .models import disponibilidad_docente
from .models import docente

class dispo_form(forms.ModelForm):
    class Meta:
        model: disponibilidad_docente
        fields = ['__all__']


class UploadCSVForm(forms.Form):
   # csv_file = forms.FileField(required=False)
    Subir_archivo_excel = forms.FileField(required=False)
