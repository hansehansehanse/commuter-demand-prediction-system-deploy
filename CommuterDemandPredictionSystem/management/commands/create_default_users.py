from django.core.management.base import BaseCommand
from CommuterDemandPredictionSystem.models import CustomUser

class Command(BaseCommand):
    help = 'Creates default admin and bus manager users if they do not exist'

    def handle(self, *args, **kwargs):
        # Check if the admin user exists
        if not CustomUser.objects.filter(username='admin').exists():
            # Create admin user with access level 'Admin' and verified set to True
            admin = CustomUser.objects.create_superuser(
                username='admin',
                first_name='initial_admin',
                last_name='-',  
                email='admin@example.com',
                password='adminpassword123',
                access_level='Admin',  # Set access level to 'Admin'
                verified=True  # Set verified to True for the admin
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))

        # Check if the bus manager user exists
        if not CustomUser.objects.filter(username='bus_manager').exists():
            # Create bus manager user with access level 'Bus Manager'
            bus_manager = CustomUser.objects.create_user(
                username='bus_manager',
                first_name='initial_bus_manager',
                last_name='-',
                email='busmanager@example.com',
                password='busmanagerpassword123',
                access_level='Bus Manager',  # Set access level to 'Bus Manager'
                verified=False  # Make sure verified is False (or any default state)
            )
            self.stdout.write(self.style.SUCCESS('Bus Manager user created successfully!'))
