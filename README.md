# Sistema de priorización de incidentes técnicos

Aplicación web en Django que registra incidentes técnicos y los ordena automáticamente por urgencia, combinando prioridad, tiempo abierto y contrato SLA del cliente.

## Problema que resuelve / contexto

Este es un proyecto de práctica personal, inspirado en un problema real que se da en cualquier área de soporte técnico: cuando hay varios incidentes abiertos a la vez, no siempre es obvio cuál atender primero. Un ticket de baja prioridad que lleva tres días abierto puede ser más urgente que uno crítico recién reportado.

Lo construí para practicar Django con un caso de uso completo (modelos relacionados, lógica de negocio simple, dashboard, generación de reportes en PDF) y para tener algo mostrable en mi portafolio. Todos los datos (empresa, técnicos, incidentes) son ficticios y se generan con un comando de siembra; no corresponden a ningún cliente ni empresa real.

## Stack tecnológico

- Django 5.x
- PostgreSQL (vía Docker) / SQLite (para desarrollo local sin Docker)
- Docker y docker-compose
- WeasyPrint (generación de reportes en PDF)
- Chart.js (gráficos del dashboard, vía CDN)
- pytest / pytest-django (tests)

## Cómo correrlo localmente

### 1. Clonar y configurar variables de entorno

```bash
git clone <url-del-repo>
cd incidentes-practica
cp .env.example .env
```

Edita `.env` y genera tu propio `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Opción A: sin Docker (SQLite)

Con `USE_SQLITE=True` en tu `.env` (valor por defecto), no necesitas Postgres ni Docker.

```bash
python -m venv venv
venv\Scripts\activate          # en Windows
# source venv/bin/activate     # en Linux/Mac

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo     # carga los datos de demostración ficticios
python manage.py runserver
```

Nota: la generación de PDF con WeasyPrint depende de librerías nativas (Pango/Cairo/GTK) que en Windows requieren una instalación aparte. Si solo vas a probar el dashboard y el listado de incidentes, SQLite sin Docker es suficiente; para probar los reportes en PDF se recomienda la opción con Docker.

### 3. Opción B: con Docker (PostgreSQL)

Cambia `USE_SQLITE=False` en tu `.env` y define las credenciales de Postgres que prefieras.

```bash
docker-compose up --build
```

En otra terminal, dentro del contenedor:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_demo
```

La app queda disponible en `http://localhost:8000`.

### 4. Crear un superusuario

El superusuario nunca se crea con contraseña hardcodeada. Dos formas de hacerlo:

```bash
# Interactiva (recomendada)
python manage.py createsuperuser

# O definiendo DJANGO_SUPERUSER_* en tu .env y usando --noinput
python manage.py createsuperuser --noinput
```

### 5. Correr los tests

```bash
pytest
```
