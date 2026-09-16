# Sistema de priorización de incidentes técnicos

Aplicación web en Django para registrar incidentes técnicos y ordenarlos automáticamente según urgencia, tiempo abierto y condiciones de SLA.

## Contexto

Proyecto de portafolio inspirado en un problema frecuente de soporte técnico: cuando existen múltiples incidentes abiertos, la prioridad declarada no siempre refleja cuál requiere atención inmediata. El sistema incorpora reglas de negocio para facilitar una atención ordenada y trazable.

Todos los datos incluidos son ficticios y se generan únicamente con fines de demostración.

## Funcionalidades principales

- Registro y gestión de incidentes técnicos.
- Priorización automática considerando prioridad, antigüedad y SLA.
- Dashboard con indicadores operativos.
- Generación de reportes en PDF.
- Datos de demostración mediante comando de siembra.
- Configuración para PostgreSQL con Docker o SQLite en desarrollo local.
- Pruebas automatizadas con pytest y pytest-django.

## Stack tecnológico

- Python
- Django 5.x
- PostgreSQL / SQLite
- Docker y Docker Compose
- WeasyPrint
- Chart.js
- pytest / pytest-django

## Ejecución local

### 1. Clonar y configurar

```bash
git clone https://github.com/pansitozzz/incidentes-practica.git
cd incidentes-practica
cp .env.example .env
```

Para generar una clave segura de Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Desarrollo local con SQLite

Con `USE_SQLITE=True` en `.env`:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
# source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### 3. Ejecución con PostgreSQL y Docker

Configurar `USE_SQLITE=False` y las credenciales de PostgreSQL en `.env`, luego ejecutar:

```bash
docker-compose up --build
```

En otra terminal:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_demo
```

La aplicación queda disponible en `http://localhost:8000`.

> La generación de PDF con WeasyPrint requiere dependencias nativas adicionales en algunos entornos. La configuración con Docker facilita su ejecución.

## Pruebas

```bash
pytest
```

## Privacidad

Este repositorio es una versión demostrativa e independiente. No contiene información confidencial, nombres reales de clientes ni datos de producción.
