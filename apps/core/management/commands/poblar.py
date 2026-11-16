# apps/core/management/commands/poblar_db.py

from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from datetime import date

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

        # Asegurar que existan todos los grupos y permisos del sistema
        call_command("crear_grupos", stdout=StringIO())

        with transaction.atomic():
            if options["limpiar"]:
                self.stdout.write("Limpiando datos existentes...")

                # 1. Pagos y Cobranzas (evita ProtectedError en Cobranza.parada)
                AjusteCobranza.objects.all().delete()
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

                # Desbloquear todos los usuarios (superusuario y regulares)
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
                user.is_active = True
                user.intentos_fallidos = 0
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
                        "numero": "0002-00015378",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200039289"],
                        "total": Decimal("475923.72"),
                    },
                    {
                        "numero": "0006-00025539",
                        "marca": marcas["30709876542"],
                        "comercio": comercios["23200042867"],
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
                        "comercio": comercios["23200039289"],
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
                        "comercio": comercios["23200058011"],
                        "total": Decimal("353247.34"),
                    },
                    {
                        "numero": "0006-00028378",
                        "marca": marcas["33698712347"],
                        "comercio": comercios["23200060768"],
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

            # ------------------------------------------------------------------
            # 7. Itinerario activo y ruta guardada (Chofer Martín Pérez - 12345678)
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

                paradas_comercios = list(comercios.values())[:5]
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
                        "estado": EstadoParada.PENDIENTE,
                        "hora_entrega": None,
                        "remito_total": Decimal("185000.00"),
                        "remito_estado": EstadoRemito.ASIGNADO,
                        "cobranza_estado": None,
                    },
                    {
                        "orden": 5,
                        "estado": EstadoParada.PENDIENTE,
                        "hora_entrega": None,
                        "remito_total": Decimal("92500.00"),
                        "remito_estado": EstadoRemito.ASIGNADO,
                        "cobranza_estado": None,
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

                    # Asegurar remito asociado a la parada
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

                        if cfg.get("ajuste") and admin_user:
                            ajuste_data = cfg["ajuste"]
                            AjusteCobranza.objects.create(
                                cobranza=cobranza_obj,
                                usuario=admin_user,
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

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("✓ Datos maestros cargados exitosamente.")
        )
        self.stdout.write("  • Superusuario: 11111111 (clave: 123)")
        self.stdout.write(f"  • Comercios: {len(comercios_data)}")
        self.stdout.write(f"  • Marcas: {len(marcas_data)}")
        if options["con_remitos"]:
            self.stdout.write(
                f"  • Remitos cargados: {len(remitos_definicion)} ({total_remitos} nuevos)"
            )
        else:
            self.stdout.write("  • Remitos cargados: 0 (use --con-remitos para cargarlos)")
        if itinerario_martin:
            self.stdout.write(
                f"  • Itinerario activo: #{itinerario_martin.id} con {total_paradas_creadas} paradas para Chofer Martín Pérez"
            )
            self.stdout.write(
                "  • Ruta guardada de prueba: 'Ruta Costera 12' (3 comercios)"
            )
            self.stdout.write(
                f"  • Cobranzas de ejemplo: {total_cobranzas_creadas} cobranzas registradas (1 Registrada, 1 Aprobada, 1 Difiere con Ajuste)"
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

        self.stdout.write(self.style.WARNING("\n1. Superusuario (Administrador con todos los roles)"))
        self.stdout.write("   • DNI / Usuario : 11111111")
        self.stdout.write("   • Contraseña    : 123")
        self.stdout.write("   • Roles         : Todos (Planificación, Conciliación, Gestión de Personal, Transportista)")
        self.stdout.write("   • Caso de prueba: Acceso completo a todos los módulos del panel administrativo web.")

        self.stdout.write(self.style.WARNING("\n2. Transportistas (Choferes - App Móvil / Rutas)"))
        self.stdout.write("   • Chofer 1: DNI 1234567  | Clave: 123 | Lautaro Gómez | Vehículo: AF123CD (Mercedes-Benz Accelo 815)")
        self.stdout.write("     - Caso de prueba: Transportista sin itinerario asignado (estado vacío institucional).")
        self.stdout.write("   • Chofer 2: DNI 12345678 | Clave: 123 | Martín Pérez  | Vehículo: AG456EF (Iveco Daily 70C17)")
        self.stdout.write("     - Caso de prueba: Itinerario activo asignado con 5 paradas (3 completadas/cobradas, 2 pendientes) y ruta guardada 'Ruta Costera 12'.")
        self.stdout.write("     - Flujo de prueba: Login -> /itinerario -> Reordenar paradas -> Guardar orden -> Rutas guardadas.")

        self.stdout.write(self.style.WARNING("\n3. Flota de Vehículos"))
        self.stdout.write("   • Asignados : AF123CD, AG456EF (a choferes de prueba)")
        self.stdout.write("   • Disponible: AE789GH (Ford Cargo 915) -> Caso de prueba: Asignación a nuevo chofer.")

        self.stdout.write(self.style.WARNING("\n4. Logística y Planificación de Itinerarios (Remitos Pendientes)"))
        self.stdout.write("   • Caso Consolidación Multimarca (mismo comercio, varias marcas):")
        self.stdout.write("     - Supermercado Los Hermanos : 2 remitos (Quilmes + Molinos)")
        self.stdout.write("     - Almacén Don Tito          : 2 remitos (Quilmes + Arcor)")
        self.stdout.write("     - Minimercado San Jorge     : 2 remitos (Molinos + Arcor)")
        self.stdout.write("     -> Caso de prueba: Probar consolidación automática/manual de marcas en una misma parada.")
        self.stdout.write("   • Caso Entregas Individuales:")
        self.stdout.write("     - Autoservicio El Sol       : 1 remito (Molinos)")
        self.stdout.write("     - Kiosco Open 25            : 1 remito (Arcor)")
        self.stdout.write("     - Distribuidora Mitre SRL   : 1 remito (Quilmes)")
        if options["con_remitos"]:
            self.stdout.write(
                f"   • Total: {len(remitos_definicion)} remitos ({total_remitos} nuevos), {len(comercios_data)} comercios, {len(marcas_data)} marcas."
            )
        else:
            self.stdout.write("   • Remitos pendientes no generados (use el flag --con-remitos para cargarlos).")
        if itinerario_martin:
            self.stdout.write(
                f"   • Itinerario activo de prueba: #{itinerario_martin.id} (5 paradas) asignado a Chofer Martín Pérez (12345678)."
            )

        self.stdout.write(self.style.WARNING("\n5. Módulo de Cobranzas y Conciliación (Panel Administrativo Web)"))
        self.stdout.write("   • Cobranza Registrada (Pendiente)  : Parada #1 - Declarada por chofer ($150.000). Lista para arqueo y validación (botón 'Validar').")
        self.stdout.write("   • Cobranza Aprobada (Conciliada)   : Parada #2 - Validada con QR de Mercado Pago ($220.000).")
        self.stdout.write("   • Cobranza con Diferencia (Difiere): Parada #3 - Declarado $310.000, verificado $300.000 (faltante de $10.000) con Ajuste complementario registrado.")
        self.stdout.write(
            self.style.HTTP_INFO("=" * 70 + "\n")
        )

