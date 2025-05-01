from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import HolidayEvent
from datetime import date

class Command(BaseCommand):
    help = 'Populates the HolidayEvent table with default holidays (without considering year) if not already present'

    def handle(self, *args, **kwargs):
        # Define a list of default holiday events (without the year)
        default_holidays = [
            {"name": "Christmas", "event_type": "holiday", "date": date(1, 12, 25)},  # Example for Christmas (no year)
            {"name": "New Year", "event_type": "holiday", "date": date(1, 1, 1)},       # Example for New Year (no year)
        ]

        for holiday in default_holidays:
            # Check if the holiday already exists in the database by comparing the month and day
            if not HolidayEvent.objects.filter(event_name=holiday["name"], date__month=holiday["date"].month, date__day=holiday["date"].day).exists():
                # Create a new holiday event if it doesn't exist
                HolidayEvent.objects.create(
                    event_name=holiday["name"],
                    event_type=holiday["event_type"],
                    date=holiday["date"],  # Only stores the month and day, year doesn't matter
                    updated_by=None  # Assuming you're not setting a user here initially
                )
                self.stdout.write(self.style.SUCCESS(f"Added default holiday: {holiday['name']}"))
            else:
                self.stdout.write(f"Holiday already exists: {holiday['name']}")
