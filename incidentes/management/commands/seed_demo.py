"""
Comando de management para cargar datos de demostración 100% ficticios.

Uso:
    python manage.py seed_demo
    python manage.py seed_demo --limpiar   (borra los datos demo antes de recrearlos)
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from incidentes.models import Activo, Empresa, Incidente, Tecnico


class Command(BaseCommand):
    help = "Carga datos de demostración ficticios para el sistema de priorización de incidentes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Elimina los datos demo existentes antes de volver a crearlos.",
        )

    def handle(self, *args, **options):
        if options["limpiar"]:
            self.stdout.write("Eliminando datos demo existentes...")
            Incidente.objects.all().delete()
            Activo.objects.all().delete()
            Tecnico.objects.all().delete()
            Empresa.objects.all().delete()

        empresa, creada = Empresa.objects.get_or_create(
            nombre="Empresa Demo S.A.C.",
            defaults={
                "rubro": "Comercio genérico",
                "tiene_contrato_sla": True,
                "contacto_nombre": "María López - Administración",
                "contacto_email": "contacto@empresademo.example.com",
            },
        )
        if creada:
            self.stdout.write(self.style.SUCCESS(f"Empresa creada: {empresa.nombre}"))

        tecnicos_info = [
            ("Juan Pérez - Técnico", "Redes y servidores"),
            ("Ana Torres - Técnico", "Soporte de equipos"),
            ("Luis Ramírez - Técnico", "Bases de datos"),
        ]
        tecnicos = []
        for nombre, especialidad in tecnicos_info:
            tecnico, _ = Tecnico.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "especialidad": especialidad,
                    "email": nombre.split(" ")[0].lower() + "@empresademo.example.com",
                },
            )
            tecnicos.append(tecnico)

        activos_info = [
            ("Servidor de Archivos", "servidor", "SRV-001"),
            ("Servidor de Correo", "servidor", "SRV-002"),
            ("PC Recepción", "pc", "PC-010"),
            ("PC Contabilidad", "pc", "PC-014"),
            ("Impresora Piso 2", "impresora", "IMP-003"),
            ("Router Principal", "red", "RED-001"),
        ]
        activos = []
        for nombre, tipo, codigo in activos_info:
            activo, _ = Activo.objects.get_or_create(
                empresa=empresa,
                nombre=nombre,
                defaults={"tipo": tipo, "codigo_inventario": codigo},
            )
            activos.append(activo)

        ahora = timezone.now()

        incidentes_info = [
            {
                "titulo": "Servidor de correo no responde",
                "descripcion": "Los usuarios no pueden enviar ni recibir correos desde esta mañana.",
                "prioridad": "P1",
                "estado": "en_progreso",
                "activo": activos[1],
                "tecnico": tecnicos[0],
                "horas_desde_reporte": 5,
                "resuelto": False,
            },
            {
                "titulo": "Caída intermitente de la red del piso 2",
                "descripcion": "La conexión se cae cada cierto tiempo en el área de ventas.",
                "prioridad": "P1",
                "estado": "abierto",
                "activo": activos[5],
                "tecnico": None,
                "horas_desde_reporte": 12,
                "resuelto": False,
            },
            {
                "titulo": "Lentitud en PC de Contabilidad",
                "descripcion": "El equipo tarda mucho en abrir el sistema contable.",
                "prioridad": "P2",
                "estado": "en_progreso",
                "activo": activos[3],
                "tecnico": tecnicos[1],
                "horas_desde_reporte": 30,
                "resuelto": False,
            },
            {
                "titulo": "Impresora del piso 2 sin tóner",
                "descripcion": "Se solicita cambio de tóner y revisión general.",
                "prioridad": "P4",
                "estado": "abierto",
                "activo": activos[4],
                "tecnico": None,
                "horas_desde_reporte": 3,
                "resuelto": False,
            },
            {
                "titulo": "Backup del servidor de archivos incompleto",
                "descripcion": "El respaldo automático de anoche se detuvo a la mitad.",
                "prioridad": "P2",
                "estado": "resuelto",
                "activo": activos[0],
                "tecnico": tecnicos[2],
                "horas_desde_reporte": 48,
                "resuelto": True,
                "horas_para_resolver": 6,
            },
            {
                "titulo": "PC de recepción no enciende",
                "descripcion": "Posible falla de fuente de poder.",
                "prioridad": "P3",
                "estado": "cerrado",
                "activo": activos[2],
                "tecnico": tecnicos[1],
                "horas_desde_reporte": 72,
                "resuelto": True,
                "horas_para_resolver": 20,
            },
            {
                "titulo": "Router principal se reinicia solo",
                "descripcion": "Reinicios espontáneos varias veces al día, se sospecha de sobrecalentamiento.",
                "prioridad": "P1",
                "estado": "abierto",
                "activo": activos[5],
                "tecnico": tecnicos[0],
                "horas_desde_reporte": 2,
                "resuelto": False,
            },
            {
                "titulo": "Actualización de antivirus pendiente en varios equipos",
                "descripcion": "Se detectaron equipos con la definición de virus desactualizada.",
                "prioridad": "P4",
                "estado": "en_progreso",
                "activo": None,
                "tecnico": tecnicos[2],
                "horas_desde_reporte": 20,
                "resuelto": False,
            },
        ]

        creados = 0
        for datos in incidentes_info:
            fecha_reporte = ahora - timedelta(hours=datos["horas_desde_reporte"])
            fecha_resolucion = None
            if datos.get("resuelto"):
                fecha_resolucion = fecha_reporte + timedelta(hours=datos.get("horas_para_resolver", 4))

            _, creado = Incidente.objects.get_or_create(
                empresa=empresa,
                titulo=datos["titulo"],
                defaults={
                    "descripcion": datos["descripcion"],
                    "prioridad": datos["prioridad"],
                    "estado": datos["estado"],
                    "activo": datos["activo"],
                    "tecnico_asignado": datos["tecnico"],
                    "fecha_reporte": fecha_reporte,
                    "fecha_resolucion": fecha_resolucion,
                },
            )
            if creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. {creados} incidentes de demostración creados."))
        self.stdout.write(
            "Recuerda: todos los datos (empresa, técnicos, incidentes) son ficticios, "
            "pensados solo para practicar y mostrar el proyecto en el portafolio."
        )
