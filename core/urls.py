from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/pessoas/', include('apps.pessoas.urls')),
    path('api/unidades/', include('apps.unidades.urls')),
    path('api/vacinas/', include('apps.vacinas.urls')),
    path('api/perfis/', include('apps.perfis.urls')),
    path('api/calendario/', include('apps.calendario.urls')),
    path('api/atendimentos/', include('apps.atendimentos.urls')),
    path('api/registros/', include('apps.registros.urls')),
    path('api/campanhas/', include('apps.campanhas.urls')),
    path('api/notificacoes/', include('apps.notificacoes.urls')),
    path('api/situacao/', include('apps.situacao.urls')),
]
