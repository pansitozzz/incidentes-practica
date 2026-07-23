"""
Lógica simple de priorización de incidentes.

La idea es calcular un "score" numérico para poder ordenar los incidentes
de mayor a menor urgencia, combinando tres factores:

1. Nivel de prioridad declarado (P1 a P4).
2. Tiempo que lleva abierto el incidente (entre más tiempo, más urgente).
3. Si la empresa tiene contrato SLA activo (suma puntos extra de urgencia).

Este cálculo es deliberadamente simple: es un proyecto de práctica para
mostrar el concepto, no un motor de priorización productivo.
"""

PESO_BASE_PRIORIDAD = {
    "P1": 100,
    "P2": 70,
    "P3": 40,
    "P4": 10,
}

PUNTOS_POR_HORA_ABIERTO = 0.5
TOPE_PUNTOS_POR_TIEMPO = 40

BONUS_SLA = 20


def calcular_score(incidente):
    """Calcula el score de urgencia de un incidente.

    Un score más alto significa que el incidente debería atenderse antes.
    """
    if incidente.esta_resuelto:
        return 0

    score = PESO_BASE_PRIORIDAD.get(incidente.prioridad, 0)

    puntos_tiempo = min(incidente.horas_abierto * PUNTOS_POR_HORA_ABIERTO, TOPE_PUNTOS_POR_TIEMPO)
    score += puntos_tiempo

    if incidente.empresa_id and incidente.empresa.tiene_contrato_sla:
        score += BONUS_SLA

    return round(score, 1)


def ordenar_por_prioridad(incidentes):
    """Recibe un iterable de incidentes y lo devuelve ordenado por score descendente."""
    return sorted(incidentes, key=calcular_score, reverse=True)
