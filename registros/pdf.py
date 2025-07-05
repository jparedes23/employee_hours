from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Registro
from django.db.models import Sum
from decimal import Decimal

def generar_pdf_reporte_semanal(fecha_inicio, fecha_fin):
    registros = Registro.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    
    def formatear_decimal_a_horas(decimal_horas):
        if not decimal_horas:
            return "0h 0min"
        total_min = int(decimal_horas * 60)
        horas = total_min // 60
        minutos = total_min % 60
        return f"{horas}h {minutos}min"

    resumen_query = registros.values('nombre_empleado').annotate(total_horas=Sum('total_horas'))

    resumen = {
        r['nombre_empleado']: {
            'raw': r['total_horas'],
            'formateado': formatear_decimal_a_horas(r['total_horas']),
            'estado': (
                "Incompleto" if r['total_horas'] < Decimal(40) else
                "Exceso" if r['total_horas'] > Decimal(40) else
                "Completo"
            )
        }
        for r in resumen_query
    }