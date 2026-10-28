from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Crea y sincroniza los grupos y permisos del sistema. Opcionalmente elimina los grupos con --limpiar."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            "-l",
            action="store_true",
            help="Elimina los grupos del sistema antes de crearlos y asignarles los permisos.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        limpiar = options["limpiar"]

        grupos_config = {
            # -------------------------------------------------------------
            # 1. PLANIFICACIÓN OPERATIVA
            # -------------------------------------------------------------
            "administrativo-planificacion": [
                # Maestros de logística: Comercios y Marcas
                "add_comercio",
                "change_comercio",
                "view_comercio",
                "add_marca",
                "change_marca",
                "view_marca",
                # Lotes y Remitos
                "add_importacionremitos",
                "change_importacionremitos",
                "view_importacionremitos",
                "add_remito",
                "change_remito",
                "view_remito",
                "delete_remito",
                # Itinerarios y Paradas
                "add_itinerario",
                "change_itinerario",
                "view_itinerario",
                "delete_itinerario",
                "add_parada",
                "change_parada",
                "view_parada",
                "delete_parada",
                # Rutas y plantillas
                "view_rutaguardada",
                "view_detallerutaguardada",
                # Flota y Choferes (consulta)
                "view_vehiculo",
                "view_transportista",
                # Incidencias y Evidencias
                "view_problemaparada",
                "view_evidenciaparada",
            ],

            # -------------------------------------------------------------
            # 2. AUDITORÍA Y CONCILIACIÓN DE COBRANZAS
            # -------------------------------------------------------------
            "administrativo-conciliacion": [
                # Cobranzas y Detalles de Pago
                "view_cobranza",
                "change_cobranza",
                "view_detallepago",
                "change_detallepago",
                # Lectura para auditar entregas y facturación
                "view_remito",
                "view_comercio",
                "view_marca",
                "view_itinerario",
                "view_parada",
                "view_problemaparada",
                "view_evidenciaparada",
            ],

            # -------------------------------------------------------------
            # 3. TRANSPORTISTA (App Móvil)
            # -------------------------------------------------------------
            "transportista": [
                # Hoja de ruta y entregas
                "view_itinerario",
                "view_parada",
                "change_parada",
                "view_remito",
                "view_comercio",
                # Rendición de cobranzas en calle
                "add_cobranza",
                "view_cobranza",
                "add_detallepago",
                "view_detallepago",
                # Incidencias y fotos
                "add_problemaparada",
                "view_problemaparada",
                "add_evidenciaparada",
                "view_evidenciaparada",
                # Plantillas y orden de paradas
                "add_rutaguardada",
                "change_rutaguardada",
                "view_rutaguardada",
                "delete_rutaguardada",
                "add_detallerutaguardada",
                "change_detallerutaguardada",
                "delete_detallerutaguardada",
                "view_detallerutaguardada",
            ],

            # -------------------------------------------------------------
            # 4. GESTIÓN DE PERSONAL Y FLOTA (Satélite)
            # -------------------------------------------------------------
            "gestion-personal": [
                # Usuarios y Cuentas de acceso
                "add_usuario",
                "change_usuario",
                "view_usuario",
                "delete_usuario",
                # Perfiles de transportistas
                "add_transportista",
                "change_transportista",
                "view_transportista",
                "delete_transportista",
                # Flota de Vehículos
                "add_vehiculo",
                "change_vehiculo",
                "view_vehiculo",
                "delete_vehiculo",
            ],
        }

        # Si se pasó el flag --limpiar, borramos los grupos definidos antes de recrear
        if limpiar:
            self.stdout.write(self.style.WARNING("Eliminando grupos existentes..."))
            nombres_a_eliminar = list(grupos_config.keys())
            borrados, _ = Group.objects.filter(name__in=nombres_a_eliminar).delete()
            self.stdout.write(
                self.style.SUCCESS(f"Se eliminaron {borrados} registros asociados a los grupos.\n")
            )

        self.stdout.write(self.style.NOTICE("Sincronizando grupos y permisos..."))

        for nombre_grupo, codenames in grupos_config.items():
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            accion = "Creado" if created else "Actualizado"

            permisos = Permission.objects.filter(codename__in=codenames)
            grupo.permissions.set(permisos)

            encontrados = set(permisos.values_list("codename", flat=True))
            faltantes = set(codenames) - encontrados
            if faltantes:
                self.stdout.write(
                    self.style.WARNING(
                        f"  [!] Grupo '{nombre_grupo}': permisos no encontrados en BD: {list(faltantes)}"
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Grupo '{nombre_grupo}' ({accion}) - {permisos.count()} permisos asignados."
                )
            )

        self.stdout.write(self.style.SUCCESS("\n¡Proceso completado exitosamente!"))
