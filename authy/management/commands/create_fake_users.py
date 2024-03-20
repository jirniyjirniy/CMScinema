from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
from authy.models import CustomUser  # Import your CustomUser model

class Command(BaseCommand):
    help = 'Generate fake users and save them to the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(100):
            # Generate a random birth date between 18 and 65 years ago
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
            # Create a User instance
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'  # Set a default password
            )
            # Create a CustomUser instance and associate it with the User instance
            CustomUser.objects.create(
                user=user,
                name=fake.first_name(),
                second_name=fake.last_name(),
                nickname=fake.user_name(),
                email=fake.email(),
                birth_date=birth_date,
                # Add other fields as needed
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 100 fake users'))
