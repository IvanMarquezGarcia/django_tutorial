from django.urls import path

from . import views	# importar vistas de la app

app_name = 'encuestas'

#	-- URLS PARA VISTAS GENÉRICAS --
urlpatterns = [
	path('', views.portal, name = 'portal'), 	# esto debería estar en la app de login, pero no tengo
	path('portal/', views.InicioView.as_view(), name = 'portal'), # esto debería estar en la app de login, pero no tengo
	path('encuestas/',  views.InicioView.as_view(), name = 'encuestas'),
	path('encuestas/<int:pk>/', views.DetailView.as_view(), name = 'detalles'),
	path('encuestas/<int:pk>/resultados/', views.ResultsView.as_view(), name = 'resultados'),
	path('encuestas/<int:id_pregunta>/votar/', views.votar, name = 'votar'), # esta de momento no es genérica porque no es similar
]



'''#	-- URLS PARA VISTAS NO GENÉRICAS --
urlpatterns = [
	path('', views.portal, name = 'portal'), 	# esto debería estar en la app de login, pero no tengo
	path('portal/', views.portal, name = 'portal'), # esto debería estar en la app de login, pero no tengo
	path('encuestas/', views.encuestas, name = 'encuestas'),
	path('encuestas/<int:id_pregunta>/', views.detalles, name = 'detalles'),
	path('encuestas/<int:id_pregunta>/resultados/', views.resultados, name = 'resultados'),
	path('encuestas/<int:id_pregunta>/votar/', views.votar, name = 'votar'),
]
'''
