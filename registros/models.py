from django.db import models
from datetime import datetime, timedelta

class Registro(models.Model):
    EMPLEADOS_CHOICES = [
        ('Julio Paredes', 'Julio Paredes'),
        ('Muhammad Ali', 'Muhammad Ali'),
        ('Marvin Herlindo Boche Paredes', 'Marvin Herlindo Boche Paredes'),
        ('Geovanny Sanchez', 'Geovanny Sanchez'),
        ('Shamir Waseem', 'Shamir Waseem'),
        ('Eddy Carrillo', 'Eddy Carrillo'),
        ('Luis Gutierrez', 'Luis Gutierrez'),
        ('Talal Haider', 'Talal Haider'),
        
        # puedes agregar más aquí
    ]

    nombre_empleado = models.CharField(max_length=100, choices=EMPLEADOS_CHOICES)
    fecha = models.DateField(auto_now_add=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    total_horas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.hora_inicio and self.hora_fin:
            inicio = datetime.combine(datetime.today(), self.hora_inicio)
            fin = datetime.combine(datetime.today(), self.hora_fin)

            if fin < inicio:
                fin += timedelta(days=1)  # caso de turno nocturno

            delta = fin - inicio
            self.total_horas = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_empleado} - {self.fecha}"
    
    def total_horas_formateado(self):
        if self.hora_inicio and self.hora_fin:
            inicio = datetime.combine(datetime.today(), self.hora_inicio)
            fin = datetime.combine(datetime.today(), self.hora_fin)
            if fin < inicio:
                fin += timedelta(days=1)
            total_segundos = (fin - inicio).total_seconds()
            horas = int(total_segundos // 3600)
            minutos = int((total_segundos % 3600) // 60)
            return f"{horas}h {minutos}min"
        return ""
    