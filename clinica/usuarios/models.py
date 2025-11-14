from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('MEDICO', 'Médico'),
        ('PACIENTE', 'Paciente'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES)
    rut = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"


class Medico(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.perfil.user.first_name} {self.perfil.user.last_name} ({self.especialidad})"


class Paciente(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.perfil.user.first_name} {self.perfil.user.last_name}"
