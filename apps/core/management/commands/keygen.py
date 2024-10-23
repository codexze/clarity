# coding=utf-8
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):

    help = 'Generate random secret key for django.'

    def handle(self, *args, **options):
        key = get_random_secret_key()
        self.stdout.write(key)
