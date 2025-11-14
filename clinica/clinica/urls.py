from django.contrib import admin
from django.urls import path, include
from usuarios.views import login_view, logout_view
from reservas.views import dashboard

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Ruta raíz → Login
    path('', login_view, name='login'),

    # Login explícito (opcional)
    path('login/', login_view, name='login_explicit'),

    # Logout
    path('logout/', logout_view, name='logout'),

    # Dashboard (lo ve cualquier usuario logueado)
    path('dashboard/', dashboard, name='dashboard'),

    # Rutas de la aplicación de reservas
    path('reservas/', include('reservas.urls')),
]
