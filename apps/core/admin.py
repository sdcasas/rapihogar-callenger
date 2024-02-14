""" Register models """
from django.contrib import admin
from .models import Company, Tecnico, Scheme, Pedido, User


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone',
        'email',
        'website',
    ]
    search_fields = [
        'name',
        'phone',
        'email',
        'website'
    ]


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'hours_worked', 'total_pedidos', 'total_payment']
    search_fields = ['apellido', 'nombre']


@admin.register(Scheme)
class SchemeyAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["type_request", "client", "scheme", "tecnico", "hours_worked"]
    list_filter = ["type_request", ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
