from django.contrib import admin

from django.utils import timezone

import datetime

from django.db.models import Value, F

from .models import Pregunta, Eleccion

# Register your models here.

#admin.site.register(Pregunta) # registro estándar de pregunta

# clase para crear elecciones en el registro de una pregunta de forma apilada
class EleccionInlineStack(admin.StackedInline):
	model = Eleccion
	extra = 3

# clase para crear elecciones en el registro de una pregunta de forma tabulada
class EleccionInlineTab(admin.TabularInline):
	model = Eleccion
	extra = 3

# clase para indicar el comportamiento del registro de una pregunta
class PreguntaAdmin(admin.ModelAdmin):
	# poner la fecha antes que el texto en el registro:
	#fields = ['fec_pub', 'texto']

	# anidar la fecha en una sección (Info. fecha):
	fieldsets = [
		(None,		{'fields': ['texto']}),
		('Info. fecha',	{'fields': ['fec_pub'], 'classes': ['collapse']}),
	]
	inlines = [EleccionInlineTab] # indicar la clase que genera el Inline

	# opción de admin para indicar los campos a mostrar en la lista
	list_display = ('texto', 'fec_pub', 'esReciente')

	# opción de admin para ordenar lista por fec_pub
	ordering = ('fec_pub',)

	# opción para añadir un panel lateral para filtrar por campos indicados
	list_filter = ['fec_pub']

	# opción de admin para añadir un buscador sensible a los campos indicados
	search_fields = ['texto']

	# opcíon de admin para indicar el número de items mostrados por página
	list_per_page = 5

	date_hierarchy = 'fec_pub'

admin.site.register(Pregunta, PreguntaAdmin)
