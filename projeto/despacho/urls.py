from django.urls import path

from .views import DespachoListView, DespachoCreateView
from .views import DespachoUpdateView, DespachoDeleteView


urlpatterns = [
	path('list/', DespachoListView.as_view(), name='despacho_list'),
	path('cad/', DespachoCreateView.as_view(), name='despacho_create'),
	path('<slug:slug>/', DespachoUpdateView.as_view(), name='despacho_update'),
	path('<slug:slug>/delete/', DespachoDeleteView.as_view(), name='despacho_delete'), 
]
 