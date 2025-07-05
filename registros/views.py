from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistroForm
from datetime import date
from .models import Registro
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .pdf import generar_pdf_reporte_semanal


def registrar_horas(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.fecha = date.today()  # ✅ asignación desde servidor
            registro.save()
            return redirect('lista_registros')
    else:
        # Pasa la fecha al formulario
        form = RegistroForm(initial={'fecha': date.today()})

    return render(request, 'registros/formulario.html', {
        'form': form,
        'today': date.today()
    })

def lista_registros(request):
    registros = Registro.objects.all().order_by('-fecha')
    hoy = date.today()

    return render(request, 'registros/lista.html', {
        'registros': registros,
        'hoy': hoy
    })


def editar_registro(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id)

    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_registros')
    else:
        form = RegistroForm(instance=registro)

    return render(request, 'registros/formulario.html', {
        'form': form,
        'today': registro.fecha  # usamos la fecha original
    })



def reporte_semanal(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    registros = []
    resumen = {}

    def formatear_horas(decimal_horas):
        if decimal_horas is None:
            return "0h 0min"
        horas = int(decimal_horas)
        minutos = int((decimal_horas - horas) * 60)
        return f"{horas}h {minutos}min"

    if fecha_inicio and fecha_fin:
        registros = Registro.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        resumen_queryset = registros.values('nombre_empleado').annotate(
            total_horas=Sum('total_horas')
        )

        resumen = {
            r['nombre_empleado']: {
                'raw': r['total_horas'],
                'formateado': formatear_horas(r['total_horas'])
            }
            for r in resumen_queryset
        }

    return render(request, 'registros/reporte_semanal.html', {
        'registros': registros,
        'resumen': resumen,
        'inicio': fecha_inicio,
        'fin': fecha_fin
    })




def exportar_reporte_semanal_pdf(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return HttpResponse("Debes proporcionar un rango de fechas", status=400)

    return generar_pdf_reporte_semanal(fecha_inicio, fecha_fin)



