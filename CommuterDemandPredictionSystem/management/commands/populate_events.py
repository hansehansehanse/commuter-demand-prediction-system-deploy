from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import TemporalEvent
import datetime

class Command(BaseCommand):
    help = 'Populates the TemporalEvent table with default university events and local holidays'

    def handle(self, *args, **kwargs):
        self.add_university_events()
        self.add_local_holidays()
        self.add_local_events()
        self.add_other_events()
        

    def add_university_events(self):

        university_events = [
        # ("Start of 1st Semester", 1, datetime.date(2024, 5, 1)),
        # ("End of 1st Semester", 2, datetime.date(2024, 6, 1)),
        # ("Start of 2nd Semester", 3, datetime.date(2024, 6, 4)),
        # ("End of 2nd Semester", 4, datetime.date(2024, 7, 1)),
        ("Start of 1st Semester", 1, datetime.date(2024, 1, 3)),
        ("End of 1st Semester", 2, datetime.date(2024, 1, 10)),
        ("Start of 2nd Semester", 3, datetime.date(2024, 1, 15)),
        ("End of 2nd Semester", 4, datetime.date(2024, 1, 25)),
        
        ("Loyalty Day", 5, datetime.date(2025, 10, 10)),
        ("UPLB Foundation Day", 1, datetime.date(2024, 3, 6)),
        ("test1", 6, datetime.date(2024, 1, 20)),
    ]

        for name, order, event_date in university_events:
            if not TemporalEvent.objects.filter(event_name=name).exists():
                TemporalEvent.objects.create(
                    event_name=name,
                    event_type='university_event',
                    sort_order=order,
                    date=event_date,
                    created_by=None,
                    updated_by=None
                )
                self.stdout.write(self.style.SUCCESS(f"Added event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

    def add_local_holidays(self):
        local_holidays = [

            ("test2", datetime.date(2024, 1, 19)),

        ]

        for name, date in local_holidays:
            if not TemporalEvent.objects.filter(event_name=name).exists():
                TemporalEvent.objects.create(
                    event_name=name,
                    event_type='local_holiday',
                    date=date,
                    created_by=None,
                    updated_by=None
                )
                self.stdout.write(self.style.SUCCESS(f"Added local holiday: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")


    # remove later for testing purposes
    def add_local_events(self):
        local_events = [

            # ("Los Baños Founding Anniversary", datetime.date(1900, 7, 15)),
            ("test3", datetime.date(2024, 1, 22)),

        ]

        for name, date in local_events:
            if not TemporalEvent.objects.filter(event_name=name).exists():
                TemporalEvent.objects.create(
                    event_name=name,
                    event_type='local_event',
                    date=date,
                    created_by=None,
                    updated_by=None
                )
                self.stdout.write(self.style.SUCCESS(f"Added local event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")


    def add_other_events(self):
        other_events = [
            ("test4", datetime.date(2024, 1, 23)),
        ]

        for name, date in other_events:
            if not TemporalEvent.objects.filter(event_name=name).exists():
                TemporalEvent.objects.create(
                    event_name=name,
                    event_type='others',
                    date=date,
                    created_by=None,
                    updated_by=None
                )
                self.stdout.write(self.style.SUCCESS(f"Added other event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")
