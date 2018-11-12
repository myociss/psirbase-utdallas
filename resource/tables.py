import django_tables2 as tables
from .models import Sequence

class SequenceTable(tables.Table):

    class Meta:
        model = Sequence
        fields = ('species', 'chromosome', 'start', 'stop', 'sequence_id', 'rna_sequence', 'source', 
            'development_stage', 'target_gene', 'number_mismatches_allowed')
        template_name = 'django_tables2/semantic.html'
