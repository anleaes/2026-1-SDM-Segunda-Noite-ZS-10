from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),

    # ── Autenticação ──
    path('accounts/', include('django.contrib.auth.urls')),

    # ── API REST ──
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