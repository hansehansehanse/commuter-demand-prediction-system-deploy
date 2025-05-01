from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import TemporalEvent
import datetime

class Command(BaseCommand):
    help = 'Populates the TemporalEvent table with default university events and local holidays'

    def handle(self, *args, **kwargs):
        self.add_university_events()
        self.add_local_holidays()

    def add_university_events(self):
        # university_events = [
        # ("Start of 1st Semester", 1),
        # ("End of 1st Semester", 2),
        # ("Start of 2nd Semester", 3),
        # ("End of 2nd Semester", 4),
        # ("Enrollment Period", 5),
        # ("Final Exams Week", 6),
        # ]

        # for name, order in university_events:
        #     if not TemporalEvent.objects.filter(event_name=name).exists():
        #         TemporalEvent.objects.create(
        #             event_name=name,
        #             event_type='university_event',
        #             date=None,
        #             sort_order=order,
        #             created_by=None,
        #             updated_by=None
        #         )
        #         self.stdout.write(self.style.SUCCESS(f"Added university event: {name}"))
        #     else:
        #         self.stdout.write(f"Already exists: {name}")

        university_events = [
        ("Start of 1st Semester", 1, datetime.date(2025, 5, 1)),
        ("End of 1st Semester", 2, datetime.date(2025, 6, 1)),
        ("Start of 2nd Semester", 3, datetime.date(2025, 6, 4)),
        ("End of 2nd Semester", 4, datetime.date(2025, 7, 1)),
        ("Enrollment Period", 5, datetime.date(2025, 7, 4)),
        # ("Final Exams Week", 6, datetime.date(2025, 12, 1)),
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
            # ("City Day", datetime.date(1900, 3, 1)),
            # ("Founding Anniversary", datetime.date(1900, 7, 15)),
            ("test", datetime.date(2025, 1, 5)),
            ("test 2", datetime.date(2024, 1, 6)),
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
