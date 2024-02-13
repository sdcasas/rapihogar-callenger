""" Register models """
from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
        list_display = [
            'name',
            'phone',
            'email',
            'website',
        ]
        list_filter = [
            'name',
            'phone',
            'email',
            'website'
        ]
        search_fields = [
            'name',
            'phone',
            'email',
            'website'
        ]