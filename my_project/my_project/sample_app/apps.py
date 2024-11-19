from django.apps import AppConfig
from .utils import load_fingering_cost

class SampleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_app'

    def ready(self):
        load_fingering_cost()
