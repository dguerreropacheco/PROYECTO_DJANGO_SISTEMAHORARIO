from django import forms
from .models import ambiente

class dispo_form(forms.ModelForm):
    class Meta:
        model: ambiente
        fields = ['__all__']


class UploadCSVForm(forms.Form):
 #   Subir_archivo_csv = forms.FileField(required=False)
    Subir_archivo_excel = forms.FileField(required=False)