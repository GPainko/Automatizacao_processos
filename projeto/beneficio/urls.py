from django.urls import path

from .views import TipoBeneficioListView, TipoBeneficioCreateView
from .views import TipoBeneficioUpdateView, TipoBeneficioDeleteView


urlpatterns = [
	path('list/', TipoBeneficioListView.as_view(), name='tipo_beneficio_list'),
	path('cad/', TipoBeneficioCreateView.as_view(), name='tipo_beneficio_create'),
	path('<slug:slug>/', TipoBeneficioUpdateView.as_view(), name='tipo_beneficio_update'),
	path('<slug:slug>/delete/', TipoBeneficioDeleteView.as_view(), name='tipo_beneficio_delete'), 
]
 