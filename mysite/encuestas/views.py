from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from encuestas.models import Pregunta

# Create your views here.
def inicio(request):
	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	context = {'ultimas_cinco_preguntas': ultimas_cinco_preguntas}
	return render(request, 'encuestas/inicio.html', context)
'''
	output = "<h1>Inicio del sitio</h1><br><br>"
	output += "Estas son las cinco últimas preguntas:<br>"

	ultimas_cinco_preguntas = Pregunta.objects.order_by('-fec_pub')[:5]
	for p in ultimas_cinco_preguntas:
		output += "· " + p.texto + "<br>"

	return HttpResponse(output)
'''
def encuestas(request):
	return HttpResponse("Inicio de encuestas")

def detalles(request, id_pregunta):
	pregunta = get_object_or_404(Pregunta, pk = id_pregunta)
	return render(request, 'encuestas/detalles.html', {'pregunta': pregunta})
	#return HttpResponse("Detalles de pregunta " + str(id_pregunta))

def resultados(request, id_pregunta):
	return HttpResponse("Resultados de pregunta " + str(id_pregunta))

def votar(request, id_pregunta):
	return HttpResponse("Estás votando para la pregunta " + str(id_pregunta))
