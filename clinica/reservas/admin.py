from django.contrib import admin
from .models import Especialidad, Reserva


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'medico', 'paciente', 'especialidad', 'estado')
    list_filter = ('estado', 'especialidad', 'fecha')
    search_fields = (
        'medico__perfil__user__first_name',
        'medico__perfil__user__last_name',
        'paciente__perfil__user__first_name',
        'paciente__perfil__user__last_name',
    )
