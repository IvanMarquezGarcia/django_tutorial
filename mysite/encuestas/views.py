from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from encuestas.models import Pregunta, Eleccion

from django.db.models import F

# Create your views here.
def portal(request):
	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	context = {'ultimas_cinco_preguntas': ultimas_cinco_preguntas}
	return render(request, 'encuestas/portal.html', context)
'''
	output = "<h1>Inicio del sitio</h1><br><br>"
	output += "Estas son las cinco últimas preguntas:<br>"

	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	for p in ultimas_cinco_preguntas:
		output += "· " + p.texto + "<br>"

	return HttpResponse(output)
'''
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
