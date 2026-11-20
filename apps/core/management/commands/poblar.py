# apps/core/management/commands/poblar_db.py

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

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
)
from apps.remitos.models import (
    Comercio,
    ErrorImportacion,
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

                # 8. Usuarios no superusuarios
                Usuario.objects.filter(is_superuser=False).delete()

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

            for grupo_nombre in Grupos.values:
                grp, _ = Group.objects.get_or_create(name=grupo_nombre)
                admin_user.groups.add(grp)
            admin_user.save()

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
                },
                {
                    "username": "12345678",
                    "first_name": "Martín",
                    "last_name": "Pérez",
                    "telefono": "5491155557777",
                    "vehiculo": vehiculos["AG456EF"],
                },
            ]

            grupo_transportista, _ = Group.objects.get_or_create(name=Grupos.TRANSPORTISTA)
            for c_data in choferes_data:
                v = c_data.pop("vehiculo")
                user, _ = Usuario.objects.get_or_create(
                    username=c_data["username"],
                    defaults={
                        "first_name": c_data["first_name"],
                        "last_name": c_data["last_name"],
                        "telefono": c_data["telefono"],
                        "is_active": True,
                    },
                )
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
                {
                    "nombre": "Inactiva Prueba",
                    "cuit": "30999999991",
                    "activo": False,
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
                        "comercio": comercios["23200033191"],
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
                        "numero": "0002-00015378",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200000145"],
                        "total": Decimal("475923.72"),
                    },
                    {
                        "numero": "0006-00025539",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["20200022190"],
                        "total": Decimal("692074.74"),
                    },
                    {
                        "numero": "0005-00015345",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200056655"],
                        "total": Decimal("671210.29"),
                    },
                    # Gaseosas del Sur S.A. (30712345671)
                    {
                        "numero": "0004-00003901",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["23200000145"],
                        "total": Decimal("733385.18"),
                    },
                    {
                        "numero": "0004-00003921",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["30200025527"],
                        "total": Decimal("492487.48"),
                    },
                    {
                        "numero": "0002-00033994",
                        "marca": marcas["30712345671"],
                        "comercio": comercios["23200063767"],
                        "total": Decimal("334706.88"),
                    },
                    # Lacteos El Tambo S.A. (33698712347)
                    {
                        "numero": "0006-00028325",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200063767"],
                        "total": Decimal("526471.00"),
                    },
                    {
                        "numero": "0005-00010362",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["20200070268"],
                        "total": Decimal("353247.34"),
                    },
                    {
                        "numero": "0006-00028378",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200008855"],
                        "total": Decimal("609129.43"),
                    },
                ]

                for r_info in remitos_definicion:
                    remito_obj, creado = Remito.objects.get_or_create(
                        numero=r_info["numero"],
                        defaults={
                            "marca": r_info["marca"],
                            "comercio": r_info["comercio"],
                            "total": r_info["total"],
                            "estado": EstadoRemito.PENDIENTE,
                            "parada": None,
                            "importacion": None,
                        },
                    )
                    remitos_creados[r_info["numero"]] = remito_obj
                    if creado:
                        total_remitos += 1

            # ------------------------------------------------------------------
            # 7. Flujo Completo: Itinerario, Paradas y Cobranza para usuario 1234567
            # ------------------------------------------------------------------
            itinerario_creado = None
            total_paradas_creadas = 0
            total_cobranzas_creadas = 0

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
                    total_paradas_creadas += 1

                    remito_1 = remitos_creados.get("0005-00024715")
                    if remito_1:
                        remito_1.parada = parada_1
                        remito_1.estado = EstadoRemito.ASIGNADO
                        remito_1.save(update_fields=["parada", "estado"])

                    # Parada 2: Comercio "23200000145" (pendiente de entrega)
                    # Este comercio tiene dos remitos: 0002-00015378 ($475923.72) y 0004-00003901 ($733385.18)
                    comercio_2 = comercios["23200000145"]
                    parada_2 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_2,
                        orden=2,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_creadas += 1

                    remito_2a = remitos_creados.get("0002-00015378")
                    remito_2b = remitos_creados.get("0004-00003901")

                    if remito_2a:
                        remito_2a.parada = parada_2
                        remito_2a.estado = EstadoRemito.ASIGNADO
                        remito_2a.save(update_fields=["parada", "estado"])

                    if remito_2b:
                        remito_2b.parada = parada_2
                        remito_2b.estado = EstadoRemito.ASIGNADO
                        remito_2b.save(update_fields=["parada", "estado"])

                    # Parada 3: Comercio "23200033191" (pendiente de entrega)
                    comercio_3 = comercios["23200033191"]
                    parada_3 = Parada.objects.create(
                        itinerario=itinerario_creado,
                        comercio=comercio_3,
                        orden=3,
                        estado=EstadoParada.PENDIENTE,
                    )
                    total_paradas_creadas += 1

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
                    total_paradas_creadas += 1

                    remito_4a = remitos_creados.get("0002-00023496")
                    remito_4b = remitos_creados.get("0005-00015345")
                    if remito_4a:
                        remito_4a.parada = parada_4
                        remito_4a.estado = EstadoRemito.ASIGNADO
                        remito_4a.save(update_fields=["parada", "estado"])
                    if remito_4b:
                        remito_4b.parada = parada_4
                        remito_4b.estado = EstadoRemito.ASIGNADO
                        remito_4b.save(update_fields=["parada", "estado"])

                    # ----------------------------------------------------------
                    # Itinerario 2: En curso (asignado a 12345678 - Martín Pérez)
                    # ----------------------------------------------------------
                    chofer_2 = Usuario.objects.filter(username="12345678").first()
                    transportista_12345678 = (
                        getattr(chofer_2, "perfil_transportista", None) if chofer_2 else None
                    )
                    vehiculo_12345678 = (
                        transportista_12345678.vehiculo if transportista_12345678 else None
                    )

                    itinerario_en_curso = Itinerario.objects.create(
                        fecha=hoy,
                        estado=EstadoItinerario.EN_CURSO,
                        transportista=transportista_12345678,
                        vehiculo=vehiculo_12345678,
                    )

                    # Parada 1 del itinerario en curso: Comercio 20200022190
                    comercio_ic_1 = comercios.get("20200022190")
                    if comercio_ic_1:
                        parada_ic_1 = Parada.objects.create(
                            itinerario=itinerario_en_curso,
                            comercio=comercio_ic_1,
                            orden=1,
                            estado=EstadoParada.FINALIZADA,
                            hora_entrega=timezone.now(),
                        )
                        total_paradas_creadas += 1

                        remito_ic_1 = remitos_creados.get("0006-00025539")
                        if remito_ic_1:
                            remito_ic_1.parada = parada_ic_1
                            remito_ic_1.estado = EstadoRemito.ENTREGADO
                            remito_ic_1.save(update_fields=["parada", "estado"])

                            cobranza_ic_1 = Cobranza.objects.create(
                                parada=parada_ic_1,
                                estado=EstadoCobranza.REGISTRADO,
                            )
                            DetallePago.objects.create(
                                cobranza=cobranza_ic_1,
                                medio=MedioPago.EFECTIVO,
                                monto_declarado=remito_ic_1.total,
                                monto_verificado=None,
                            )
                            total_cobranzas_creadas += 1

                    # Parada 2 del itinerario en curso: Comercio 30200025527 (pendiente)
                    comercio_ic_2 = comercios.get("30200025527")
                    if comercio_ic_2:
                        parada_ic_2 = Parada.objects.create(
                            itinerario=itinerario_en_curso,
                            comercio=comercio_ic_2,
                            orden=2,
                            estado=EstadoParada.PENDIENTE,
                        )
                        total_paradas_creadas += 1

                        remito_ic_2 = remitos_creados.get("0004-00003921")
                        if remito_ic_2:
                            remito_ic_2.parada = parada_ic_2
                            remito_ic_2.estado = EstadoRemito.ASIGNADO
                            remito_ic_2.save(update_fields=["parada", "estado"])

                    # ----------------------------------------------------------
                    # Itinerario 3: Finalizado (del día de ayer, asignado a 1234567)
                    # ----------------------------------------------------------
                    ayer = hoy - timezone.timedelta(days=1)
                    itinerario_finalizado = Itinerario.objects.create(
                        fecha=ayer,
                        estado=EstadoItinerario.FINALIZADO,
                        transportista=transportista_1234567,
                        vehiculo=vehiculo_1234567,
                    )

                    # Parada 1 del itinerario finalizado: Comercio 23200063767 (con 2 remitos entregados)
                    comercio_fin_1 = comercios.get("23200063767")
                    if comercio_fin_1:
                        parada_fin_1 = Parada.objects.create(
                            itinerario=itinerario_finalizado,
                            comercio=comercio_fin_1,
                            orden=1,
                            estado=EstadoParada.FINALIZADA,
                            hora_entrega=timezone.now() - timezone.timedelta(days=1, hours=3),
                        )
                        total_paradas_creadas += 1

                        remito_fin_1a = remitos_creados.get("0002-00033994")
                        remito_fin_1b = remitos_creados.get("0006-00028325")
                        monto_parada_fin_1 = Decimal("0.00")

                        if remito_fin_1a:
                            remito_fin_1a.parada = parada_fin_1
                            remito_fin_1a.estado = EstadoRemito.ENTREGADO
                            remito_fin_1a.save(update_fields=["parada", "estado"])
                            monto_parada_fin_1 += remito_fin_1a.total

                        if remito_fin_1b:
                            remito_fin_1b.parada = parada_fin_1
                            remito_fin_1b.estado = EstadoRemito.ENTREGADO
                            remito_fin_1b.save(update_fields=["parada", "estado"])
                            monto_parada_fin_1 += remito_fin_1b.total

                        if monto_parada_fin_1 > Decimal("0.00"):
                            cobranza_fin_1 = Cobranza.objects.create(
                                parada=parada_fin_1,
                                estado=EstadoCobranza.REGISTRADO,
                            )
                            # Pago dividido: 50% Efectivo, 50% Transferencia
                            monto_efectivo = (monto_parada_fin_1 / Decimal("2.00")).quantize(Decimal("0.01"))
                            monto_transf = monto_parada_fin_1 - monto_efectivo
                            DetallePago.objects.create(
                                cobranza=cobranza_fin_1,
                                medio=MedioPago.EFECTIVO,
                                monto_declarado=monto_efectivo,
                                monto_verificado=None,
                            )
                            DetallePago.objects.create(
                                cobranza=cobranza_fin_1,
                                medio=MedioPago.TRANSFERENCIA,
                                monto_declarado=monto_transf,
                                monto_verificado=None,
                            )
                            total_cobranzas_creadas += 1

                    # Parada 2 del itinerario finalizado: Comercio 20200070268
                    comercio_fin_2 = comercios.get("20200070268")
                    if comercio_fin_2:
                        parada_fin_2 = Parada.objects.create(
                            itinerario=itinerario_finalizado,
                            comercio=comercio_fin_2,
                            orden=2,
                            estado=EstadoParada.FINALIZADA,
                            hora_entrega=timezone.now() - timezone.timedelta(days=1, hours=2),
                        )
                        total_paradas_creadas += 1

                        remito_fin_2 = remitos_creados.get("0005-00010362")
                        if remito_fin_2:
                            remito_fin_2.parada = parada_fin_2
                            remito_fin_2.estado = EstadoRemito.ENTREGADO
                            remito_fin_2.save(update_fields=["parada", "estado"])

                            cobranza_fin_2 = Cobranza.objects.create(
                                parada=parada_fin_2,
                                estado=EstadoCobranza.REGISTRADO,
                            )
                            DetallePago.objects.create(
                                cobranza=cobranza_fin_2,
                                medio=MedioPago.TRANSFERENCIA,
                                monto_declarado=remito_fin_2.total,
                                monto_verificado=None,
                            )
                            total_cobranzas_creadas += 1

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
            self.stdout.write("  • Remitos: 0 (use --con-remitos o --completo para cargarlos)")

        if options["completo"]:
            self.stdout.write(
                f"  • Itinerarios creados: asignado (ID #{itinerario_creado.id if itinerario_creado else 'N/A'}), en curso (ID #{itinerario_en_curso.id if 'itinerario_en_curso' in locals() else 'N/A'}) y finalizado (ID #{itinerario_finalizado.id if 'itinerario_finalizado' in locals() else 'N/A'}) con {total_paradas_creadas} paradas en total."
            )
            self.stdout.write(
                f"  • Cobranzas registradas: {total_cobranzas_creadas}."
            )
        else:
            self.stdout.write(
                "  • Itinerarios y Paradas: Ninguno creado (use --completo para generarlos)"
            )
