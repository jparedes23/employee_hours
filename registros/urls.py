from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_horas, name='registrar_horas'),
    path('lista/', views.lista_registros, name='lista_registros'),
    
    path('reporte-semanal/pdf/', views.exportar_pdf, name='reporte_semanal_pdf'),
]