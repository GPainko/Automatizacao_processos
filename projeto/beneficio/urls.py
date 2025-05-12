from django.urls import path

from .views import BeneficioListView, BeneficioCreateView
from .views import BeneficioUpdateView, BeneficioDeleteView


urlpatterns = [
	path('list/', BeneficioListView.as_view(), name='beneficio_list'),
	path('cad/', BeneficioCreateView.as_view(), name='beneficio_create'),
	path('<slug:slug>/', BeneficioUpdateView.as_view(), name='beneficio_update'),
	path('<slug:slug>/delete/', BeneficioDeleteView.as_view(), name='beneficio_delete'), 
]
 