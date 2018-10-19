from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Species, Sequence, InformationDoc
from .tables import SequenceTable
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport


def index(request):
    available_species = Species.objects.filter(available=True)
    if InformationDoc.objects.exists():
        doc = InformationDoc.objects.latest('id')
    else:
        doc = None
    context = {'species_list': available_species, 'info_doc': doc}
    return render(request, 'resource/index.html', context)    


def search(request):
    q = request.GET.get('sequence', '')
    print(request.GET)

    if not q:
        messages.error(request, 'Please enter a sequence.')
        return redirect('index')

    search_type = request.GET.get('search-type')
    species_id = int(request.GET.get('species-id'))
    mismatches = int(request.GET.get('mismatches'))

    if search_type == 'siRNA sequence':
        accepted_chars = set('tgcauTGCAU')
        if any((c not in accepted_chars) for c in q):
            messages.error(request, 'Invalid character in sequence.')
            return redirect('index')
        sequences = Sequence.objects.filter(species_id=species_id, rna_sequence=q.upper(), 
                        number_mismatches_allowed=mismatches)
    else:
        sequences = Sequence.objects.filter(species_id=species_id, target_gene=q,
                        number_mismatches_allowed=mismatches)
    
    sequence_table = SequenceTable(sequences)
    sequence_table.paginate(page=request.GET.get('page', 1), per_page=25)

    RequestConfig(request).configure(sequence_table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, sequence_table)
        return exporter.response('table.{}'.format(export_format))
    return render(request, 'resource/results.html', {'table': sequence_table})
