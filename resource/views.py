from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Species, Sequence
from .tables import SequenceTable

def index(request):
    available_species = Species.objects.filter(available=True)
    context = {'species_list': available_species}
    return render(request, 'resource/index.html', context)    


def search(request):
    q = request.GET.get('sequence', '').upper()
    print(request.GET)

    if not q:
        messages.error(request, 'Please enter a sequence.')
        return redirect('index')

    search_type = request.GET.get('search-type')
    species_id = int(request.GET.get('species-id'))
    mismatches = int(request.GET.get('mismatches'))

    if search_type == 'siRNA sequence':
        accepted_chars = set('TGCAU')
        if any((c not in accepted_chars) for c in q):
            messages.error(request, 'Invalid character in sequence.')
            return redirect('index')
        sequences = Sequence.objects.filter(species_id=species_id, rna_sequence=q, 
                        number_mismatches_allowed=mismatches)
    else:
        sequences = Sequence.objects.filter(species_id=species_id, target_gene=q,
                        number_mismatches_allowed=mismatches)
    sequence_table = SequenceTable(sequences)
    sequence_table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'psiRbase/results.html', {'table': sequence_table})
