# apps/core/management/commands/poblar_db.py

from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from datetime import date, timedelta

from apps.cobranza.models import (
    AjusteCobranza,
    Cobranza,
    DetallePago,
    EstadoCobranza,
    MedioPago,
)
from apps.core.models import EstadoVehiculo, Grupos, Transportista, Vehiculo
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    EstadoParada,
    EvidenciaParada,
    Itinerario,
    Parada,
    ProblemaParada,
    RutaGuardada,
    TipoProblema,
)
from apps.remitos.models import (
    Comercio,
    ErrorImportacion,
    EstadoImportacion,
    EstadoRemito,
    ImportacionRemitos,
    Marca,
    Remito,
)

Usuario = get_user_model()


class Command(BaseCommand):
    help = (
        "Carga datos maestros (Superusuario, Vehículos, Usuarios Chofer, Marcas, Comercios y Rutas Guardadas)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Elimina los datos de prueba anteriores antes de cargar.",
        )
        parser.add_argument(
            "--con-remitos",
            action="store_true",
            help="(Deshabilitado) Los remitos se gestionan importando las planillas de reparto.",
        )
        parser.add_argument(
            "--completo",
            action="store_true",
            help="(Deshabilitado) Mantenido por retrocompatibilidad.",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando la carga de datos de prueba..."))

        # Asegurar que existan todos los grupos y permisos del sistema
        call_command("crear_grupos", stdout=StringIO())

        with transaction.atomic():
            if options["limpiar"]:
                self.stdout.write("Limpiando datos existentes...")

                # 1. Cobranzas, Ajustes y Pagos (AjusteCobranza tiene FK a Usuario con PROTECT y FK a Cobranza; Cobranza tiene OneToOne PROTECT a Parada)
                AjusteCobranza.objects.all().delete()
                DetallePago.objects.all().delete()
                Cobranza.objects.all().delete()

                # 2. Evidencias y problemas de paradas (hijas de Parada)
                EvidenciaParada.objects.all().delete()
                ProblemaParada.objects.all().delete()

                # 3. Remitos e Importaciones (Remito tiene FK a Parada SET_NULL, FK a Comercio PROTECT, FK a Marca PROTECT)
                Remito.objects.all().delete()
                ErrorImportacion.objects.all().delete()
                ImportacionRemitos.objects.all().delete()

                # 4. Paradas e Itinerarios (Itinerario tiene FK PROTECT a Transportista y Vehiculo)
                Parada.objects.all().delete()
                Itinerario.objects.all().delete()

                # 5. Tablas intermedias e hijas de rutas
                DetalleRutaGuardada.objects.all().delete()
                RutaGuardada.objects.all().delete()

                # 6. Comercios y Marcas
                Comercio.objects.all().delete()
                Marca.objects.all().delete()

                # 7. Perfiles Transportista y Vehículos
                Transportista.objects.all().delete()
                Vehiculo.objects.all().delete()

                # 8. Desbloquear todos los usuarios (superusuario y regulares)
                Usuario.objects.all().update(is_active=True, intentos_fallidos=0)

            # ------------------------------------------------------------------
            # 1. Superusuario Administrador
            # ------------------------------------------------------------------
            admin_user, _ = Usuario.objects.get_or_create(
                username="11111111",
                defaults={
                    "first_name": "Administrador",
                    "last_name": "Softech",
                    "email": "admin@softech.com.ar",
                    "telefono": "1155551111",
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.intentos_fallidos = 0
            admin_user.set_password("123")
            admin_user.save()

            # Asignar todos los roles por defecto al superusuario
            todos_los_grupos = Group.objects.filter(name__in=Grupos.values)
            admin_user.groups.set(todos_los_grupos)

            # Usuarios específicos por rol para pruebas web (HU-35, HU-36, etc.)
            grupo_conciliacion, _ = Group.objects.get_or_create(name=Grupos.ADMIN_CONCILIACION)
            grupo_planificacion, _ = Group.objects.get_or_create(name=Grupos.ADMIN_PLANIFICACION)
            grupo_personal, _ = Group.objects.get_or_create(name=Grupos.GESTION_PERSONAL)

            conciliacion, _ = Usuario.objects.get_or_create(
                username="22222222",
                defaults={
                    "first_name": "Conciliacion",
                    "last_name": "Softech",
                    "email": "admin@softech.com.ar",
                    "telefono": "1155551111",
                    "is_staff": True,
                    "is_superuser": False,
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
            )
            conciliacion.is_staff = True
            conciliacion.is_superuser = False
            conciliacion.is_active = True
            conciliacion.intentos_fallidos = 0
            conciliacion.set_password("123")
            conciliacion.groups.add(grupo_conciliacion)
            conciliacion.save()

            planificacion, _ = Usuario.objects.get_or_create(
                username="33333333",
                defaults={
                    "first_name": "Planificacion",
                    "last_name": "Softech",
                    "email": "admin@softech.com.ar",
                    "telefono": "1155551111",
                    "is_staff": True,
                    "is_superuser": False,
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
            )
            planificacion.is_staff = True
            planificacion.is_superuser = False
            planificacion.is_active = True
            planificacion.intentos_fallidos = 0
            planificacion.set_password("123")
            planificacion.groups.add(grupo_planificacion)
            planificacion.save()

            personal, _ = Usuario.objects.get_or_create(
                username="44444444",
                defaults={
                    "first_name": "Personal",
                    "last_name": "Softech",
                    "email": "admin@softech.com.ar",
                    "telefono": "1155551111",
                    "is_staff": True,
                    "is_superuser": False,
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
            )
            personal.is_staff = True
            personal.is_superuser = False
            personal.is_active = True
            personal.intentos_fallidos = 0
            personal.set_password("123")
            personal.groups.add(grupo_personal)
            personal.save()

            # ------------------------------------------------------------------
            # 2. Vehículos
            # ------------------------------------------------------------------
            vehiculos_data = [
                {
                    "patente": "AF123CD",
                    "modelo": "Mercedes-Benz Accelo 815",
                    "poliza": "POL-987654",
                    "estado": EstadoVehiculo.ASIGNADO,
                },
                {
                    "patente": "AG456EF",
                    "modelo": "Iveco Daily 70C17",
                    "poliza": "POL-123456",
                    "estado": EstadoVehiculo.ASIGNADO,
                },
                {
                    "patente": "AD345JK",
                    "modelo": "Renault Kangoo 1.6",
                    "poliza": "POL-567890",
                    "estado": EstadoVehiculo.ASIGNADO,
                },
                {
                    "patente": "AE789GH",
                    "modelo": "Ford Cargo 915",
                    "poliza": "POL-345678",
                    "estado": EstadoVehiculo.DISPONIBLE,
                },
            ]
            vehiculos = {}
            for v_data in vehiculos_data:
                vehiculo, _ = Vehiculo.objects.get_or_create(
                    patente=v_data["patente"], defaults=v_data
                )
                vehiculos[v_data["patente"]] = vehiculo

            # ------------------------------------------------------------------
            # 3. Usuarios y Perfiles Transportista
            # ------------------------------------------------------------------
            choferes_data = [
                {
                    "username": "1234567",
                    "first_name": "Lautaro",
                    "last_name": "Gómez",
                    "telefono": "5491155554444",
                    "vehiculo": vehiculos["AF123CD"],
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
                {
                    "username": "12345678",
                    "first_name": "Martín",
                    "last_name": "Pérez",
                    "telefono": "5491155557777",
                    "vehiculo": vehiculos["AG456EF"],
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
                {
                    "username": "12345680",
                    "first_name": "Lucas",
                    "last_name": "Rodríguez",
                    "telefono": "5491155556666",
                    "vehiculo": vehiculos["AD345JK"],
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
                {
                    "username": "12345679",
                    "first_name": "Carlos",
                    "last_name": "Bloqueado",
                    "telefono": "5491155558888",
                    "vehiculo": None,
                    "is_active": False,
                    "intentos_fallidos": 5,
                },
                {
                    "username": "12345681",
                    "first_name": "Esteban",
                    "last_name": "Suplente",
                    "telefono": "5491155559999",
                    "vehiculo": None,
                    "is_active": True,
                    "intentos_fallidos": 0,
                },
            ]

            grupo_transportista, _ = Group.objects.get_or_create(name=Grupos.TRANSPORTISTA)
            for c_data in choferes_data:
                v = c_data.pop("vehiculo")
                is_active = c_data.pop("is_active", True)
                intentos_fallidos = c_data.pop("intentos_fallidos", 0)
                user, _ = Usuario.objects.get_or_create(
                    username=c_data["username"],
                    defaults={
                        "first_name": c_data["first_name"],
                        "last_name": c_data["last_name"],
                        "telefono": c_data["telefono"],
                        "is_active": is_active,
                        "intentos_fallidos": intentos_fallidos,
                    },
                )
                user.is_active = is_active
                user.intentos_fallidos = intentos_fallidos
                user.groups.add(grupo_transportista)
                user.set_password("123")
                user.save()

                transportista, _ = Transportista.objects.get_or_create(
                    usuario=user,
                    defaults={"vehiculo": v},
                )
                if transportista.vehiculo != v:
                    transportista.vehiculo = v
                    transportista.save(update_fields=["vehiculo"])

            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # 4. Marcas
            # ------------------------------------------------------------------
            marcas_data = [
                {
                    "nombre": "Cerveceria La Diagonal S.A.",
                    "cuit": "30654321090",
                    "activo": True,
                },
                {
                    "nombre": "Snacks Andinos S.R.L.",
                    "cuit": "30709876542",
                    "activo": True,
                },
                {
                    "nombre": "Gaseosas del Sur S.A.",
                    "cuit": "30712345671",
                    "activo": True,
                },
                {
                    "nombre": "Lacteos El Tambo S.A.",
                    "cuit": "33698712347",
                    "activo": True,
                },
            ]
            marcas = {}
            for m_data in marcas_data:
                marca, _ = Marca.objects.get_or_create(
                    cuit=m_data["cuit"], defaults=m_data
                )
                marcas[m_data["cuit"]] = marca
                marcas[m_data["nombre"]] = marca

            # ------------------------------------------------------------------
            # 5. Comercios
            # ------------------------------------------------------------------
            comercios_data = [
                {
                    "razon_social": "ALMACEN SAN CAYETANO S.A.",
                    "cuit": "23200034562",
                    "domicilio": "Av. Hipolito Yrigoyen 417, Berazategui",
                    "telefono": "1142500049",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO AVENIDA S.R.L.",
                    "cuit": "23200039289",
                    "domicilio": "Belgrano 5541, CABA",
                    "telefono": "1142500037",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN LOS PIBES S.R.L.",
                    "cuit": "23200042867",
                    "domicilio": "Av. Mitre 478, Lomas de Zamora",
                    "telefono": "1142500047",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO AVENIDA S.R.L.",
                    "cuit": "23200048148",
                    "domicilio": "Av. Hipolito Yrigoyen 2810, Florencio Varela",
                    "telefono": "1142500001",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO DOÑA ROSA S.A.S.",
                    "cuit": "23200056655",
                    "domicilio": "Belgrano 4950, Bernal",
                    "telefono": "1142500003",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA MI BARRIO",
                    "cuit": "23200058011",
                    "domicilio": "Av. Mitre 3541, Berazategui",
                    "telefono": "1142500008",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO SANTA RITA S.A.",
                    "cuit": "23200060768",
                    "domicilio": "Castelli 2762, Lanus",
                    "telefono": "1142500009",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO LA RIBERA S.A.",
                    "cuit": "23200063767",
                    "domicilio": "Sarmiento 2916, Wilde",
                    "telefono": "1142500053",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA DOÑA ROSA",
                    "cuit": "27200002143",
                    "domicilio": "Av. La Plata 5423, Bernal",
                    "telefono": "1142500019",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA DOÑA ROSA S.A.",
                    "cuit": "27200004480",
                    "domicilio": "Av. La Plata 669, Avellaneda",
                    "telefono": "1142500052",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO LA RIBERA",
                    "cuit": "27200010979",
                    "domicilio": "Independencia 2285, Temperley",
                    "telefono": "1142500007",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO EL IMAN S.A.",
                    "cuit": "27200012467",
                    "domicilio": "9 de Julio 1729, Lanus",
                    "telefono": "1142500024",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN LA RIBERA S.A.S.",
                    "cuit": "27200015849",
                    "domicilio": "Independencia 6079, Bernal",
                    "telefono": "1142500031",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN EL GALLEGO S.A.",
                    "cuit": "27200027677",
                    "domicilio": "Dorrego 663, Lomas de Zamora",
                    "telefono": "1142500020",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN EL FARO",
                    "cuit": "27200029157",
                    "domicilio": "Belgrano 976, Bernal",
                    "telefono": "1142500005",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO MI BARRIO S.A.",
                    "cuit": "27200037540",
                    "domicilio": "Av. Hipolito Yrigoyen 5066, Florencio Varela",
                    "telefono": "1142500016",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO EL AGUILA S.A.",
                    "cuit": "27200045926",
                    "domicilio": "Castelli 5992, Florencio Varela",
                    "telefono": "1142500012",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN LA ESQUINA S.A.",
                    "cuit": "27200053499",
                    "domicilio": "Independencia 5439, Avellaneda",
                    "telefono": "1142500055",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO AVENIDA S.A.S.",
                    "cuit": "27200059900",
                    "domicilio": "Castelli 6088, Sarandi",
                    "telefono": "1142500011",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN AVENIDA",
                    "cuit": "27200061891",
                    "domicilio": "Lavalle 4648, Lomas de Zamora",
                    "telefono": "1142500023",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO EL HORNERO S.A.S.",
                    "cuit": "27200067490",
                    "domicilio": "Moreno 1610, Avellaneda",
                    "telefono": "1142500026",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO LA ESQUINA S.A.S.",
                    "cuit": "27200074675",
                    "domicilio": "9 de Julio 426, Wilde",
                    "telefono": "1142500015",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO SAN CAYETANO S.R.L.",
                    "cuit": "30200002934",
                    "domicilio": "Belgrano 3212, Quilmes",
                    "telefono": "1142500025",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO EL FARO S.R.L.",
                    "cuit": "30200005933",
                    "domicilio": "Av. La Plata 5699, Temperley",
                    "telefono": "1142500036",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO DON CHICHO S.A.S.",
                    "cuit": "30200010244",
                    "domicilio": "Castelli 998, Lanus",
                    "telefono": "1142500045",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO 24 HS S.R.L.",
                    "cuit": "30200014096",
                    "domicilio": "Dorrego 4747, Quilmes",
                    "telefono": "1142500043",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA LA RIBERA",
                    "cuit": "30200016870",
                    "domicilio": "Av. Rivadavia 4920, Lomas de Zamora",
                    "telefono": "1142500046",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN LA RIBERA S.A.S.",
                    "cuit": "30200018660",
                    "domicilio": "San Martin 6025, Sarandi",
                    "telefono": "1142500051",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO EL HORNERO S.R.L.",
                    "cuit": "30200021092",
                    "domicilio": "Av. Rivadavia 717, Berazategui",
                    "telefono": "1142500050",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO MI BARRIO",
                    "cuit": "30200024032",
                    "domicilio": "Av. Mitre 510, Sarandi",
                    "telefono": "1142500056",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO SAN CAYETANO S.R.L.",
                    "cuit": "30200025527",
                    "domicilio": "Dorrego 4766, Lomas de Zamora",
                    "telefono": "1142500041",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN EL FARO S.A.",
                    "cuit": "30200026299",
                    "domicilio": "Av. Hipolito Yrigoyen 1172, Temperley",
                    "telefono": "1142500042",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA DON CHICHO S.R.L.",
                    "cuit": "30200031608",
                    "domicilio": "Castelli 3124, Sarandi",
                    "telefono": "1142500017",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO EL GALLEGO",
                    "cuit": "30200035972",
                    "domicilio": "Urquiza 4273, Wilde",
                    "telefono": "1142500058",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN AVENIDA S.R.L.",
                    "cuit": "30200040437",
                    "domicilio": "Urquiza 3205, Temperley",
                    "telefono": "1142500032",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO AVENIDA",
                    "cuit": "30200044025",
                    "domicilio": "Av. Rivadavia 1540, Bernal",
                    "telefono": "1142500044",
                    "activo": True,
                },
                {
                    "razon_social": "MAXIKIOSCO EL FARO S.R.L.",
                    "cuit": "30200055523",
                    "domicilio": "Independencia 3121, Lanus",
                    "telefono": "1142500034",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO LA RIBERA",
                    "cuit": "30200064794",
                    "domicilio": "Independencia 5753, Lanus",
                    "telefono": "1142500010",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN LA NUEVA UNION S.A.",
                    "cuit": "30200066053",
                    "domicilio": "Av. Mitre 5900, Florencio Varela",
                    "telefono": "1142500028",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO 24 HS S.A.",
                    "cuit": "30200069222",
                    "domicilio": "Belgrano 4671, Wilde",
                    "telefono": "1142500004",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO LOS PIBES S.R.L.",
                    "cuit": "30200073432",
                    "domicilio": "Belgrano 588, Lanus",
                    "telefono": "1142500022",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN SANTA RITA",
                    "cuit": "30200076083",
                    "domicilio": "Sarmiento 5437, Berazategui",
                    "telefono": "1142500048",
                    "activo": True,
                },
                {
                    "razon_social": "ALMACEN MI BARRIO",
                    "cuit": "30200077578",
                    "domicilio": "Av. Hipolito Yrigoyen 5782, Berazategui",
                    "telefono": "1142500035",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO SANTA RITA S.A.S.",
                    "cuit": "30200079821",
                    "domicilio": "Belgrano 336, Temperley",
                    "telefono": "1142500038",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO LOS PIBES",
                    "cuit": "30200081427",
                    "domicilio": "Lavalle 5970, Banfield",
                    "telefono": "1142500040",
                    "activo": True,
                },
                {
                    "razon_social": "AUTOSERVICIO LA RIBERA",
                    "cuit": "23200033191",
                    "domicilio": "Dorrego 3429, Sarandi",
                    "telefono": "1142500000",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO EL FARO",
                    "cuit": "23200000145",
                    "domicilio": "Av. Rivadavia 1928, Lanus",
                    "telefono": "1142500000",
                    "activo": True,
                },
                {
                    "razon_social": "KIOSCO EL TREBOL S.A.S.",
                    "cuit": "20200022190",
                    "domicilio": "Av. Hipolito Yrigoyen 117, Wilde",
                    "telefono": "1142500000",
                    "activo": True,
                },
                {
                    "razon_social": "DESPENSA SAN CAYETANO",
                    "cuit": "20200070268",
                    "domicilio": "Independencia 1802, Temperley",
                    "telefono": "1142500000",
                    "activo": True,
                },
                {
                    "razon_social": "MINIMERCADO EL HORNERO S.A.S.",
                    "cuit": "23200008855",
                    "domicilio": "San Martin 2269, Lanus",
                    "telefono": "1142500000",
                    "activo": True,
                },
            ]

            comercios = {}
            for c_data in comercios_data:
                comercio, _ = Comercio.objects.get_or_create(
                    cuit=c_data["cuit"], defaults=c_data
                )
                comercios[c_data["cuit"]] = comercio

            # ------------------------------------------------------------------
            # 6. Lote con errores de auditoría (HU-38)
            # ------------------------------------------------------------------
            # Se registra un lote rechazado con errores para verificar la pantalla de excepciones
            lote_rechazado, _ = ImportacionRemitos.objects.get_or_create(
                archivo="importaciones/30712345671_lote_con_errores.csv",
                defaults={
                    "marca": marcas["30712345671"],
                    "cantidad": 0,
                    "estado": EstadoImportacion.RECHAZADO,
                },
            )
            ErrorImportacion.objects.filter(importacion=lote_rechazado).delete()
            ErrorImportacion.objects.create(
                importacion=lote_rechazado,
                fila=2,
                motivo="CUIT del comercio inválido (debe tener 11 dígitos numéricos).",
            )
            ErrorImportacion.objects.create(
                importacion=lote_rechazado,
                fila=5,
                motivo="La razón social es obligatoria para comercios no registrados previamente.",
            )

            # ------------------------------------------------------------------
            # 7. Rutas Guardadas de prueba (HU-63, HU-64, HU-65)
            # ------------------------------------------------------------------
            # Asociadas directamente a Chofer y Comercios, sin remitos ni paradas
            comercios_lista = list(comercios.values())

            transportista_martin = Transportista.objects.filter(
                usuario__username="12345678"
            ).first()
            if transportista_martin:
                ruta_guardada_martin, _ = RutaGuardada.objects.get_or_create(
                    transportista=transportista_martin,
                    nombre="Ruta Costera 12",
                )
                DetalleRutaGuardada.objects.filter(ruta_guardada=ruta_guardada_martin).delete()
                for p_idx, com in enumerate(comercios_lista[:3], start=1):
                    DetalleRutaGuardada.objects.create(
                        ruta_guardada=ruta_guardada_martin,
                        comercio=com,
                        prioridad=p_idx,
                    )

            chofer_lautaro = Usuario.objects.filter(username="1234567").first()
            if chofer_lautaro:
                transportista_lautaro = getattr(chofer_lautaro, "perfil_transportista", None)
                if transportista_lautaro:
                    ruta_guardada_lautaro, _ = RutaGuardada.objects.get_or_create(
                        transportista=transportista_lautaro,
                        nombre="Ruta Rapida Alternativa",
                    )
                    DetalleRutaGuardada.objects.filter(ruta_guardada=ruta_guardada_lautaro).delete()
                    for idx_r, com_r in enumerate(comercios_lista[3:7], start=1):
                        DetalleRutaGuardada.objects.create(
                            ruta_guardada=ruta_guardada_lautaro,
                            comercio=com_r,
                            prioridad=idx_r,
                        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("✓ Datos maestros cargados exitosamente.")
        )
        self.stdout.write("  • Superusuario: 11111111 (clave: 123)")
        self.stdout.write("  • Administrativo Conciliacion: 22222222 (clave: 123)")
        self.stdout.write("  • Administrativo Planificacion: 33333333 (clave: 123)")
        self.stdout.write("  • Administrativo Gestion Personal: 44444444 (clave: 123)")
        self.stdout.write(f"  • Comercios: {len(comercios_data)}")
        self.stdout.write(f"  • Marcas: {len(marcas_data)}")
        self.stdout.write("  • Choferes / Transportistas: 5 perfiles activos/configurados")
        self.stdout.write("  • Rutas guardadas: 2 rutas base ('Ruta Costera 12', 'Ruta Rapida Alternativa')")
        self.stdout.write("  • Remitos e Itinerarios: 0 (los remitos se cargan importando las planillas CSV/Excel)")

        self.stdout.write(
            self.style.HTTP_INFO("\n" + "=" * 70)
        )
        self.stdout.write(
            self.style.HTTP_INFO("📋 CASOS DE PRUEBA Y CREDENCIALES DISPONIBLES")
        )
        self.stdout.write(
            self.style.HTTP_INFO("=" * 70)
        )

        self.stdout.write(self.style.WARNING("\n1. Superusuario y Administrativos Web"))
        self.stdout.write("   • Superusuario Admin   : 11111111 | Clave: 123 (Todos los accesos)")
        self.stdout.write("   • Admin Conciliación   : 22222222 | Clave: 123 (Cobranzas, Arqueo, Ajuste con DNI registrado)")
        self.stdout.write("   • Admin Planificación  : 33333333 | Clave: 123 (Planillas, Remitos, Diagramación)")
        self.stdout.write("   • Admin Personal       : 44444444 | Clave: 123 (Choferes, Desbloqueo)")

        self.stdout.write(self.style.WARNING("\n2. Transportistas (Choferes - App Móvil / Rutas)"))
        self.stdout.write("   • Chofer 1: DNI 1234567  | Clave: 123 | Lautaro Gómez | Vehículo: AF123CD")
        self.stdout.write("     - Ruta guardada: 'Ruta Rapida Alternativa'.")
        self.stdout.write("   • Chofer 2: DNI 12345678 | Clave: 123 | Martín Pérez  | Vehículo: AG456EF")
        self.stdout.write("     - Ruta guardada: 'Ruta Costera 12'.")
        self.stdout.write("   • Chofer 3 (Bloqueado/Suspendido): DNI 12345679 | Clave: 123 | Carlos Bloqueado (Para probar desbloqueo HU-11 / HU-66).")
        self.stdout.write("   • Chofer 4: DNI 12345680 | Clave: 123 | Lucas Rodríguez | Vehículo: AD345JK")
        self.stdout.write("   • Chofer 5 (Sin Ruta - Caso de Borde): DNI 12345681 | Clave: 123 | Esteban Suplente (Sin itinerario asignado HU-62).")

        self.stdout.write(self.style.WARNING("\n3. Flujo Operativo y Remitos"))
        self.stdout.write("   • Importación de Planillas: Ingresar con Admin Planificación (33333333) e importar planillas CSV/Excel.")
        self.stdout.write("   • Diagramación de Itinerarios: Diagramar itinerarios asignando paradas y remitos desde la interfaz web.")
        self.stdout.write("   • Lote Rechazado de Ejemplo: Lote con errores de fila registrado para verificar auditoría de excepciones.")

        self.stdout.write(
            self.style.HTTP_INFO("=" * 70 + "\n")
        )
