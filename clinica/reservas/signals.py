from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Especialidad


@receiver(post_migrate)
def crear_especialidades_default(sender, **kwargs):
    # Evitar crear datos en apps que no son esta
    if sender.name != 'reservas':
        return
    
    especialidades = [
        "Medicina General",
        "Pediatría",
        "Traumatología",
        "Cardiología",
        "Dermatología",
    ]

    for nombre in especialidades:
        Especialidad.objects.get_or_create(nombre=nombre)

    print("Especialidades por defecto cargadas ✔")
