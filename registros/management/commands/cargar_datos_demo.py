from django.core.management.base import BaseCommand
from registros.models import Registro
from datetime import datetime, timedelta, time
import random

class Command(BaseCommand):
    help = 'Genera datos de prueba para los registros de horas.'

    def handle(self, *args, **kwargs):
        # Lista de empleados de prueba
        empleados = [
            'Julio Paredes', 'Muhammad Ali', 'Marvin Herlindo Boche Paredes',
            'Geovanny Sanchez', 'Shamir Waseem', 'Eddy Carrillo',
            'Luis Gutierrez', 'Talal Haider'
        ]

        # Limpia registros anteriores (opcional)
        Registro.objects.all().delete()

        # Día base: hoy menos 6 días (para simular una semana)
        dia_base = datetime.now().date() - timedelta(days=6)

        for i in range(7):  # 7 días
            fecha = dia_base + timedelta(days=i)  # Avanza un día en cada vuelta

            for empleado in empleados:
                # Genera hora de inicio aleatoria entre 7:00 y 9:00
                hora_inicio = time(hour=random.randint(7, 9), minute=0)
                # Genera hora de fin aleatoria entre 15:00 y 17:00
                hora_fin = time(hour=hora_inicio.hour + 8, minute=random.randint(0, 59))

                # Crea el registro
                Registro.objects.create(
                    nombre_empleado=empleado,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )

        self.stdout.write(self.style.SUCCESS('✅ Datos de prueba generados con fechas diferentes por día.'))
