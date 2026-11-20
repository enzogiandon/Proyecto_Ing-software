import logging
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver

from apps.remitos.models import Remito
from apps.itinerarios.models import Parada
from apps.cobranza.models import Cobranza

logger = logging.getLogger(__name__)


def eliminar_parada_si_vacia(parada_id):
    """
    Invariante de dominio: Una parada debe tener al menos un remito asociado.
    Si una parada queda con 0 remitos (por eliminación o desvinculación de remitos),
    se elimina automáticamente la parada del itinerario (salvo que tenga cobranzas registradas)
    y se reordena la secuencia de las paradas restantes.
    """
    if not parada_id:
        return
    try:
        parada = Parada.objects.filter(pk=parada_id).first()
        if not parada:
            return

        # Si aún tiene remitos asociados, no se debe eliminar
        if parada.remitos.exists():
            return

        # Si posee cobranzas registradas, protegemos la integridad contable
        if Cobranza.objects.filter(parada=parada).exists():
            logger.warning(
                f"Parada #{parada_id} quedó sin remitos pero no se elimina por poseer cobranzas registradas."
            )
            return

        itinerario = parada.itinerario
        parada.delete()

        # Reordenar correlativamente las paradas restantes del itinerario
        if itinerario:
            for idx, p in enumerate(
                itinerario.paradas.all().order_by("orden", "id"), start=1
            ):
                if p.orden != idx:
                    p.orden = idx
                    p.save(update_fields=["orden"])

        logger.info(
            f"Parada #{parada_id} eliminada automáticamente por quedar sin remitos asociados."
        )
    except Exception as exc:
        logger.error(
            f"Error al verificar/eliminar parada vacía #{parada_id}: {exc}",
            exc_info=True,
        )


@receiver(post_delete, sender=Remito)
def remito_post_delete(sender, instance, **kwargs):
    if instance.parada_id:
        eliminar_parada_si_vacia(instance.parada_id)


@receiver(pre_save, sender=Remito)
def remito_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_parada_id = (
                Remito.objects.filter(pk=instance.pk)
                .values_list("parada_id", flat=True)
                .first()
            )
            instance._old_parada_id = old_parada_id
        except Exception:
            instance._old_parada_id = None
    else:
        instance._old_parada_id = None


@receiver(post_save, sender=Remito)
def remito_post_save(sender, instance, **kwargs):
    old_parada_id = getattr(instance, "_old_parada_id", None)
    if old_parada_id and old_parada_id != instance.parada_id:
        eliminar_parada_si_vacia(old_parada_id)
