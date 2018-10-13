from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
import csv
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.admin import AdminSite
from io import TextIOWrapper

from .models import Species, DataSet, Sequence

class DataSetAdmin(admin.ModelAdmin):
    model = DataSet

class SpeciesAdmin(admin.ModelAdmin):
    model = Species

class SequenceAdmin(admin.ModelAdmin):
    model = Sequence
    change_list_template = 'admin/resource/sequence/sequence_changelist.html'

    def validate(self, obj):
        try:
            obj.clean()
            return None
        except ValidationError as e:
            return "\n".join(e.messages)

    def import_csv(self, request):
        f = TextIOWrapper(request.FILES['upload-file'].file, encoding=request.encoding)
        reader = csv.reader(f, delimiter='\t')
        for row_num, row in enumerate(reader):
            species_str = row[-1].split('_')
            if len(species_str) != 2:
                self.message_user(request, 
                    'Error in row ' + str(row_num + 1) + ": invalid species name", level='warning')
                return redirect('..')
            
            genus = species_str[0].lower()
            species_name = species_str[1].lower()

            if Species.objects.filter(genus=genus, species_name=species_name).exists():
                species = Species.objects.get(genus=genus, species_name=species_name)
            else:
                species = Species(genus=genus, species_name=species_name)
                errors = self.validate(species)
                if errors:
                    self.message_user(request, 
                    'Error in row ' + str(row_num + 1) + ":" + errors, level='warning')
                    return redirect('..')
                species.save()


            if Sequence.objects.filter(chromosome=row[0], start=row[1], sequence_id=row[3], 
			    development_stage=row[6], target_gene=row[7]).exists():
                sequence = Sequence.objects.get(chromosome=row[0], start=row[1], sequence_id=row[3], 
			        development_stage=row[6], target_gene=row[7])
                sequence.stop=row[2]
                sequence.rna_sequence=row[4]
                sequence.source=row[5]
                sequence.number_mismatches_allowed=row[8]
            else:
                sequence = Sequence(chromosome=row[0], start=row[1], stop=row[2],
                            sequence_id=row[3], rna_sequence=row[4], source=row[5], development_stage=row[6],
                            target_gene=row[7], number_mismatches_allowed=row[8])
                sequence.species = species
            errors = self.validate(sequence)
            if errors:
                self.message_user(request, 
                'Error in row ' + str(row_num + 1) + ":" + errors, level='warning')
                return redirect('..')
            sequence.save()
            
            if not species.available:
                species.available = True
                species.save()
            

        self.message_user(request, "Your csv file has been imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        sequence_admin_urls = [
            path('import-csv/', self.import_csv),
        ]
        return sequence_admin_urls + urls


class PsiRnaAdminSite(AdminSite):
    site_header = 'RNA Database Admin'

psirna_admin_site = PsiRnaAdminSite(name='admin')
psirna_admin_site.register(Species, SpeciesAdmin)
psirna_admin_site.register(DataSet, DataSetAdmin)
psirna_admin_site.register(Sequence, SequenceAdmin)