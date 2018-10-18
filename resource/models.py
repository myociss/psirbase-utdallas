from django.db import models
import os

class Species(models.Model):

	def save(self, *args, **kwargs):
		self.genus = self.genus.lower()
		self.species_name = self.species_name.lower()
		if self.common_name:
			self.common_name = self.common_name.lower()
		return super(Species, self).save(*args, **kwargs)

	def __str__(self):
		return self.genus.capitalize() + " " + self.species_name

	genus = models.CharField(max_length=50, null=False)
	species_name = models.CharField(max_length=50, null=False)
	common_name = models.CharField(max_length=50, null=True)
	icon = models.FileField(upload_to='species_icons', default='species_icons/default-icon.png', null=False)
	available = models.BooleanField(default=False, null=False)


	class Meta(object):
		verbose_name_plural = 'Species'
		unique_together = ('genus', 'species_name')


class Sequence(models.Model):
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	chromosome = models.CharField(max_length=50, verbose_name='Chr')
	start = models.IntegerField()
	stop = models.IntegerField()
	sequence_id = models.CharField(max_length=50)
	rna_sequence = models.CharField(max_length=35, verbose_name='sequence')
	source = models.CharField(max_length=40)
	development_stage = models.CharField(max_length=50, verbose_name='stage')
	target_gene = models.CharField(max_length=40, verbose_name='target')
	number_mismatches_allowed = models.IntegerField(verbose_name='NM')

	class Meta(object):
		unique_together = ('chromosome', 'start', 'sequence_id', 
			'development_stage', 'target_gene')


class DataSet(models.Model):

	def __str__(self):
   		return self.species.genus + " " + self.species.species_name + " data set"

	species = models.OneToOneField(Species, on_delete=models.CASCADE, primary_key=True)
	cDNA_data = models.FileField(upload_to='data_sets/', blank=True)
	siRNA_data = models.FileField(upload_to='data_sets/', blank=True)
	ncRNA_data = models.FileField(upload_to='data_sets/', blank=True)
	genome_data = models.FileField(upload_to='data_sets/', blank=True)

class InformationDoc(models.Model):
	def __str__(self):
   		return self.document.url

	document = models.FileField(upload_to='infodocs/', blank=False, null=False)
