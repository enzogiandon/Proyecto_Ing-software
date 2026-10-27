# apps/core/management/commands/poblar_db.py

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cobranza.models import Cobranza, DetallePago
from apps.core.models import EstadoVehiculo, Roles, Transportista, Vehiculo
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
        "Carga datos maestros (Vehículos, Usuarios Chofer, Marcas, Comercios) "
        "y Remitos PENDIENTES."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Elimina los datos de prueba anteriores antes de cargar.",
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

            # ------------------------------------------------------------------
            # 1. Vehículos
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
            # 2. Usuarios y Perfiles Transportista
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

            for c_data in choferes_data:
                v = c_data.pop("vehiculo")
                user, _ = Usuario.objects.get_or_create(
                    username=c_data["username"],
                    defaults={
                        "first_name": c_data["first_name"],
                        "last_name": c_data["last_name"],
                        "telefono": c_data["telefono"],
                        "rol": Roles.TRANSPORTISTA,
                        "is_active": True,
                    },
                )
                user.set_password("chofer123")
                user.save()

                transportista, _ = Transportista.objects.get_or_create(
                    usuario=user,
                    defaults={"vehiculo": v},
                )
                if transportista.vehiculo != v:
                    transportista.vehiculo = v
                    transportista.save(update_fields=["vehiculo"])

            # ------------------------------------------------------------------
            # 3. Marcas
            # ------------------------------------------------------------------
            marcas_data = [
                {
                    "nombre": "Cervecería y Maltería Quilmes",
                    "cuit": "30500123451",
                    "telefono": "1143657000",
                    "email": "pedidos@quilmes.com.ar",
                    "activo": True,
                },
                {
                    "nombre": "Molinos Río de la Plata",
                    "cuit": "30500987652",
                    "telefono": "1143401000",
                    "email": "ventas@molinos.com.ar",
                    "activo": True,
                },
                {
                    "nombre": "Arcor Alimentos S.A.",
                    "cuit": "30502233443",
                    "telefono": "1147083000",
                    "email": "distribucion@arcor.com",
                    "activo": True,
                },
            ]
            marcas = {}
            for m_data in marcas_data:
                marca, _ = Marca.objects.get_or_create(
                    cuit=m_data["cuit"], defaults=m_data
                )
                marcas[m_data["nombre"]] = marca

            # ------------------------------------------------------------------
            # 4. Comercios
            # ------------------------------------------------------------------
            comercios_data = [
                {
                    "razon_social": "Supermercado Los Hermanos",
                    "cuit": "20301112223",
                    "domicilio": "Av. San Martín 1540, Quilmes",
                    "telefono": "1142501234",
                    "activo": True,
                },
                {
                    "razon_social": "Almacén Don Tito",
                    "cuit": "20283334445",
                    "domicilio": "Calle 844 N° 230, San Francisco Solano",
                    "telefono": "1142505678",
                    "activo": True,
                },
                {
                    "razon_social": "Autoservicio El Sol",
                    "cuit": "27359998881",
                    "domicilio": "Mitre 450, Bernal",
                    "telefono": "1142509999",
                    "activo": True,
                },
                {
                    "razon_social": "Kiosco Open 25",
                    "cuit": "20365554443",
                    "domicilio": "Pringles 890, Quilmes Este",
                    "telefono": "1142500000",
                    "activo": True,
                },
                {
                    "razon_social": "Distribuidora Mitre SRL",
                    "cuit": "30718889991",
                    "domicilio": "Av. Mitre 2100, Avellaneda",
                    "telefono": "1142013344",
                    "activo": True,
                },
                {
                    "razon_social": "Minimercado San Jorge",
                    "cuit": "20251114449",
                    "domicilio": "Alvear 320, Quilmes Centro",
                    "telefono": "1142548888",
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
            # 5. Remitos PENDIENTES
            # ------------------------------------------------------------------
            remitos_definicion = [
                # Supermercado Los Hermanos (2 marcas distintas para probar consolidación en una parada)
                {
                    "numero": "R-0001-00000101",
                    "marca": marcas["Cervecería y Maltería Quilmes"],
                    "comercio": comercios["20301112223"],
                    "total": Decimal("185000.00"),
                },
                {
                    "numero": "R-0002-00000201",
                    "marca": marcas["Molinos Río de la Plata"],
                    "comercio": comercios["20301112223"],
                    "total": Decimal("142500.00"),
                },
                # Almacén Don Tito
                {
                    "numero": "R-0001-00000102",
                    "marca": marcas["Cervecería y Maltería Quilmes"],
                    "comercio": comercios["20283334445"],
                    "total": Decimal("86000.00"),
                },
                {
                    "numero": "R-0003-00000301",
                    "marca": marcas["Arcor Alimentos S.A."],
                    "comercio": comercios["20283334445"],
                    "total": Decimal("53000.00"),
                },
                # Autoservicio El Sol
                {
                    "numero": "R-0002-00000202",
                    "marca": marcas["Molinos Río de la Plata"],
                    "comercio": comercios["27359998881"],
                    "total": Decimal("98000.00"),
                },
                # Kiosco Open 25
                {
                    "numero": "R-0003-00000302",
                    "marca": marcas["Arcor Alimentos S.A."],
                    "comercio": comercios["20365554443"],
                    "total": Decimal("34500.00"),
                },
                # Distribuidora Mitre SRL
                {
                    "numero": "R-0001-00000103",
                    "marca": marcas["Cervecería y Maltería Quilmes"],
                    "comercio": comercios["30718889991"],
                    "total": Decimal("245000.00"),
                },
                # Minimercado San Jorge (2 marcas distintas)
                {
                    "numero": "R-0002-00000203",
                    "marca": marcas["Molinos Río de la Plata"],
                    "comercio": comercios["20251114449"],
                    "total": Decimal("72000.00"),
                },
                {
                    "numero": "R-0003-00000303",
                    "marca": marcas["Arcor Alimentos S.A."],
                    "comercio": comercios["20251114449"],
                    "total": Decimal("46500.00"),
                },
            ]

            total_remitos = 0

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
            self.style.SUCCESS("✓ Datos maestros y remitos cargados exitosamente.")
        )
        self.stdout.write(f"  • Comercios: {len(comercios_data)}")
        self.stdout.write(f"  • Marcas: {len(marcas_data)}")
        self.stdout.write(
            f"  • Remitos PENDIENTES: {len(remitos_definicion)} ({total_remitos} nuevos)"
        )
        self.stdout.write(
            "  • Itinerarios y Paradas: Ninguno creado (quedan para generar en el flujo de asignación)"
        )
