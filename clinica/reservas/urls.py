from django.urls import path
from .views import agendar_reserva, editar_reserva, cancelar_reserva, cambiar_estado_reserva

urlpatterns = [
    path('agendar/', agendar_reserva, name='agendar'),
    path('editar/<int:reserva_id>/', editar_reserva, name='editar_reserva'),
    path('cancelar/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),
    path('estado/<int:reserva_id>/<str:nuevo_estado>/', cambiar_estado_reserva, name='cambiar_estado_reserva'),
]
