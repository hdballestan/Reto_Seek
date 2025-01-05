from django.core.management.base import BaseCommand
from biblioteca.models import Book
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Seed the database with sample book data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        genders = ['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Biography', 'History']
        
        for _ in range(20):
            title = fake.sentence(nb_words=4)
            author = fake.name()
            published_date = fake.date_between(start_date="-30y", end_date="today")
            gender = random.choice(genders)
            price = round(random.uniform(10, 100), 2)
            
            Book.objects.create(
                title=title,
                author=author,
                published_date=published_date,
                gender=gender,
                price=price
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with books!'))
