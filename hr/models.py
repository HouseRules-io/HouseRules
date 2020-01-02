from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
from django.conf import settings
from colorful.fields import RGBColorField
from django.contrib.auth.models import AbstractUser


import qrcode
from io import BytesIO
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.

class Profile(models.Model):

	user = models.OneToOneField(User, related_name = "profile", on_delete = models.CASCADE)

	@property
	def my_houses(self):
		my_houses = self.user.owned_houses.all()
		my_houses = (my_houses | self.user.visit_houses.all())
		return my_houses

class House(models.Model):
	house_name = models.CharField(max_length=50, unique = True)

	creator = models.ForeignKey(User, related_name = "owned_houses", blank = True, null = True, on_delete=models.CASCADE)
	followers = models.ForeignKey(User, related_name = "visit_houses", blank = True, null = True, on_delete=models.CASCADE)

	hex_id = models.CharField(max_length = 20)
	qr_code = models.ImageField(upload_to = 'images/qr_codes', default = 'qr_codes/default-qr.jpg')

	# color = models.RGBColorField()

	def image_tag(self):
		return mark_safe('<img src="%s" width="150" height="150" />' % (self.qr_code.url))

	image_tag.short_description = 'QR code'


	def __str__(self):
		return self.house_name

	def save(self, *args, **kwargs):
		super(House, self).save(*args, **kwargs)

	def init_qr(self):
		self.hex_id = hex(int(self.pk))[2:]
		self.gen_qr_code()
		self.save()

	def get_absolute_url(self):
		return settings.BASE_URL + reverse('house', args = [str(self.hex_id)])
		# return reverse('house', args=[str(self.hex_id)])

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

		bbuffer = BytesIO()
		# img.save(bbuffer, 'PNG', optimize=True, quality=70)
		filename = 'qr_codes/house-qr-%s.png' % (self.id)
		img.save(bbuffer, format='PNG', quality=100)
		img_content = ContentFile(bbuffer.getvalue(), filename)
		# filebuffer = InMemoryUploadedFile(
		# 	bbuffer, None, filename, 'image/png', bbuffer.getbuffer().nbytes, None)
		self.qr_code.save(filename, img_content, save = True)#filebuffer)

	def copy(self, user):
		new_house = House.objects.create()
		new_house.creator = user
		new_house.house_name = self.house_name + '-copy'

		for rb in self.rulebooks.all():
			rb.copy(new_house, user)

		new_house.init_qr()

		new_house.save()

class Rulebook(models.Model):
	rulebook_name = models.CharField(max_length=50)
	parent_house = models.ForeignKey(House, related_name = "rulebooks", default = "0000000", on_delete=models.CASCADE)
	# icon_link = models.CharField(max_length=25)

	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def copy(self, house, user):
		rulebook_name = self.rulebook_name + "-copy"
		parent_house = house
		creator = user
		new_rb = Rulebook.objects.create(rulebook_name = rulebook_name, parent_house = parent_house, creator = creator)

		for rule in self.rules.all():
			rule.copy(new_rb, user)

		new_rb.save()


	def __str__(self):
		return self.parent_house.__str__() + "'s " + self.rulebook_name + " Rules"

class Rule(models.Model):
	rule_name = models.CharField(max_length=50)
	rule_text = models.CharField(max_length=500)
	parent_rulebook = models.ForeignKey(Rulebook, related_name = "rules", default = "0000000", on_delete=models.CASCADE)
	icon_link = models.CharField(max_length=25, blank = True, null = True)

	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def copy(self, rb, user):
		rule_name = self.rule_name
		rule_text = self.rule_text
		parent_rulebook = rb
		creator = user
		new_rule = Rule.objects.create(rule_name = rule_name, rule_text = rule_text, parent_rulebook = parent_rulebook, creator = creator)

		new_rule.save()

	def __str__(self):
		return self.rule_name + " for " + self.parent_rulebook.__str__()

