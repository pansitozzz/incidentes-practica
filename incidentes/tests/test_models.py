from datetime import timedelta

import pytest
from django.utils import timezone

from incidentes.models import Empresa, Incidente


@pytest.mark.django_db
def test_incidente_str_incluye_prioridad_y_titulo():
    empresa = Empresa.objects.create(nombre="Empresa de Prueba")
    incidente = Incidente.objects.create(
        empresa=empresa, titulo="Falla de ejemplo", prioridad="P2"
    )

    assert str(incidente) == "[P2] Falla de ejemplo"


@pytest.mark.django_db
def test_esta_resuelto_true_para_resuelto_y_cerrado():
    empresa = Empresa.objects.create(nombre="Empresa de Prueba")
    resuelto = Incidente.objects.create(empresa=empresa, titulo="A", estado="resuelto")
    cerrado = Incidente.objects.create(empresa=empresa, titulo="B", estado="cerrado")
    abierto = Incidente.objects.create(empresa=empresa, titulo="C", estado="abierto")

    assert resuelto.esta_resuelto is True
    assert cerrado.esta_resuelto is True
    assert abierto.esta_resuelto is False


@pytest.mark.django_db
def test_horas_abierto_usa_fecha_resolucion_si_existe():
    empresa = Empresa.objects.create(nombre="Empresa de Prueba")
    fecha_reporte = timezone.now() - timedelta(hours=10)
    fecha_resolucion = fecha_reporte + timedelta(hours=4)

    incidente = Incidente.objects.create(
        empresa=empresa,
        titulo="Incidente con resolución",
        estado="resuelto",
        fecha_reporte=fecha_reporte,
        fecha_resolucion=fecha_resolucion,
    )

    assert incidente.horas_abierto == 4.0
