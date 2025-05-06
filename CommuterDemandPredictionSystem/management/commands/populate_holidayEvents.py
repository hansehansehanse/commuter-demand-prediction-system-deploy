from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import HolidayEvent
from datetime import date

class Command(BaseCommand):
    help = 'Populates the HolidayEvent table with default holidays (without considering year) if not already present'

    def handle(self, *args, **kwargs):
        # Define a list of default holiday events (without the year)
        default_holidays = [
            # {"name": "Start of Christmas Vacation", "event_type": "holiday", "date": date(1, 12, 23)},
            # {"name": "End of Christmas Vacation", "event_type": "holiday", "date": date(1, 1, 1)},
            # {"name": "Christmas", "event_type": "holiday", "date": date(1, 12, 25)},  
            # {"name": "New Year", "event_type": "holiday", "date": date(1, 1, 1)},       
            {"name": "New Year's Day", "event_type": "holiday", "date": date(1, 1, 1)},
            {"name": "EDSA People Power Revolution", "event_type": "holiday", "date": date(1, 2, 25)},
            {"name": "Araw ng Kagitingan", "event_type": "holiday", "date": date(1, 4, 9)},
            {"name": "Labor Day", "event_type": "holiday", "date": date(1, 5, 1)},
            {"name": "Independence Day", "event_type": "holiday", "date": date(1, 6, 12)},
            {"name": "Ninoy Aquino Day", "event_type": "holiday", "date": date(1, 8, 21)},
            {"name": "National Heroes Day", "event_type": "holiday", "date": date(1, 8, 29)},                   # .
            {"name": "All Saints’ Day", "event_type": "holiday", "date": date(1, 11, 1)},
            {"name": "All Souls’ Day", "event_type": "holiday", "date": date(1, 11, 2)},                        # .
            {"name": "Bonifacio Day", "event_type": "holiday", "date": date(1, 11, 30)},
            {"name": "Christmas Eve", "event_type": "holiday", "date": date(1, 12, 24)},
            {"name": "Christmas Day", "event_type": "holiday", "date": date(1, 12, 25)},
            {"name": "Rizal Day", "event_type": "holiday", "date": date(1, 12, 30)},
            {"name": "New Year’s Eve", "event_type": "holiday", "date": date(1, 12, 31)},
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
