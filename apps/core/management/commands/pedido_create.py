from django.core.management.base import BaseCommand

from core.tests.factories import PedidoFactory


def cantidad_is_valid(value):
    return 1 <= value <= 100


class Command(BaseCommand):
    help = 'Crear registros del modelo Pedido'
    
    def add_arguments(self, parser):
        parser.add_argument("--cantidad", required=True, type=int)
    
    def handle(self, *args, **options):
        cantidad = options.get('cantidad')
        
        if not cantidad_is_valid(value=cantidad):
            print("Cantidad debe ser un valor entre 1 y 100")
            return
        
        PedidoFactory.create_batch(cantidad)
