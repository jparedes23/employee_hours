from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from decimal import Decimal
from .models import Registro
from django.db.models import Sum

def formatear_decimal_a_horas(decimal_horas):
    if not decimal_horas:
        return "0h 0min"
    total_min = int(decimal_horas * 60)
    horas = total_min // 60
    minutos = total_min % 60
    return f"{horas}h {minutos}min"

def generar_pdf_reporte_semanal(fecha_inicio, fecha_fin):
    registros = Registro.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

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

    html_string = render_to_string('pdf_template.html', {
        'inicio': fecha_inicio,
        'fin': fecha_fin,
        'resumen': resumen
    })

    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as output:
        HTML(string=html_string).write_pdf(output.name)
        output.seek(0)
        pdf = output.read()

    return HttpResponse(pdf, content_type='application/pdf')