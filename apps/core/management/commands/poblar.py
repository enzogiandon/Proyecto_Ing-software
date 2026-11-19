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
        "Carga datos maestros (Superusuario, Vehículos, Usuarios Chofer, Marcas, Comercios) "
        "y opcionalmente Remitos, Itinerarios y Cobranzas."
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
            help="Carga un conjunto de remitos de prueba pendientes (por defecto no se cargan remitos).",
        )
        parser.add_argument(
            "--completo",
            action="store_true",
            help="Carga el flujo completo: remitos, itinerario con paradas asignado al usuario 1234567 y cobranzas.",
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
            # 6. Remitos (opcional mediante --con-remitos o --completo)
            # ------------------------------------------------------------------
            total_remitos = 0
            cargar_remitos = options["con_remitos"] or options["completo"]
            remitos_creados = {}
            if cargar_remitos:
                remitos_definicion = [
                    # Cerveceria La Diagonal S.A. (30654321090)
                    {
                        "numero": "0005-00024715",
                        "marca": marcas["30654321090"],
                        "comercio": comercios["23200048148"],
                        "total": Decimal("364269.35"),
                    },
                    {
                        "numero": "0002-00023458",
                        "marca": marcas["30654321090"],
                        "comercio": comercios["23200034562"],
                        "total": Decimal("199477.06"),
                    },
                    {
                        "numero": "0002-00023496",
                        "marca": marcas["30654321090"],
                        "comercio": comercios["23200056655"],
                        "total": Decimal("829717.82"),
                    },
                    # Snacks Andinos S.R.L. (30709876542)
                    {
                        "numero": "0090-00015378",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200039289"],
                        "total": Decimal("475923.72"),
                    },
                    {
                        "numero": "0090-00025539",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200042867"],
                        "total": Decimal("692074.74"),
                    },
                    {
                        "numero": "0090-00015345",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200056655"],
                        "total": Decimal("671210.29"),
                    },
                    # Gaseosas del Sur S.A. (30712345671)
                    {
                        "numero": "0090-00003901",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["23200039289"],
                        "total": Decimal("733385.18"),
                    },
                    {
                        "numero": "0090-00003921",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["30200025527"],
                        "total": Decimal("492487.48"),
                    },
                    {
                        "numero": "0090-00033994",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["23200063767"],
                        "total": Decimal("334706.88"),
                    },
                    # Lacteos El Tambo S.A. (33698712347)
                    {
                        "numero": "0090-00028325",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200063767"],
                        "total": Decimal("526471.00"),
                    },
                    {
                        "numero": "0090-00010362",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200058011"],
                        "total": Decimal("353247.34"),
                    },
                    {
                        "numero": "0090-00028378",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200060768"],
                        "total": Decimal("609129.43"),
                    },
                    # Casos de Unicidad Compuesta por Marca + Remito (HU-04)
                    {
                        "numero": "0001-00099999",
                        "marca": marcas["30654321090"],  # Cervecería La Diagonal S.A.
                        "comercio": comercios["23200034562"],
                        "total": Decimal("150000.00"),
                    },
                    {
                        "numero": "0001-00099999",
                        "marca": marcas["30709876542"],  # Snacks Andinos S.R.L.
                        "comercio": comercios["23200039289"],
                        "total": Decimal("85000.00"),
                    },
                ]

                for r_info in remitos_definicion:
                    remito_obj, creado = Remito.objects.get_or_create(
                        numero=r_info["numero"],
                        marca=r_info["marca"],
                        defaults={
                            "comercio": r_info["comercio"],
                            "total": r_info["total"],
                            "estado": EstadoRemito.PENDIENTE,
                            "parada": None,
                            "importacion": None,
                        },
                    )
                    remitos_creados[r_info["numero"]] = remito_obj
                    remitos_creados[(r_info["marca"].cuit, r_info["numero"])] = remito_obj
                    if creado:
                        total_remitos += 1

                # 6.1. Lotes de Importación de Remitos (HU-37, HU-38, HU-40)
                # Lote 1: Exitoso y Descartable (remitos en estado PENDIENTE para probar HU-40)
                lote_descartable, _ = ImportacionRemitos.objects.get_or_create(
                    archivo="importaciones/30709876542_lote_descartable.csv",
                    defaults={
                        "marca": marcas["30709876542"],
                        "cantidad": 2,
                        "estado": EstadoImportacion.EXITO,
                    },
                )
                rem_desc_1 = remitos_creados.get("0090-00025539")
                rem_desc_2 = remitos_creados.get("0090-00003921")
                if rem_desc_1:
                    rem_desc_1.importacion = lote_descartable
                    rem_desc_1.save(update_fields=["importacion"])
                if rem_desc_2:
                    rem_desc_2.importacion = lote_descartable
                    rem_desc_2.save(update_fields=["importacion"])

                # Lote 2: Con Errores / Rechazado (para probar HU-38: detalle de excepciones)
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
            # 7. Itinerario asignado y ruta guardada (Chofer Martín Pérez - 12345678)
            # ------------------------------------------------------------------
            transportista_martin = Transportista.objects.filter(
                usuario__username="12345678"
            ).first()
            itinerario_martin = None
            total_paradas_creadas = 0

            if transportista_martin:
                itinerario_martin, _ = Itinerario.objects.get_or_create(
                    fecha=date.today(),
                    transportista=transportista_martin,
                    defaults={
                        "estado": EstadoItinerario.ASIGNADO,
                        "vehiculo": transportista_martin.vehiculo,
                    },
                )
                itinerario_martin.estado = EstadoItinerario.ASIGNADO
                itinerario_martin.vehiculo = transportista_martin.vehiculo
                itinerario_martin.save()

                comercios_disponibles = [
                    c for c in comercios.values()
                    if c.cuit not in {"23200048148", "23200000145", "23200033191", "23200056655"}
                ]
                paradas_comercios = comercios_disponibles[:5]
                marcas_list = list(marcas.values())
                admin_user = Usuario.objects.filter(username="11111111").first()
                total_cobranzas_creadas = 0

                paradas_config = [
                    {
                        "orden": 1,
                        "estado": EstadoParada.FINALIZADA,
                        "hora_entrega": timezone.now().replace(hour=9, minute=30, second=0),
                        "remito_total": Decimal("150000.00"),
                        "remito_estado": EstadoRemito.ENTREGADO,
                        "cobranza_estado": EstadoCobranza.REGISTRADO,
                        "detalles": [
                            {"medio": MedioPago.EFECTIVO, "declarado": Decimal("100000.00"), "verificado": Decimal("0.00")},
                            {"medio": MedioPago.TRANSFERENCIA, "declarado": Decimal("50000.00"), "verificado": Decimal("0.00")},
                        ],
                        "observacion": None,
                        "ajuste": None,
                    },
                    {
                        "orden": 2,
                        "estado": EstadoParada.FINALIZADA,
                        "hora_entrega": timezone.now().replace(hour=10, minute=15, second=0),
                        "remito_total": Decimal("220000.00"),
                        "remito_estado": EstadoRemito.ENTREGADO,
                        "cobranza_estado": EstadoCobranza.APROBADO,
                        "detalles": [
                            {
                                "medio": MedioPago.QR,
                                "declarado": Decimal("220000.00"),
                                "verificado": Decimal("220000.00"),
                                "mp_payment_id": "MP-8877665544",
                            },
                        ],
                        "observacion": "Cobranza validada y conciliada contra liquidación MP.",
                        "ajuste": None,
                    },
                    {
                        "orden": 3,
                        "estado": EstadoParada.FINALIZADA,
                        "hora_entrega": timezone.now().replace(hour=11, minute=0, second=0),
                        "remito_total": Decimal("310000.00"),
                        "remito_estado": EstadoRemito.ENTREGADO,
                        "cobranza_estado": EstadoCobranza.DIFIERE,
                        "detalles": [
                            {
                                "medio": MedioPago.EFECTIVO,
                                "declarado": Decimal("310000.00"),
                                "verificado": Decimal("300000.00"),
                            },
                        ],
                        "observacion": "Faltante de $10.000 en el sobre de rendición de efectivo.",
                        "ajuste": {
                            "medio": MedioPago.EFECTIVO,
                            "monto": Decimal("10000.00"),
                            "motivo": "Acreditación complementaria por ticket de transferencia bancaria de respaldo.",
                        },
                    },
                    {
                        "orden": 4,
                        "estado": EstadoParada.ERROR,
                        "hora_entrega": None,
                        "remito_total": Decimal("185000.00"),
                        "remito_estado": EstadoRemito.ASIGNADO,
                        "cobranza_estado": None,
                        "problema": {
                            "tipo": TipoProblema.LOCAL_CERRADO,
                            "descripcion": "Local cerrado con persiana baja a las 11:45 hs. Sin respuesta al timbre.",
                            "impide_entrega": True,
                        },
                    },
                    {
                        "orden": 5,
                        "estado": EstadoParada.PENDIENTE,
                        "hora_entrega": None,
                        "cobranza_estado": None,
                        "multimarca": [
                            {"marca_idx": 0, "total": Decimal("75000.00"), "sufijo": "1"},
                            {"marca_idx": 1, "total": Decimal("45000.00"), "sufijo": "2"},
                        ],
                    },
                ]

                for orden_idx, com in enumerate(paradas_comercios, start=1):
                    if not com:
                        continue
                    cfg = paradas_config[orden_idx - 1]
                    parada_obj, _ = Parada.objects.get_or_create(
                        itinerario=itinerario_martin,
                        comercio=com,
                        defaults={
                            "orden": cfg["orden"],
                            "estado": cfg["estado"],
                            "hora_entrega": cfg["hora_entrega"],
                        },
                    )
                    parada_obj.orden = cfg["orden"]
                    parada_obj.estado = cfg["estado"]
                    parada_obj.hora_entrega = cfg["hora_entrega"]
                    parada_obj.save()
                    total_paradas_creadas += 1

                    # Registrar problema/inconveniente operativo si corresponde (HU-56 / HU-18)
                    if cfg.get("problema"):
                        ProblemaParada.objects.filter(parada=parada_obj).delete()
                        p_info = cfg["problema"]
                        ProblemaParada.objects.create(
                            parada=parada_obj,
                            tipo=p_info["tipo"],
                            descripcion=p_info["descripcion"],
                            impide_entrega=p_info["impide_entrega"],
                        )

                    # Asegurar remitos asociados a la parada
                    if cfg.get("multimarca"):
                        # Parada multimarca con múltiples remitos de distintas marcas (HU-25 / HU-36)
                        Remito.objects.filter(parada=parada_obj).delete()
                        for m_info in cfg["multimarca"]:
                            marca_obj = marcas_list[m_info["marca_idx"] % len(marcas_list)]
                            Remito.objects.create(
                                numero=f"0009-0000005{m_info['sufijo']}",
                                marca=marca_obj,
                                comercio=com,
                                total=m_info["total"],
                                estado=EstadoRemito.ASIGNADO,
                                parada=parada_obj,
                            )
                    else:
                        remito_existente = Remito.objects.filter(comercio=com, parada__isnull=True).first()
                        if remito_existente:
                            remito_existente.parada = parada_obj
                            remito_existente.estado = cfg["remito_estado"]
                            remito_existente.total = cfg["remito_total"]
                            remito_existente.save(update_fields=["parada", "estado", "total"])
                        else:
                            remito_existente = Remito.objects.filter(comercio=com, parada=parada_obj).first()
                            if not remito_existente:
                                marca_asignada = marcas_list[(orden_idx - 1) % len(marcas_list)]
                                Remito.objects.create(
                                    numero=f"0009-{str(orden_idx).zfill(8)}",
                                    marca=marca_asignada,
                                    comercio=com,
                                    total=cfg["remito_total"],
                                    estado=cfg["remito_estado"],
                                    parada=parada_obj,
                                )
                            else:
                                remito_existente.estado = cfg["remito_estado"]
                                remito_existente.total = cfg["remito_total"]
                                remito_existente.save(update_fields=["estado", "total"])

                    # Crear cobranza de ejemplo si corresponde a la configuración de la parada
                    if cfg.get("cobranza_estado"):
                        Cobranza.objects.filter(parada=parada_obj).delete()
                        cobranza_obj = Cobranza.objects.create(
                            parada=parada_obj,
                            estado=cfg["cobranza_estado"],
                            observacion=cfg.get("observacion"),
                        )
                        total_cobranzas_creadas += 1

                        for det in cfg["detalles"]:
                            DetallePago.objects.create(
                                cobranza=cobranza_obj,
                                medio=det["medio"],
                                monto_declarado=det["declarado"],
                                monto_verificado=det.get("verificado", Decimal("0.00")),
                                mp_payment_id=det.get("mp_payment_id"),
                            )

                        if cfg.get("ajuste") and conciliacion:
                            ajuste_data = cfg["ajuste"]
                            AjusteCobranza.objects.create(
                                cobranza=cobranza_obj,
                                usuario=conciliacion,
                                medio=ajuste_data["medio"],
                                monto=ajuste_data["monto"],
                                motivo=ajuste_data["motivo"],
                            )

                # Ruta guardada de prueba para validar HU-63, HU-64 y HU-65
                ruta_guardada, _ = RutaGuardada.objects.get_or_create(
                    transportista=transportista_martin,
                    nombre="Ruta Costera 12",
                )
                DetalleRutaGuardada.objects.filter(ruta_guardada=ruta_guardada).delete()
                for p_idx, com in enumerate(paradas_comercios[:3], start=1):
                    if com:
                        DetalleRutaGuardada.objects.create(
                            ruta_guardada=ruta_guardada,
                            comercio=com,
                            prioridad=p_idx,
                        )

            # ------------------------------------------------------------------
            # 8. Itinerario histórico finalizado (Jornada anterior - HU-60 / HU-61)
            # ------------------------------------------------------------------
            itinerario_ayer = None
            if transportista_martin:
                fecha_ayer = date.today() - timedelta(days=1)
                itinerario_ayer, _ = Itinerario.objects.get_or_create(
                    fecha=fecha_ayer,
                    transportista=transportista_martin,
                    defaults={
                        "estado": EstadoItinerario.FINALIZADO,
                        "vehiculo": transportista_martin.vehiculo,
                    },
                )
                itinerario_ayer.estado = EstadoItinerario.FINALIZADO
                itinerario_ayer.vehiculo = transportista_martin.vehiculo
                itinerario_ayer.save()

                paradas_ayer_comercios = comercios_disponibles[5:8]
                for p_ayer_idx, c_ayer in enumerate(paradas_ayer_comercios, start=1):
                    p_ayer_obj, _ = Parada.objects.get_or_create(
                        itinerario=itinerario_ayer,
                        comercio=c_ayer,
                        defaults={
                            "orden": p_ayer_idx,
                            "estado": EstadoParada.FINALIZADA,
                            "hora_entrega": timezone.now().replace(hour=8 + p_ayer_idx, minute=45, second=0),
                        },
                    )
                    p_ayer_obj.estado = EstadoParada.FINALIZADA
                    p_ayer_obj.orden = p_ayer_idx
                    p_ayer_obj.save()

                    rem_ayer = Remito.objects.filter(comercio=c_ayer, parada=p_ayer_obj).first()
                    if not rem_ayer:
                        rem_ayer = Remito.objects.create(
                            numero=f"0008-0000000{p_ayer_idx}",
                            marca=marcas_list[p_ayer_idx % len(marcas_list)],
                            comercio=c_ayer,
                            total=Decimal("110000.00") * p_ayer_idx,
                            estado=EstadoRemito.ENTREGADO,
                            parada=p_ayer_obj,
                        )
                    else:
                        rem_ayer.estado = EstadoRemito.ENTREGADO
                        rem_ayer.save(update_fields=["estado"])

                    Cobranza.objects.filter(parada=p_ayer_obj).delete()
                    cob_ayer = Cobranza.objects.create(
                        parada=p_ayer_obj,
                        estado=EstadoCobranza.APROBADO,
                        observacion="Cobranza histórica aprobada y conciliada.",
                    )
                    DetallePago.objects.create(
                        cobranza=cob_ayer,
                        medio=MedioPago.EFECTIVO,
                        monto_declarado=rem_ayer.total,
                        monto_verificado=rem_ayer.total,
                    )

            # ------------------------------------------------------------------
            # 8.1. Itinerario en curso (Chofer Lucas Rodríguez - 12345680)
            # ------------------------------------------------------------------
            transportista_lucas = Transportista.objects.filter(
                usuario__username="12345680"
            ).first()
            itinerario_en_curso = None
            total_paradas_en_curso = 0

            if transportista_lucas:
                itinerario_en_curso, _ = Itinerario.objects.get_or_create(
                    fecha=date.today(),
                    transportista=transportista_lucas,
                    defaults={
                        "estado": EstadoItinerario.EN_CURSO,
                        "vehiculo": transportista_lucas.vehiculo,
                    },
                )
                itinerario_en_curso.estado = EstadoItinerario.EN_CURSO
                itinerario_en_curso.vehiculo = transportista_lucas.vehiculo
                itinerario_en_curso.save()

                paradas_en_curso_comercios = comercios_disponibles[8:11]
                paradas_en_curso_cfg = [
                    {
                        "orden": 1,
                        "estado": EstadoParada.FINALIZADA,
                        "hora_entrega": timezone.now().replace(hour=10, minute=30, second=0),
                        "remito_total": Decimal("135000.00"),
                        "remito_estado": EstadoRemito.ENTREGADO,
                        "cobranza_estado": EstadoCobranza.REGISTRADO,
                        "detalles": [
                            {"medio": MedioPago.EFECTIVO, "declarado": Decimal("135000.00"), "verificado": Decimal("0.00")},
                        ],
                    },
                    {
                        "orden": 2,
                        "estado": EstadoParada.PENDIENTE,
                        "hora_entrega": None,
                        "remito_total": Decimal("85000.00"),
                        "remito_estado": EstadoRemito.ASIGNADO,
                        "cobranza_estado": None,
                    },
                    {
                        "orden": 3,
                        "estado": EstadoParada.PENDIENTE,
                        "hora_entrega": None,
                        "remito_total": Decimal("112000.00"),
                        "remito_estado": EstadoRemito.ASIGNADO,
                        "cobranza_estado": None,
                    },
                ]

                for p_idx, c_obj in enumerate(paradas_en_curso_comercios, start=1):
                    if not c_obj:
                        continue
                    cfg_ec = paradas_en_curso_cfg[p_idx - 1]
                    p_obj, _ = Parada.objects.get_or_create(
                        itinerario=itinerario_en_curso,
                        comercio=c_obj,
                        defaults={
                            "orden": cfg_ec["orden"],
                            "estado": cfg_ec["estado"],
                            "hora_entrega": cfg_ec["hora_entrega"],
                        },
                    )
                    p_obj.orden = cfg_ec["orden"]
                    p_obj.estado = cfg_ec["estado"]
                    p_obj.hora_entrega = cfg_ec["hora_entrega"]
                    p_obj.save()
                    total_paradas_en_curso += 1

                    rem_ec = Remito.objects.filter(comercio=c_obj, parada=p_obj).first()
                    if not rem_ec:
                        Remito.objects.create(
                            numero=f"0010-{str(p_idx).zfill(8)}",
                            marca=marcas_list[p_idx % len(marcas_list)],
                            comercio=c_obj,
                            total=cfg_ec["remito_total"],
                            estado=cfg_ec["remito_estado"],
                            parada=p_obj,
                        )
                    else:
                        rem_ec.estado = cfg_ec["remito_estado"]
                        rem_ec.total = cfg_ec["remito_total"]
                        rem_ec.save(update_fields=["estado", "total"])

                    if cfg_ec.get("cobranza_estado"):
                        Cobranza.objects.filter(parada=p_obj).delete()
                        cob_ec = Cobranza.objects.create(
                            parada=p_obj,
                            estado=cfg_ec["cobranza_estado"],
                            observacion="Cobranza de parada en curso registrada por chofer.",
                        )
                        for d_ec in cfg_ec["detalles"]:
                            DetallePago.objects.create(
                                cobranza=cob_ec,
                                medio=d_ec["medio"],
                                monto_declarado=d_ec["declarado"],
                                monto_verificado=d_ec.get("verificado", Decimal("0.00")),
                            )

            # ------------------------------------------------------------------
            # 8.2. Itinerario eliminable de prueba (HU-48 Happy Path - Sin cobranzas)
            # ------------------------------------------------------------------
            itinerario_eliminable, _ = Itinerario.objects.get_or_create(
                fecha=date.today() + timedelta(days=1),
                transportista=transportista_lucas,
                defaults={
                    "estado": EstadoItinerario.ASIGNADO,
                    "vehiculo": transportista_lucas.vehiculo if transportista_lucas else None,
                },
            )
            itinerario_eliminable.estado = EstadoItinerario.ASIGNADO
            itinerario_eliminable.save()
            comercio_el = comercios.get("27200002143")
            if comercio_el:
                Parada.objects.get_or_create(
                    itinerario=itinerario_eliminable,
                    comercio=comercio_el,
                    defaults={
                        "orden": 1,
                        "estado": EstadoParada.PENDIENTE,
                    },
                )

            # ------------------------------------------------------------------
            # 9. Flujo Completo: Itinerario, Paradas y Cobranza para usuario 1234567
            # ------------------------------------------------------------------
            itinerario_creado = None
            total_paradas_completo = 0
            total_cobranzas_completo = 0

            if options["completo"]:
                chofer_user = Usuario.objects.filter(username="1234567").first()
                if not chofer_user:
                    self.stdout.write(
                        self.style.ERROR("No se encontró el usuario 1234567.")
                    )
                else:
                    transportista_1234567 = getattr(
                        chofer_user, "perfil_transportista", None
                    )
                    vehiculo_1234567 = (
                        transportista_1234567.vehiculo if transportista_1234567 else None
                    )

                    hoy = timezone.now().date()
                    itinerario_creado = Itinerario.objects.create(
                        fecha=hoy,
                        estado=EstadoItinerario.ASIGNADO,
                        transportista=transportista_1234567,
                        vehiculo=vehiculo_1234567,
                    )

                    # Parada 1: Comercio "23200048148" (pendiente de entrega)
                    comercio_1 = comercios["23200048148"]
                    parada_1 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_1,
                        orden=1,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_completo += 1

                    remito_1 = remitos_creados.get("0005-00024715")
                    if remito_1:
                        remito_1.parada = parada_1
                        remito_1.estado = EstadoRemito.ASIGNADO
                        remito_1.save(update_fields=["parada", "estado"])

                        cobranza_1 = Cobranza.objects.create(
                            parada=parada_1,
                            estado=EstadoCobranza.REGISTRADO,
                        )
                        # Pago con 2 medios (efectivo y transferencia)
                        monto_efectivo = Decimal("150000.00")
                        monto_transferencia = remito_1.total - monto_efectivo

                        DetallePago.objects.create(
                            cobranza=cobranza_1,
                            medio=MedioPago.EFECTIVO,
                            monto_declarado=monto_efectivo,
                            monto_verificado=None,
                        )
                        DetallePago.objects.create(
                            cobranza=cobranza_1,
                            medio=MedioPago.TRANSFERENCIA,
                            monto_declarado=monto_transferencia,
                            monto_verificado=None,
                        )
                        total_cobranzas_completo += 1

                    # Parada 2: Comercio "23200000145" (finalizada con cobranza registrada / pendiente de validación)
                    # Este comercio tiene dos remitos: 0090-00015378 y 0090-00003901
                    comercio_2 = comercios["23200000145"]
                    parada_2 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_2,
                        orden=2,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_completo += 1

                    remito_2a = remitos_creados.get("0090-00015378")
                    remito_2b = remitos_creados.get("0090-00003901")
                    total_monto_parada_2 = Decimal("0.00")

                    if remito_2a:
                        remito_2a.parada = parada_2
                        remito_2a.estado = EstadoRemito.ASIGNADO
                        remito_2a.save(update_fields=["parada", "estado"])

                    if remito_2b:
                        remito_2b.parada = parada_2
                        remito_2b.estado = EstadoRemito.ASIGNADO
                        remito_2b.save(update_fields=["parada", "estado"])
                        total_monto_parada_2 += remito_2b.total

                    if total_monto_parada_2 > Decimal("0.00"):
                        cobranza_2 = Cobranza.objects.create(
                            parada=parada_2,
                            estado=EstadoCobranza.REGISTRADO,
                        )
                        DetallePago.objects.create(
                            cobranza=cobranza_2,
                            medio=MedioPago.TRANSFERENCIA,
                            monto_declarado=total_monto_parada_2,
                            monto_verificado=None,
                        )
                        total_cobranzas_completo += 1

                    # Parada 3: Comercio "23200033191" (pendiente de entrega)
                    comercio_3 = comercios["23200033191"]
                    parada_3 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_3,
                        orden=3,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_completo += 1

                    remito_3 = remitos_creados.get("0002-00023458")
                    if remito_3:
                        remito_3.parada = parada_3
                        remito_3.estado = EstadoRemito.ASIGNADO
                        remito_3.save(update_fields=["parada", "estado"])

                    # Parada 4: Comercio "23200056655" (pendiente de entrega, con 2 remitos)
                    comercio_4 = comercios["23200056655"]
                    parada_4 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_4,
                        orden=4,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_completo += 1

                    remito_4a = remitos_creados.get("0002-00023496")
                    remito_4b = remitos_creados.get("0090-00015345")
                    if remito_4a:
                        remito_4a.parada = parada_4
                        remito_4a.estado = EstadoRemito.ASIGNADO
                        remito_4a.save(update_fields=["parada", "estado"])
                    if remito_4b:
                        remito_4b.parada = parada_4
                        remito_4b.estado = EstadoRemito.ASIGNADO
                        remito_4b.save(update_fields=["parada", "estado"])

                    # Ruta guardada de prueba para usuario 1234567 (HU-63, HU-64, HU-65)
                    ruta_guardada_lautaro, _ = RutaGuardada.objects.get_or_create(
                        transportista=transportista_1234567,
                        nombre="Ruta Rapida Alternativa",
                    )
                    DetalleRutaGuardada.objects.filter(ruta_guardada=ruta_guardada_lautaro).delete()
                    for idx_r, com_r in enumerate([comercio_1, comercio_2, comercio_3, comercio_4], start=1):
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
        if cargar_remitos:
            self.stdout.write(
                f"  • Remitos cargados: {len(remitos_definicion)} ({total_remitos} nuevos)"
            )
        else:
            self.stdout.write("  • Remitos cargados: 0 (use --con-remitos o --completo para cargarlos)")

        if options["completo"]:
            self.stdout.write(
                f"  • Itinerario asignado a 1234567: ID #{itinerario_creado.id if itinerario_creado else 'N/A'} con {total_paradas_completo} paradas."
            )
            self.stdout.write(
                f"  • Cobranzas registradas: {total_cobranzas_completo}."
            )
        else:
            self.stdout.write(
                "  • Chofer 1234567: Sin itinerario asignado (use --completo para generarlo)"
            )

        if itinerario_martin:
            self.stdout.write(
                f"  • Itinerario asignado (Hoy): #{itinerario_martin.id} con {total_paradas_creadas} paradas para Chofer Martín Pérez"
            )
            self.stdout.write(
                "  • Ruta guardada de prueba: 'Ruta Costera 12' (3 comercios)"
            )
            self.stdout.write(
                f"  • Cobranzas de ejemplo: {total_cobranzas_creadas} cobranzas registradas (1 Registrada, 1 Aprobada, 1 Difiere con Ajuste auditado por 22222222)"
            )
        if itinerario_en_curso:
            self.stdout.write(
                f"  • Itinerario en curso (Hoy): #{itinerario_en_curso.id} con {total_paradas_en_curso} paradas para Chofer Lucas Rodríguez"
            )
        if itinerario_ayer:
            self.stdout.write(
                f"  • Itinerario histórico (Ayer): #{itinerario_ayer.id} cerrado/finalizado con 3 paradas y cobranzas aprobadas"
            )

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
        self.stdout.write("   • Chofer 1 (Activo Completo): DNI 1234567  | Clave: 123 | Lautaro Gómez | Vehículo: AF123CD")
        self.stdout.write("     - Itinerario de hoy con 4 paradas (2 finalizadas con cobranza, 2 pendientes de entrega en calle).")
        self.stdout.write("     - Ruta guardada: 'Ruta Rapida Alternativa'.")
        self.stdout.write("   • Chofer 2 (Completo Avanzado): DNI 12345678 | Clave: 123 | Martín Pérez  | Vehículo: AG456EF")
        self.stdout.write("     - Itinerario de hoy con 5 paradas (1 registrada, 1 aprobada, 1 difiere con ajuste auditado, 1 error local cerrado, 1 Consolidación Multimarca).")
        self.stdout.write("     - Ruta guardada: 'Ruta Costera 12'.")
        self.stdout.write("   • Chofer 3 (Bloqueado/Suspendido): DNI 12345679 | Clave: 123 | Carlos Bloqueado (Para probar desbloqueo HU-11 / HU-66).")
        self.stdout.write("   • Chofer 4 (En Curso): DNI 12345680 | Clave: 123 | Lucas Rodríguez | Vehículo: AD345JK (Itinerario en curso HU-60).")
        self.stdout.write("   • Chofer 5 (Sin Ruta - Caso de Borde): DNI 12345681 | Clave: 123 | Esteban Suplente (Sin itinerario asignado HU-62).")

        self.stdout.write(self.style.WARNING("\n3. Lotes de Importación y Remitos"))
        self.stdout.write("   • Lote Descartable (HU-40) : Snacks Andinos S.R.L. con remitos PENDIENTES (eliminable sin trabas).")
        self.stdout.write("   • Lote Rechazado (HU-38)   : Gaseosas del Sur S.A. con errores de fila registrados para auditoría.")
        self.stdout.write("   • Remitos Clave Compuesta  : #0001-00099999 (coexiste en Cervecería La Diagonal y Snacks Andinos).")

        self.stdout.write(self.style.WARNING("\n4. Itinerarios y Trazabilidad"))
        self.stdout.write("   • Itinerario de Hoy (Activo)     : Asignado a Lautaro Gómez (#" + str(itinerario_creado.id if itinerario_creado else 'N/A') + ") y Martín Pérez.")
        self.stdout.write("   • Itinerario Eliminable (HU-48)  : Hoja de ruta para mañana asignada a Lucas Rodríguez (sin cobranzas, eliminable).")
        self.stdout.write("   • Itinerario Histórico (Inmutable): Finalizado ayer para Martín Pérez (controles deshabilitados, protegido).")

        self.stdout.write(
            self.style.HTTP_INFO("=" * 70 + "\n")
        )
