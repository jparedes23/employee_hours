from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from datetime import datetime
from .models import Registro
from django.db.models import Sum


def formatear_decimal_a_horas(decimal_horas):
    if decimal_horas is None:
        return "0h 0min"
    horas = int(decimal_horas)
    minutos = int((decimal_horas - horas) * 60)
    return f"{horas}h {minutos}min"


def generar_pdf_reporte_semanal(fecha_inicio_str, fecha_fin_str):
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponse("Fechas inválidas", status=400)

    registros = Registro.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    resumen_query = registros.values('nombre_empleado').annotate(total_horas=Sum('total_horas'))

    resumen = {
        r['nombre_empleado']: {
            'formateado': formatear_decimal_a_horas(r['total_horas']),
            'estado': (
                "Incompleto" if r['total_horas'] < 40 else
                "Exceso" if r['total_horas'] > 40 else
                "Completo"
            )
        }
        for r in resumen_query
    }

    template = get_template('registros/reporte_pdf.html')
    html = template.render({
        'inicio': fecha_inicio,
        'fin': fecha_fin,
        'resumen': resumen
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_semanal.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response