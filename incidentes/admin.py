from django.contrib import admin

from .models import Activo, Empresa, Incidente, Tecnico


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rubro", "tiene_contrato_sla")
    list_filter = ("tiene_contrato_sla",)
    search_fields = ("nombre",)


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especialidad", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "tipo", "codigo_inventario")
    list_filter = ("tipo", "empresa")
    search_fields = ("nombre", "codigo_inventario")


@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "empresa",
        "prioridad",
        "estado",
        "tecnico_asignado",
        "fecha_reporte",
    )
    list_filter = ("prioridad", "estado", "empresa")
    search_fields = ("titulo", "descripcion")
    date_hierarchy = "fecha_reporte"
