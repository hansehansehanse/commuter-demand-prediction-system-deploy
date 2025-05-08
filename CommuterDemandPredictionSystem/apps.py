
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class CommuterdemandpredictionsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CommuterDemandPredictionSystem'

    def ready(self):
        # Connect the post_migrate signal to automatically create default users
        post_migrate.connect(self.create_default_users, sender=self)

    def create_default_users(self, **kwargs):
        # Call the custom command to create default users after migration
        call_command('create_default_users')
        call_command('populate_events')
        call_command('populate_holidayEvents')
        call_command('populate_historicalEvents')

        
