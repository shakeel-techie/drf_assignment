# Generated by Django 3.0.5 on 2020-04-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='source_type',
            field=models.CharField(blank=True, choices=[('S1', 'SourceType 1'), ('S2', 'SourceType 2')], max_length=20, null=True),
        ),
    ]