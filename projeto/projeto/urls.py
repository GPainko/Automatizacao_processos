from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('membro/', include('appmembro.urls')), 
    
    path('aviso/', include('aviso.urls')), 
    
    path('instituicao/', include('instituicao.urls')), 
    path('tipo_beneficio/', include('tipo_beneficio.urls')), 
    path('beneficio/', include('beneficio.urls')), 
    path('despachio',include('despacho.urls')),
    path('usuario/', include('usuario.urls')),   
    
    path('accounts/', include('django.contrib.auth.urls')),
]

#url para arquivos de media quando em desenvolvimento
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, 
    document_root = settings.STATIC_ROOT)   
