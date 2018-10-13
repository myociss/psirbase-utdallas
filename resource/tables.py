import django_tables2 as tables
from .models import Sequence

class SequenceTable(tables.Table):

    class Meta:
        model = Sequence
        template_name = 'django_tables2/semantic.html'
