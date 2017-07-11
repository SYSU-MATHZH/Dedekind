from django.apps import AppConfig


class SuaConfig(AppConfig):
    name = 'sua'

    def ready(self):
        import sua.signals.handlers
