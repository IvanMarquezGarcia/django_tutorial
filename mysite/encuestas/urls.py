from django.urls import path

from . import views	# importar vistas de la app

app_name = 'encuestas'

urlpatterns = [
	path('', views.inicio, name = 'inicio'), 	# esto debería estar en la app de login, pero no tengo
	path('inicio/', views.inicio, name = 'inicio'), # esto debería estar en la app de login, pero no tengo
	path('encuestas/', views.encuestas, name = 'encuestas'),
	path('encuestas/<int:id_pregunta>/', views.detalles, name = 'detalles'),
	path('encuestas/<int:id_pregunta>/resultados/', views.resultados, name = 'resultados'),
	path('encuestas/<int:id_pregunta>/votar/', views.votar, name = 'votar'),
]
