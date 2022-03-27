from django.test import TestCase

import datetime

from django.test import TestCase

from django.utils import timezone

from .models import Pregunta

# Create your tests here.

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
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		pregunta = Pregunta(fec_pub = time)
		self.assertIs(pregunta.esReciente(), True)
