from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import HistoricalTemporalEvent
import datetime
import uuid


class Command(BaseCommand):
    help = 'Populates the HistoricalTemporalEvent table with default university events and local holidays'

    def handle(self, *args, **kwargs):
        print("Running the populate events command...")  # Add this line to check if the method is called
        self.stdout.write(self.style.SUCCESS("Starting to add events..."))
        self.add_university_events()
        self.add_local_holidays()
        self.add_local_events()
        self.add_other_events()

    def add_university_events(self):
        university_events = [
            # AY-2022-2023 Events
            ("AY-2022-2023 START OF 1ST SEM", datetime.date(2022, 9, 5)),
            ("AY-2022-2023 Official Start of DLTB Bus Operations @ UPLB", datetime.date(2022, 10, 17)),
            ("AY-2022-2023 START OF READING BREAK 1ST SEM", datetime.date(2022, 10, 24)),
            ("AY-2022-2023 END OF READING BREAK 1ST SEM", datetime.date(2022, 10, 29)),
            ("AY-2022-2023 END OF 1ST SEM", datetime.date(2022, 12, 21)),
            ("AY-2022-2023 Start of 1st Sem Final Examinations", datetime.date(2023, 1, 4)),
            ("AY-2022-2023 End of 1st Sem Final Examinations", datetime.date(2023, 1, 11)),
            ("AY-2022-2023 START OF 2ND SEM", datetime.date(2023, 2, 13)),
            ("AY-2022-2023 START OF READING BREAK 2ND SEM", datetime.date(2023, 4, 10)),

            ("AY-2022-2023 END OF READING BREAK 2ND SEM", datetime.date(2023, 4, 15)),
            ("AY-2022-2023 END OF 2ND SEM", datetime.date(2023, 6, 2)),
            ("AY-2022-2023 Start of 2nd Sem Final Examinations", datetime.date(2023, 6, 6)),
            ("AY-2022-2023 End of 2nd Sem Final Examinations", datetime.date(2023, 6, 14)),
            ("AY-2022-2023 START OF MIDYEAR", datetime.date(2023, 7, 5)),
            ("AY-2022-2023 END OF MIDYEAR", datetime.date(2023, 8, 22)),
            ("AY-2022-2023 Start of Mid Year Final Examinations", datetime.date(2023, 8, 24)),
            ("AY-2022-2023 End of Mid Year Final Examinations", datetime.date(2023, 8, 26)),
            ("AY-2022-2023 Graduate School Recognition and Hooding Ceremony", datetime.date(2023, 8, 4)),
            ("AY-2022-2023 UPLB COMMENCEMENT EXERCISES", datetime.date(2023, 8, 5)),

            # AY-2023-2024 Events
            ("AY-2023-2024 START OF 1ST SEM", datetime.date(2023, 8, 29)),
            ("AY-2023-2024 START OF READING BREAK 1ST SEM", datetime.date(2023, 10, 30)),
            ("AY-2023-2024 END OF READING BREAK 1ST SEM", datetime.date(2023, 11, 4)),
            ("AY-2023-2024 END OF 1ST SEM", datetime.date(2023, 12, 21)),
            ("AY-2023-2024 Start of 1st Sem Final Examinations", datetime.date(2024, 1, 4)),
            ("AY-2023-2024 End of 1st Sem Final Examinations", datetime.date(2024, 1, 11)),
            ("AY-2023-2024 START OF 2ND SEM", datetime.date(2024, 2, 5)),
            ("AY-2023-2024 START OF READING BREAK 2ND SEM", datetime.date(2024, 4, 1)),

            ("AY-2023-2024 END OF READING BREAK 2ND SEM", datetime.date(2024, 4, 6)),
            ("AY-2023-2024 END OF 2ND SEM", datetime.date(2024, 5, 31)),
            ("AY-2023-2024 Start of 2nd Sem Final Examinations", datetime.date(2024, 6, 3)),
            ("AY-2023-2024 End of 2nd Sem Final Examinations", datetime.date(2024, 6, 10)),
            ("AY-2023-2024 START OF MIDYEAR", datetime.date(2024, 6, 24)),
            ("AY-2023-2024 END OF MIDYEAR", datetime.date(2024, 7, 27)),
            ("AY-2023-2024 Start of Mid Year Final Examinations", datetime.date(2024, 7, 30)),
            ("AY-2023-2024 End of Mid Year Final Examinations", datetime.date(2024, 7, 31)),
            ("AY-2023-2024 Graduate School Recognition and Hooding Ceremony", datetime.date(2024, 8, 2)),
            ("AY-2023-2024 UPLB COMMENCEMENT EXERCISES", datetime.date(2024, 8, 3)),
        ]

        for name, event_date in university_events:
            if not HistoricalTemporalEvent.objects.filter(event_name=name).exists():
                HistoricalTemporalEvent.objects.create(
                    event_name=name,
                    event_type='university_event',
                    date=event_date,
                    created_by=None,
                    updated_by=None,
                    sort_order=1  # You can set an incremental sort order here if needed
                )
                self.stdout.write(self.style.SUCCESS(f"Added university event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

    def add_local_holidays(self):
        local_holidays = [
            ("test2", datetime.date(2024, 1, 19)),
        ]

        for name, event_date in local_holidays:
            if not HistoricalTemporalEvent.objects.filter(event_name=name).exists():
                HistoricalTemporalEvent.objects.create(
                    event_name=name,
                    event_type='local_holiday',
                    date=event_date,
                    created_by=None,
                    updated_by=None,
                    sort_order=2
                )
                self.stdout.write(self.style.SUCCESS(f"Added local holiday: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

    def add_local_events(self):
        local_events = [
            ("test3", datetime.date(2024, 1, 22)),
        ]

        for name, event_date in local_events:
            if not HistoricalTemporalEvent.objects.filter(event_name=name).exists():
                HistoricalTemporalEvent.objects.create(
                    event_name=name,
                    event_type='local_event',
                    date=event_date,
                    created_by=None,
                    updated_by=None,
                    sort_order=3
                )
                self.stdout.write(self.style.SUCCESS(f"Added local event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

    def add_other_events(self):
        other_events = [
            ("test4", datetime.date(2024, 1, 23)),
        ]

        for name, event_date in other_events:
            if not HistoricalTemporalEvent.objects.filter(event_name=name).exists():
                HistoricalTemporalEvent.objects.create(
                    event_name=name,
                    event_type='others',
                    date=event_date,
                    created_by=None,
                    updated_by=None,
                    sort_order=4
                )
                self.stdout.write(self.style.SUCCESS(f"Added other event: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")
