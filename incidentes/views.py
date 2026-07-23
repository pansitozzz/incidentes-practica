from django.db.models import Avg, Count, ExpressionWrapper, F, DurationField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Incidente
from .priority import calcular_score, ordenar_por_prioridad


def dashboard(request):
    incidentes = Incidente.objects.select_related("empresa").all()
    context = {
        "total_incidentes": incidentes.count(),
        "abiertos": incidentes.exclude(estado__in=["resuelto", "cerrado"]).count(),
        "resueltos": incidentes.filter(estado__in=["resuelto", "cerrado"]).count(),
    }
    return render(request, "incidentes/dashboard.html", context)


def datos_dashboard(request):
    """Datos agregados en JSON para alimentar los gráficos de Chart.js."""
    incidentes = Incidente.objects.all()

    por_prioridad = {
        codigo: incidentes.filter(prioridad=codigo).count()
        for codigo, _ in Incidente.PRIORIDAD_CHOICES
    }
    por_estado = {
        codigo: incidentes.filter(estado=codigo).count()
        for codigo, _ in Incidente.ESTADO_CHOICES
    }

    resueltos = incidentes.filter(
        estado__in=["resuelto", "cerrado"], fecha_resolucion__isnull=False
    ).annotate(
        duracion=ExpressionWrapper(
            F("fecha_resolucion") - F("fecha_reporte"), output_field=DurationField()
        )
    )
    duraciones_horas = [r.duracion.total_seconds() / 3600 for r in resueltos]
    promedio_horas = round(sum(duraciones_horas) / len(duraciones_horas), 1) if duraciones_horas else 0

    return JsonResponse(
        {
            "por_prioridad": por_prioridad,
            "por_estado": por_estado,
            "tiempo_promedio_resolucion_horas": promedio_horas,
        }
    )


def lista_incidentes(request):
    incidentes = list(Incidente.objects.select_related("empresa", "tecnico_asignado").all())
    incidentes_ordenados = ordenar_por_prioridad(incidentes)
    for incidente in incidentes_ordenados:
        incidente.score = calcular_score(incidente)
    return render(request, "incidentes/lista_incidentes.html", {"incidentes": incidentes_ordenados})


def detalle_incidente(request, pk):
    incidente = get_object_or_404(Incidente, pk=pk)
    incidente.score = calcular_score(incidente)
    return render(request, "incidentes/detalle_incidente.html", {"incidente": incidente})


def reporte_incidente_pdf(request, pk):
    incidente = get_object_or_404(Incidente, pk=pk)
    incidente.score = calcular_score(incidente)
    html_string = render_to_string(
        "incidentes/reports/reporte_incidente.html",
        {"incidente": incidente, "generado_en": timezone.now()},
    )
    return _html_a_pdf(html_string, f"incidente-{incidente.pk}.pdf")


def reporte_resumen_pdf(request):
    incidentes = list(Incidente.objects.select_related("empresa", "tecnico_asignado").all())
    incidentes_ordenados = ordenar_por_prioridad(incidentes)
    for incidente in incidentes_ordenados:
        incidente.score = calcular_score(incidente)

    html_string = render_to_string(
        "incidentes/reports/reporte_resumen.html",
        {"incidentes": incidentes_ordenados, "generado_en": timezone.now()},
    )
    return _html_a_pdf(html_string, "resumen-incidentes.pdf")


def _html_a_pdf(html_string, nombre_archivo):
    """Convierte un HTML renderizado a PDF usando WeasyPrint.

    La importación de weasyprint se hace dentro de la función para que el
    resto del proyecto (y los tests que no generan PDFs) no requieran tener
    instaladas sus dependencias nativas (Pango/Cairo) para funcionar.
    """
    from weasyprint import HTML

    pdf_bytes = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nombre_archivo}"'
    return response
