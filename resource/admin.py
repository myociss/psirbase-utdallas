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
    delete_confirmation_template = 'admin/resource/species/species_delete_confirmation.html'

class PsiRnaAdminSite(AdminSite):
    site_header = 'RNA Database Admin'

psirna_admin_site = PsiRnaAdminSite(name='admin')
psirna_admin_site.register(Species, SpeciesAdmin)
psirna_admin_site.register(DataSet, DataSetAdmin)
