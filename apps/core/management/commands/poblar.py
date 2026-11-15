# apps/core/management/commands/poblar_db.py

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cobranza.models import Cobranza, DetallePago
from apps.core.models import EstadoVehiculo, Grupos, Transportista, Vehiculo
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    Itinerario,
    Parada,
    RutaGuardada,
)
from apps.remitos.models import (
    Comercio,
    EstadoRemito,
    Marca,
    Remito,
)

Usuario = get_user_model()


class Command(BaseCommand):
    help = (
        "Carga datos maestros (Superusuario, Vehículos, Usuarios Chofer, Marcas, Comercios) "
        "y opcionalmente Remitos PENDIENTES."
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

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando la carga de datos de prueba..."))

        with transaction.atomic():
            if options["limpiar"]:
                self.stdout.write("Limpiando datos existentes...")

                # 1. Pagos y Cobranzas (evita ProtectedError en Cobranza.parada)
                DetallePago.objects.all().delete()
                Cobranza.objects.all().delete()

                # 2. Tablas intermedias e hijas de rutas
                DetalleRutaGuardada.objects.all().delete()
                RutaGuardada.objects.all().delete()

                # 3. Remitos y Paradas
                Remito.objects.all().delete()
                Parada.objects.all().delete()

                # 4. Itinerarios (libera la referencia protegida a Transportista)
                Itinerario.objects.all().delete()

                # 5. Comercios y Marcas
                Comercio.objects.all().delete()
                Marca.objects.all().delete()

                # 6. Perfiles y Vehículos
                Transportista.objects.all().delete()
                Vehiculo.objects.all().delete()

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
                },
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.set_password("123")
            admin_user.save()

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
                    "telefono": "1143401000",
                    "email": "ventas@cervecerialadiagonal.com.ar",
                    "activo": True,
                },
                {
                    "nombre": "Snacks Andinos S.R.L.",
                    "cuit": "30709876542",
                    "telefono": "1147083000",
                    "email": "distribucion@snacksandinos.com.ar",
                    "activo": True,
                },
                {
                    "nombre": "Gaseosas del Sur S.A.",
                    "cuit": "30712345671",
                    "telefono": "1143657000",
                    "email": "pedidos@gaseosasdelsur.com.ar",
                    "activo": True,
                },
                {
                    "nombre": "Lacteos El Tambo S.A.",
                    "cuit": "33698712347",
                    "telefono": "1147084000",
                    "email": "contacto@lacteoseltambo.com.ar",
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
            ]

            comercios = {}
            for c_data in comercios_data:
                comercio, _ = Comercio.objects.get_or_create(
                    cuit=c_data["cuit"], defaults=c_data
                )
                comercios[c_data["cuit"]] = comercio

            # ------------------------------------------------------------------
            # 6. Remitos PENDIENTES (opcional mediante --con-remitos)
            # ------------------------------------------------------------------
            total_remitos = 0
            if options["con_remitos"]:
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
                    _, creado = Remito.objects.get_or_create(
                        numero=r_info["numero"],
                        defaults={
                            "marca": r_info["marca"],
                            "comercio": r_info["comercio"],
                            "total": r_info["total"],
                            "estado": EstadoRemito.PENDIENTE,
                            "parada": None,
                            "importacion": None,
                            "eliminado": False,
                        },
                    )
                    if creado:
                        total_remitos += 1

        self.stdout.write(
            self.style.SUCCESS("✓ Datos maestros cargados exitosamente.")
        )
        self.stdout.write("  • Superusuario: 11111111 (clave: 123)")
        self.stdout.write(f"  • Comercios: {len(comercios_data)}")
        self.stdout.write(f"  • Marcas: {len(marcas_data)}")
        if options["con_remitos"]:
            self.stdout.write(
                f"  • Remitos PENDIENTES: {len(remitos_definicion)} ({total_remitos} nuevos)"
            )
        else:
            self.stdout.write("  • Remitos PENDIENTES: 0 (use --con-remitos para cargarlos)")
        self.stdout.write(
            "  • Itinerarios y Paradas: Ninguno creado (quedan para generar en el flujo de asignación)"
        )
