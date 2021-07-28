from boards.models import Board

from django.core.management.base import BaseCommand

from faker import Faker

UserModel = Board


class Command(BaseCommand):
    help = "Create random boards" # noqa A003

    def add_arguments(self, parser):
        parser.add_argument("total", type=int, choices=range(1, 1000), help='Number of users to create')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']
        obj = [
            UserModel(
                name=fake.name(),
                description=fake.last_name(),
            )
            for _ in range(total)
        ]

        UserModel.objects.bulk_create(obj)
        print("Board Created!") # noqa T001
