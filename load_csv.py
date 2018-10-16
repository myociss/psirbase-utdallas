import sys, os, django, csv
sys.path.append('psirbase')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psirbase.settings')
django.setup()

from resource.models import Sequence, Species

def validate(obj):
    try:
        obj.clean()
        return None
    except ValidationError as e:
        return "\n".join(e.messages)

with open(sys.argv[1]) as f:
    reader = csv.reader(f, delimiter='\t')
    for row_num, row in enumerate(reader):
        species_str = row[-1].split('_')
        if len(species_str) != 2:
            print('Error in row ' + str(row_num + 1) + ': invalid species name')
            exit()
        
        genus = species_str[0].lower()
        species_name = species_str[1].lower()

        if Species.objects.filter(genus=genus, species_name=species_name).exists():
            species = Species.objects.get(genus=genus, species_name=species_name)
        else:
            species = Species(genus=genus, species_name=species_name)
            errors = validate(species)
            if errors:
                print( 'Error in row ' + str(row_num + 1) + ":" + errors)
                exit()
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
        errors = validate(sequence)
        if errors:
            print('Error in row ' + str(row_num + 1) + ":" + errors)
            exit()
        sequence.save()
        
        if not species.available:
            species.available = True
            species.save()