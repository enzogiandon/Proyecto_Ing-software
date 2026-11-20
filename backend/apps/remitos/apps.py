from django.apps import AppConfig


class RemitosConfig(AppConfig):
    name = 'apps.remitos'

    def ready(self):
        import apps.remitos.signals  # noqa
