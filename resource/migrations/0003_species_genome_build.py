# Generated by Django 2.1.2 on 2018-10-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_informationdoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='genome_build',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
