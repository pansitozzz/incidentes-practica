from datetime import timedelta

import pytest
from django.utils import timezone

from incidentes.models import Empresa, Incidente
from incidentes.priority import calcular_score, ordenar_por_prioridad


@pytest.fixture
def empresa_sin_sla(db):
    return Empresa.objects.create(nombre="Empresa Sin SLA", tiene_contrato_sla=False)


@pytest.fixture
def empresa_con_sla(db):
    return Empresa.objects.create(nombre="Empresa Con SLA", tiene_contrato_sla=True)


def crear_incidente(empresa, prioridad, horas_abierto, estado="abierto"):
    fecha_reporte = timezone.now() - timedelta(hours=horas_abierto)
    return Incidente.objects.create(
        empresa=empresa,
        titulo=f"Incidente {prioridad}",
        prioridad=prioridad,
        estado=estado,
        fecha_reporte=fecha_reporte,
    )


@pytest.mark.django_db
def test_p1_tiene_mayor_score_que_p4_con_mismo_tiempo(empresa_sin_sla):
    incidente_p1 = crear_incidente(empresa_sin_sla, "P1", horas_abierto=1)
    incidente_p4 = crear_incidente(empresa_sin_sla, "P4", horas_abierto=1)

    assert calcular_score(incidente_p1) > calcular_score(incidente_p4)


@pytest.mark.django_db
def test_mas_tiempo_abierto_aumenta_el_score(empresa_sin_sla):
    incidente_reciente = crear_incidente(empresa_sin_sla, "P3", horas_abierto=1)
    incidente_antiguo = crear_incidente(empresa_sin_sla, "P3", horas_abierto=20)

    assert calcular_score(incidente_antiguo) > calcular_score(incidente_reciente)


@pytest.mark.django_db
def test_contrato_sla_suma_puntos_extra(empresa_sin_sla, empresa_con_sla):
    incidente_sin_sla = crear_incidente(empresa_sin_sla, "P2", horas_abierto=5)
    incidente_con_sla = crear_incidente(empresa_con_sla, "P2", horas_abierto=5)

    assert calcular_score(incidente_con_sla) > calcular_score(incidente_sin_sla)


@pytest.mark.django_db
def test_incidente_resuelto_tiene_score_cero(empresa_sin_sla):
    incidente = crear_incidente(empresa_sin_sla, "P1", horas_abierto=100, estado="resuelto")

    assert calcular_score(incidente) == 0


@pytest.mark.django_db
def test_ordenar_por_prioridad_devuelve_orden_descendente(empresa_sin_sla):
    bajo = crear_incidente(empresa_sin_sla, "P4", horas_abierto=1)
    critico = crear_incidente(empresa_sin_sla, "P1", horas_abierto=1)
    medio = crear_incidente(empresa_sin_sla, "P3", horas_abierto=1)

    orden = ordenar_por_prioridad([bajo, critico, medio])

    assert orden[0] == critico
    assert orden[-1] == bajo
