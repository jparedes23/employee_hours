from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Registro
from django.db.models import Sum
from decimal import Decimal

def generar_pdf_reporte_semanal(fecha_inicio, fecha_fin):
    # ✅ Convertir strings a objetos date
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    registros = Registro.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    resumen_queryset = registros.values('nombre_empleado').annotate(
        total_horas=Sum('total_horas')
    )
    resumen = {
        r['nombre_empleado']: r['total_horas']
        for r in resumen_queryset
    }

    template = get_template('registros/reporte_pdf.html')
    html = template.render({
        'resumen': resumen,
        'inicio': fecha_inicio,
        'fin': fecha_fin
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_semanal.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response



def formatear_decimal_a_horas(decimal_horas):
    if not decimal_horas:
        return "0h 0min"
    total_min = int(decimal_horas * 60)
    horas = total_min // 60
    minutos = total_min % 60
    return f"{horas}h {minutos}min"

resumen = registros.values('nombre_empleado').annotate(total_horas=Sum('total_horas'))

# Armar estructura con formato para el template
resumen_formateado = {
    r['nombre_empleado']: {
        'raw': r['total_horas'],
        'formateado': formatear_decimal_a_horas(r['total_horas']),
        'estado': (
            "Incompleto" if r['total_horas'] < Decimal(40) else
            "Exceso" if r['total_horas'] > Decimal(40) else
            "Completo"
        )
    }
    for r in resumen
}