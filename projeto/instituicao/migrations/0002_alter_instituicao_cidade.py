# Generated by Django 4.2.16 on 2025-05-02 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instituicao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituicao',
            name='cidade',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cidade'),
        ),
    ]
