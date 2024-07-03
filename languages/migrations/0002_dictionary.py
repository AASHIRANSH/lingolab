# Generated by Django 4.2.1 on 2024-02-24 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('pos', models.CharField(max_length=50)),
                ('cefr', models.CharField(blank=True, max_length=10, null=True)),
                ('pronounciation', models.JSONField(blank=True, null=True, verbose_name='Pronounciation')),
                ('forms', models.JSONField(blank=True, null=True, verbose_name='Forms')),
                ('senses', models.JSONField(verbose_name='Senses')),
                ('word_details', models.JSONField(blank=True, null=True, verbose_name='Word Details')),
                ('related_post', models.ManyToManyField(blank=True, to='languages.post')),
            ],
        ),
    ]
