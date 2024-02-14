from django.core.management.base import BaseCommand

from core.tests.factories import TecnicoFactory


class Command(BaseCommand):
    help = 'Crear registros del modelo Tecnico'
    
    def add_arguments(self, parser):
        parser.add_argument("--cantidad", required=True, type=int)
    
    def handle(self, *args, **options):
        cantidad = options.get('cantidad')
        TecnicoFactory.create_batch(cantidad)
