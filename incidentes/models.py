from django.db import models
from django.utils import timezone


class Empresa(models.Model):
    """Cliente ficticio al que pertenecen los equipos e incidentes."""

    nombre = models.CharField(max_length=150)
    rubro = models.CharField(max_length=100, blank=True)
    tiene_contrato_sla = models.BooleanField(
        default=False,
        verbose_name="Tiene contrato SLA",
        help_text="Si la empresa cuenta con un contrato de nivel de servicio activo.",
    )
    contacto_nombre = models.CharField(max_length=150, blank=True)
    contacto_email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Tecnico(models.Model):
    """Técnico ficticio encargado de atender incidentes."""

    nombre = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Activo(models.Model):
    """Equipo o activo técnico que puede presentar incidentes."""

    TIPO_CHOICES = [
        ("servidor", "Servidor"),
        ("pc", "Computadora"),
        ("impresora", "Impresora"),
        ("red", "Equipo de red"),
        ("otro", "Otro"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="activos")
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="otro")
    codigo_inventario = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Activo"
        verbose_name_plural = "Activos"
        ordering = ["empresa__nombre", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"


class Incidente(models.Model):
    """Incidente técnico reportado sobre un activo de una empresa."""

    PRIORIDAD_CHOICES = [
        ("P1", "P1 - Crítico"),
        ("P2", "P2 - Alto"),
        ("P3", "P3 - Medio"),
        ("P4", "P4 - Bajo"),
    ]

    ESTADO_CHOICES = [
        ("abierto", "Abierto"),
        ("en_progreso", "En progreso"),
        ("resuelto", "Resuelto"),
        ("cerrado", "Cerrado"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="incidentes")
    activo = models.ForeignKey(
        Activo, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidentes"
    )
    tecnico_asignado = models.ForeignKey(
        Tecnico, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidentes"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    prioridad = models.CharField(max_length=2, choices=PRIORIDAD_CHOICES, default="P3")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="abierto")
    fecha_reporte = models.DateTimeField(default=timezone.now)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"
        ordering = ["-fecha_reporte"]

    def __str__(self):
        return f"[{self.prioridad}] {self.titulo}"

    @property
    def esta_resuelto(self):
        return self.estado in ("resuelto", "cerrado")

    @property
    def tiempo_abierto(self):
        """Duración desde el reporte hasta la resolución (o hasta ahora si sigue abierto)."""
        fin = self.fecha_resolucion or timezone.now()
        return fin - self.fecha_reporte

    @property
    def horas_abierto(self):
        return round(self.tiempo_abierto.total_seconds() / 3600, 1)

    @property
    def score_prioridad(self):
        """Puntaje de priorización calculado. Ver incidentes.priority.calcular_score."""
        from .priority import calcular_score

        return calcular_score(self)
