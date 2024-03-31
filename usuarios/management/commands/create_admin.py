import json
from django.core.management.base import BaseCommand
from usuarios.models import Usuario
import os

class Command(BaseCommand):
    help = 'Comando para crear administrador del sitio'

    def handle(self, *args, **options):
        if os.getenv("SU_USER") and os.getenv("SU_PASSWORD"):
            user = Usuario.objects.get(username=os.getenv("SU_USER"))
            if not user:
                Usuario.objects.create_superuser(username=os.getenv("SU_USER"), password=os.getenv("SU_PASSWORD"))
            self.stdout.write(self.style.SUCCESS('Administrador creado exitosamente'))
        else:
            self.stdout.write(self.style.ERROR_OUTPUT('No se configuraron las variables de entorno SU_USER y SU_PASSWORD'))