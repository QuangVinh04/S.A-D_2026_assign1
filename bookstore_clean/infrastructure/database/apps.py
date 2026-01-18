"""Django app configuration for database infrastructure"""
from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    """Configuration for database infrastructure app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrastructure.database'
    label = 'database'
    verbose_name = 'Database Infrastructure'
