from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy

from encuestas.models import Pregunta, Eleccion

from django.db.models import F

from django.views import generic

from django.conf import settings

from django.utils import timezone

# Create your views here.
#	-- VISTAS GENÉRICAS --
def portal(request):
	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	context = {'ultimas_cinco_preguntas': ultimas_cinco_preguntas, 'titulo': 'Inicio del sitio', 'app_name': 'portal'}
	return render(request, 'encuestas/portal.html', context)

class IndexView(generic.ListView):
#	template_name = 'encuestas/genericas/index_app.html'
	context_object_name = 'lista'

	template_name = 'encuestas/genericas/index_app.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if self.request.path == reverse('encuestas:encuestas'):
#			context['lista'] = Pregunta.objects.all()
			context['titulo'] = 'Encuestas'

		return context

	def get_queryset(self):
		return Pregunta.objects.filter(fec_pub__lte=timezone.now()).order_by('-fec_pub')[:5]

class DetailView(generic.DetailView):
	model = Pregunta
	template_name = 'encuestas/genericas/detalles.html'
	context_object_name = 'pregunta'

	def get_queryset(self):
		return Pregunta.objects.filter(fec_pub__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Pregunta
	template_name = 'encuestas/genericas/resultados.html'

# agregado como mejora de Django Tutorial
class AgregarPreguntaView(generic.CreateView):
	model = Pregunta
	fields = ['texto', 'fec_pub']
	template_name_suffix = '_agregar'
	template_name = 'encuestas/genericas/pregunta_agregar.html'

	def get_success_url(self):
        	return reverse('encuestas:encuestas', kwargs={})

	def post(self, request, *args, **kwargs):
		pregunta = Pregunta(texto = request.POST.get("texto"), fec_pub = request.POST.get("fec_pub"))
		pregunta.save()
		pregunta.eleccion_set.create(texto = request.POST.get("texto_eleccion1"), votos = 0)
		pregunta.eleccion_set.create(texto = request.POST.get("texto_eleccion2"), votos = 0)
		pregunta.eleccion_set.create(texto = request.POST.get("texto_eleccion3"), votos = 0)
		return HttpResponseRedirect(reverse_lazy('encuestas:encuestas'))

# agregado como mejora de Django Tutorial
class AgregarEleccionView(generic.CreateView):
	model = Eleccion
	fields = ['texto', 'votos']
	template_name_suffix = '_agregar'
	template_name = 'encuestas/genericas/eleccion_agregar.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pregunta'] = Pregunta.objects.get(pk = self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse('encuestas:detalles', self.kwargs.get('pk'))

	def post(self, request, *args, **kwargs):
		pregunta = Pregunta.objects.get(pk = self.kwargs.get('pk'))
		pregunta.eleccion_set.create(texto = request.POST.get("texto"), votos = request.POST.get("votos"))
		pregunta.save()
#		return HttpResponseRedirect(reverse('encuestas:detalles', args=[pregunta.pk]))
#		return HttpResponseRedirect(reverse('encuestas:detalles', kargs={'id_pregunta': pregunta.pk}))
#		return HttpResponseRedirect(reverse('encuestas:detalles', args=[self.pk]))
		return HttpResponseRedirect(reverse('encuestas:detalles', args=(self.kwargs.get('pk'),)))
#		return HttpResponseRedirect(reverse('encuestas:detalles', args=[str(self.pk)]))'''

def votar(request, id_pregunta):
	pregunta = get_object_or_404(Pregunta, pk = id_pregunta)

	try:
		selected_eleccion = pregunta.eleccion_set.get(pk = request.POST['eleccion'])
	except (KeyError, Eleccion.DoesNotExist):
		# volver a mostrar el formulario de la pregunta
		return render(request, 'encuestas/detalles.html', {'pregunta': pregunta, 'msg_err': "No has seleccionado ninguna opción"})
	else:
		selected_eleccion.votos = F('votos') + 1
		selected_eleccion.save()
		return HttpResponseRedirect(reverse('encuestas:resultados', args=(pregunta.id,)))

#	return HttpResponse("Estás votando para la pregunta " + str(id_pregunta))

'''#	-- VISTAS NO GENÉRICAS --
def portal(request):
	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	context = {'ultimas_cinco_preguntas': ultimas_cinco_preguntas}
	return render(request, 'encuestas/portal.html', context)

	# hardcoded desde aquí
	output = "<h1>Inicio del sitio</h1><br><br>"
	output += "Estas son las cinco últimas preguntas:<br>"

	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	for p in ultimas_cinco_preguntas:
		output += "· " + p.texto + "<br>"

	return HttpResponse(output)
	# hardcoded hasta aquí

def encuestas(request):
	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	context = {'ultimas_cinco_preguntas': ultimas_cinco_preguntas}
	return render(request, 'encuestas/inicio.html', context)
#	return HttpResponse("Inicio de encuestas")

def detalles(request, id_pregunta):
	pregunta = get_object_or_404(Pregunta, pk = id_pregunta)
	return render(request, 'encuestas/detalles.html', {'pregunta': pregunta})
	#return HttpResponse("Detalles de pregunta " + str(id_pregunta))

def resultados(request, id_pregunta):
	pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
	return render(request, 'encuestas/resultados.html', {'pregunta': pregunta})
#	return HttpResponse("Resultados de pregunta " + str(id_pregunta))

def votar(request, id_pregunta):
	pregunta = get_object_or_404(Pregunta, pk = id_pregunta)

	try:
		selected_eleccion = pregunta.eleccion_set.get(pk = request.POST['eleccion'])
	except (KeyError, Eleccion.DoesNotExist):
		# volver a mostrar el formulario de la pregunta
		return render(request, 'encuestas/detalles.html', {'pregunta': pregunta, 'msg_err': "No has seleccionado ninguna opción"})
	else:
		selected_eleccion.votos = F('votos') + 1
		selected_eleccion.save()
		return HttpResponseRedirect(reverse('encuestas:resultados', args=(pregunta.id,)))

#	return HttpResponse("Estás votando para la pregunta " + str(id_pregunta))
'''
