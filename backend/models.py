# -*- encoding: utf-8 -*-
from django.db import models
import os, time
# Create your models here.

def rename(instance, filename):
	print instance.numero
	path = "denuncias/"
	if not instance.numero:
		format = time.strftime("%Y%m%d%H%M",time.localtime()) + "-" + filename
	else:
		format = str(instance.numero) +  "_" + time.strftime("%Y%m%d%H%M",time.localtime()) + "_" + filename
	return os.path.join(path, format)

class Tipo(models.Model):
	titulo 	= models.CharField(max_length=30)
	desc	= models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.titulo

class Denuncia(models.Model):
	tipo 		= models.ForeignKey(Tipo)
	numero 		= models.CharField(max_length=30, 
				help_text="Podes ingresar como 09XXXXXXXX, 5959XXXXXXXX o +5959XXXXXXXX")
	screenshot 	= models.ImageField('Captura de pantalla', upload_to=rename, 
				help_text="Si fue una llamada hacer captura del registro de llamadas")
	desc 		= models.TextField('Descripción o comentarios al respecto', null=True, blank=True, 
				help_text="Completar especialmente si fue una llamada")
	check		= models.NullBooleanField(null=True, default=False)
	votsi		= models.IntegerField(null=True, blank=True, default=0)
	votno		= models.IntegerField(null=True, blank=True, default=0)
	added 		= models.DateTimeField('Agregado',auto_now_add=True, null=True, blank=True)

	def validateNumber(self, number):

		if number.startswith('09'):
			new = "5959" + number[2:]
		elif number.startswith('+'):
			new = number[1:]
		else:
			new = number

		if len(new)==12:
			return new
		else:
			return new

	def save(self, *args, **kwargs):
	 	print "entre 1"
	 	print self.numero
	 	self.numero = self.validateNumber(self.numero)
	 	super(Denuncia, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.numero + " - " + unicode(self.tipo)
	

