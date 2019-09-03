from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

import qrcode
from io import StringIO
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.

class House(models.Model):
	house_name = models.CharField(max_length=50, unique = True)

	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	qr_code = models.ImageField(upload_to = 'images/qr_codes', default = 'default-qr.jpg')

	def __str__(self):
		return self.house_name

	def save(self, *args, **kwargs):
		self.gen_qr_code()
		super(Model, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('events.views.details', args=[str(self.id)])

	def gen_qr_code(self):
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=6,
			border=0,
		)

		qr.add_data(self.get_absolute_url())
		qr.make(fit=True)

		img = qr.make_image()

		buffer = StringIO.StringIO()
		img.save(buffer)
		filename = 'house-qr-%s.png' % (self.id)
		filebuffer = InMemoryUploadedFile(
			buffer, None, filename, 'image/png', buffer.len, None)
		self.qrcode.save(filename, filebuffer)

class Rulebook(models.Model):
	rulebook_name = models.CharField(max_length=50)
	parent_house = models.ForeignKey(House, default = "0000000", on_delete=models.CASCADE)
	# icon_link = models.CharField(max_length=25)

	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.parent_house.__str__() + "'s " + self.rulebook_name + " Rules"

class Rule(models.Model):
	rule_name = models.CharField(max_length=50)
	rule_text = models.CharField(max_length=500)
	parent_rulebook = models.ForeignKey(Rulebook, default = "0000000", on_delete=models.CASCADE)
	icon_link = models.CharField(max_length=25)

	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.rule_name + " for " + self.parent_rulebook.__str__()