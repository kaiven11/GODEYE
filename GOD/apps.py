from django.apps import AppConfig
class GodConfig(AppConfig):
    name = 'GOD'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import GODEYE.signals