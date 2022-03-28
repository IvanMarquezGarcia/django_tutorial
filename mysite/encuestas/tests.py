import datetime

from django.test import TestCase

from django.utils import timezone

from django.urls import reverse

from .models import Pregunta

# Create your tests here.

def crear_pregunta(texto, dias):
	# crear pregunta
	time = timezone.now() + datetime.timedelta(days = dias)
	return Pregunta.objects.create(texto = texto, fec_pub = time)

class PreguntaModelTests(TestCase):
	def test_es_reciente_con_fecha_futura(self):
		# test esReciente() con pregunta con fecha futura
		time = timezone.now() + datetime.timedelta(days = 30)
		pregunta = Pregunta(fec_pub = time)
		self.assertIs(pregunta.esReciente(), False)

	def test_es_reciente_con_pregunta_antigua(self):
		# test esReciente() con pregunta de hace más de un día
		time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
		pregunta = Pregunta(fec_pub = time)
		self.assertIs(pregunta.esReciente(), False)

	def test_es_reciente_con_pregunta_reciente(self):
		# test esReciente() con pregunta reciente
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		pregunta = Pregunta(fec_pub = time)
		self.assertIs(pregunta.esReciente(), True)

class PreguntaIndexViewTests(TestCase):
	def test_no_hay_preguntas(self):
		response = self.client.get(reverse('encuestas:encuestas'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "La lista está vacía")
		self.assertQuerysetEqual(response.context['lista'], [])

	def test_pregunta_pasada(self):
		pregunta = crear_pregunta(texto = "Pregunta pasada", dias = -30)
		response = self.client.get(reverse('encuestas:encuestas'))
		self.assertQuerysetEqual(
						response.context['lista'],
						[pregunta],
		)

	def test_pregunta_futura(self):
		crear_pregunta(texto = "Pregunta futura", dias = 30)
		response = self.client.get(reverse('encuestas:encuestas'))
		self.assertContains(response, "La lista está vacía")
		self.assertQuerysetEqual(response.context['lista'], [])

	def test_pregunta_futura_y_pregunta_pasada(self):
		pregunta_pasada = crear_pregunta(texto = "Pregunta pasada", dias = -30)
		pregunta_futura = crear_pregunta(texto = "Pregunta futura", dias = 30)
		response = self.client.get(reverse('encuestas:encuestas'))
		self.assertQuerysetEqual(
			response.context['lista'],
			[pregunta_pasada],
		)

	def test_dos_preguntas_pasadas(self):
		pregunta1 = crear_pregunta(texto = "Pregunta pasada 1", dias = -30)
		pregunta2 = crear_pregunta(texto = "Pregunta pasada 2", dias = -3)
		response = self.client.get(reverse('encuestas:encuestas'))
		self.assertQuerysetEqual(
			response.context['lista'],
			[pregunta2, pregunta1],
		)

class PreguntaDetailViewTests(TestCase):
	def test_pregunta_futura(self):
		pregunta = crear_pregunta(texto = "Futura", dias = 10000)
		url = reverse('encuestas:detalles', args=(pregunta.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_pregunta_pasada(self):
		pregunta = crear_pregunta(texto = "Pasada", dias = -1000)
		url = reverse('encuestas:detalles', args=(pregunta.id,))
		response = self.client.get(url)
		self.assertContains(response, pregunta.texto)
		self.assertEqual(response.status_code, 200)

