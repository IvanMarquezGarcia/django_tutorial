import datetime

from django.db import models

from django.utils import timezone

# Create your models here.

class Pregunta(models.Model):
	texto = models.CharField(max_length = 200)
	fec_pub = models.DateTimeField('fecha de publicación')

	def __str__(self):
		return self.texto

	def esReciente(self):
		return self.fec_pub >= (timezone.now() - datetime.timedelta(days=1))



class Eleccion(models.Model):
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	texto = models.CharField(max_length = 200)
	votos = models.IntegerField(default = 0)

	def __str__(self):
		return self.texto
