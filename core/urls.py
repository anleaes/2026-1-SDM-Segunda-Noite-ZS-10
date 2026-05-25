from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/pessoas/', include('apps.pessoas.urls')),
    path('api/unidades/', include('apps.unidades.urls')),
    path('api/vacinas/', include('apps.vacinas.urls')),
    path('api/perfis/', include('apps.perfis.urls')),
    path('api/calendario/', include('calendario.urls')),
    path('api/atendimentos/', include('atendimentos.urls')),
]
