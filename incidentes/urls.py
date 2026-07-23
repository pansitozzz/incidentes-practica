from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("incidentes/", views.lista_incidentes, name="lista_incidentes"),
    path("incidentes/<int:pk>/", views.detalle_incidente, name="detalle_incidente"),
    path("incidentes/<int:pk>/reporte.pdf", views.reporte_incidente_pdf, name="reporte_incidente_pdf"),
    path("reportes/resumen.pdf", views.reporte_resumen_pdf, name="reporte_resumen_pdf"),
    path("api/datos-dashboard/", views.datos_dashboard, name="datos_dashboard"),
]
