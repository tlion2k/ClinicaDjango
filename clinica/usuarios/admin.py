from django.contrib import admin
from .models import Perfil, Medico, Paciente


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'rut', 'telefono')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'rut')


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'especialidad')
    search_fields = ('perfil__user__first_name', 'perfil__user__last_name', 'especialidad')


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'fecha_nacimiento')
    search_fields = ('perfil__user__first_name', 'perfil__user__last_name')
