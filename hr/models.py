from django.db import models

# Create your models here.

class House(models.Model):
	house_name = models.CharField(max_length=50)

	def __str__(self):
		return self.house_name

class Rulebook(models.Model):
	rulebook_name = models.CharField(max_length=50)
	parent_house = models.ForeignKey(House, default = "0000000", on_delete=models.CASCADE)

	def __str__(self):
		return self.rulebook_name

class Rule(models.Model):
	rule_name = models.CharField(max_length=50)
	rule_text = models.CharField(max_length=500)
	parent_rulebook = models.ForeignKey(Rulebook, default = "0000000", on_delete=models.CASCADE)

	def __str__(self):
		return self.rule_name