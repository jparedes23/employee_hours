from django import forms
from .models import Registro

# Lista predefinida de empleados
NOMBRES_EMPLEADOS = [
    ('Julio Paredes', 'Julio Paredes'),
        ('Muhammad Ali', 'Muhammad Ali'),
        ('Marvin Herlindo Boche Paredes', 'Marvin Herlindo Boche Paredes'),
        ('Geovanny Sanchez', 'Geovanny Sanchez'),
        ('Shamir Waseem', 'Shamir Waseem'),
        ('Eddy Carrillo', 'Eddy Carrillo'),
        ('Luis Gutierrez', 'Luis Gutierrez'),
        ('Talal Haider', 'Talal Haider'),
]

from django import forms
from .models import Registro
from datetime import date

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        exclude = []  # ✅ No excluir fecha
        labels = {
            'nombre_empleado': 'Employee Name',
            'hora_inicio': 'Start Time',
            'hora_fin': 'End Time',
            'fecha': 'Date',
        }
        widgets = {
            'nombre_empleado': forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get("nombre_empleado")
        fecha = cleaned_data.get("fecha")

        if empleado and fecha:
            existe = Registro.objects.filter(nombre_empleado=empleado, fecha=fecha)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)

            if existe.exists():
                raise forms.ValidationError(f"{empleado} already has a record for {fecha}.")

        return cleaned_data
