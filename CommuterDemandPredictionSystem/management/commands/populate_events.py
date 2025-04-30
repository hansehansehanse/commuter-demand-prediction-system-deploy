from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import TemporalEvent
import uuid

class Command(BaseCommand):
    help = 'Populates the TemporalEvent table with default university events if not already present'

    def handle(self, *args, **kwargs):
        default_events = [
            "Start of 1st Sem",
            "End of 1st Sem"
        ]

        for name in default_events:
            if not TemporalEvent.objects.filter(event_name=name).exists():
                TemporalEvent.objects.create(
                    event_name=name,
                    event_type='University Event',
                    date=None,
                    created_by=None,                                                            # can't use other placeholder values like '-' 
                    updated_by=None
                )
                self.stdout.write(self.style.SUCCESS(f"Added default event: {name}"))
            else:
                self.stdout.write(f"Event already exists: {name}")
