from django.urls import path

from .views import DespachoListView, DespachoCreateView
from .views import DespachoUpdateView, DespachoDeleteView
from .views import DespachoPdfView


urlpatterns = [
	path('list/', DespachoListView.as_view(), name='despacho_list'),
	path('cad/', DespachoCreateView.as_view(), name='despacho_create'),
	path('<slug:slug>/', DespachoUpdateView.as_view(), name='despacho_update'),
	path('<slug:slug>/delete/', DespachoDeleteView.as_view(), name='despacho_delete'), 
    path('despacho/<slug:slug>/pdf/', DespachoPdfView.as_view(), name='despacho_pdf'),
]
 