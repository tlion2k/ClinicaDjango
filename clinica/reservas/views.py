from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from usuarios.models import Perfil, Medico, Paciente
from .models import Reserva, Especialidad
from django.contrib import messages
from django.db.models import Count


@login_required
def dashboard(request):
    """Vista principal después de login, muestra reservas según el rol."""
    perfil = Perfil.objects.filter(user=request.user).first()

    # Por defecto: todas las reservas (para ADMIN)
    reservas = Reserva.objects.all().order_by('fecha', 'hora')
    titulo = "Todas las reservas"

    # Métricas simples de reservas por estado (globales)
    resumen_estados = Reserva.objects.values('estado').annotate(total=Count('id'))

    if perfil:
        if perfil.rol == 'PACIENTE':
            paciente = getattr(perfil, 'paciente', None) or Paciente.objects.filter(perfil=perfil).first()
            if paciente:
                reservas = Reserva.objects.filter(paciente=paciente).order_by('fecha', 'hora')
                titulo = "Mis reservas como paciente"

        elif perfil.rol == 'MEDICO':
            medico = getattr(perfil, 'medico', None) or Medico.objects.filter(perfil=perfil).first()
            if medico:
                reservas = Reserva.objects.filter(medico=medico).order_by('fecha', 'hora')
                titulo = "Mis reservas como médico"

        else:  # ADMIN
            titulo = "Todas las reservas"

    # Convertir a diccionario más cómodo para el template
    resumen_dict = {item['estado']: item['total'] for item in resumen_estados}
    total_reservas = sum(resumen_dict.values())
    
    context = {
        "reservas": reservas,
        "perfil": perfil,
        "titulo": titulo,
        "resumen_estados": resumen_dict,
        "total_reservas": total_reservas,
    }

    return render(request, "dashboard.html", context)


@login_required
def agendar_reserva(request):
    perfil = Perfil.objects.get(user=request.user)

    # Solo pacientes pueden agendar
    if perfil.rol != "PACIENTE":
        messages.error(request, "Solo los pacientes pueden agendar reservas.")
        return redirect("dashboard")

    paciente = Paciente.objects.get(perfil=perfil)

    # 🔹 AQUÍ CARGAMOS TODOS LOS MÉDICOS Y ESPECIALIDADES
    especialidades = Especialidad.objects.all()
    medicos = Medico.objects.all()

    if request.method == "POST":
        especialidad_id = request.POST["especialidad"]
        medico_id = request.POST["medico"]
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]

        Reserva.objects.create(
            paciente=paciente,
            medico=Medico.objects.get(id=medico_id),
            especialidad=Especialidad.objects.get(id=especialidad_id),
            fecha=fecha,
            hora=hora,
            estado="PENDIENTE",
        )

        messages.success(request, "Reserva creada correctamente.")
        return redirect("dashboard")

    # 👇 MUY IMPORTANTE: pasar 'medicos' al contexto
    return render(request, "agendar.html", {
        "especialidades": especialidades,
        "medicos": medicos,
    })

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    perfil = Perfil.objects.get(user=request.user)

    # Solo paciente dueño de la reserva o ADMIN pueden editar
    if perfil.rol == 'PACIENTE':
        paciente = Paciente.objects.get(perfil=perfil)
        if reserva.paciente != paciente:
            messages.error(request, "No puedes editar una reserva que no es tuya.")
            return redirect("dashboard")

    # 🔹 Cargar médicos y especialidades para el formulario
    especialidades = Especialidad.objects.all()
    medicos = Medico.objects.all()

    if request.method == "POST":
        especialidad_id = request.POST["especialidad"]
        medico_id = request.POST["medico"]
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]

        reserva.especialidad = Especialidad.objects.get(id=especialidad_id)
        reserva.medico = Medico.objects.get(id=medico_id)
        reserva.fecha = fecha
        reserva.hora = hora
        reserva.save()

        messages.success(request, "Reserva actualizada correctamente.")
        return redirect("dashboard")

    # 👇 IMPORTANTE: pasar 'medicos' y 'especialidades' al contexto
    return render(request, "editar_reserva.html", {
        "reserva": reserva,
        "especialidades": especialidades,
        "medicos": medicos,
    })


@login_required
def cancelar_reserva(request, reserva_id):
    """Cambiar estado a CANCELADA."""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    perfil = Perfil.objects.get(user=request.user)

    # Solo paciente dueño o ADMIN
    if perfil.rol == 'PACIENTE':
        paciente = Paciente.objects.get(perfil=perfil)
        if reserva.paciente != paciente:
            messages.error(request, "No puedes cancelar una reserva que no es tuya.")
            return redirect("dashboard")

    # Cambiar estado
    reserva.estado = "CANCELADA"
    reserva.save()

    messages.success(request, "Reserva cancelada correctamente.")
    return redirect("dashboard")

@login_required
def cambiar_estado_reserva(request, reserva_id, nuevo_estado):
    """Permite a un médico (o admin) cambiar el estado de su reserva."""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    perfil = Perfil.objects.get(user=request.user)

    # Solo médico dueño de la reserva o ADMIN pueden cambiar estado
    if perfil.rol == 'MEDICO':
        medico = Medico.objects.get(perfil=perfil)
        if reserva.medico != medico:
            messages.error(request, "No puedes cambiar el estado de una reserva que no es tuya.")
            return redirect("dashboard")
    elif perfil.rol != 'ADMIN':
        messages.error(request, "No tienes permisos para cambiar estados.")
        return redirect("dashboard")

    # Validar que el estado nuevo esté dentro de los permitidos
    estados_validos = [e[0] for e in Reserva.ESTADO_CHOICES]
    if nuevo_estado not in estados_validos:
        messages.error(request, "Estado no válido.")
        return redirect("dashboard")

    reserva.estado = nuevo_estado
    reserva.save()
    messages.success(request, f"Estado cambiado a {reserva.get_estado_display()}.")
    return redirect("dashboard")
