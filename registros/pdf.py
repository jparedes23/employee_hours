from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Registro
from django.db.models import Sum

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