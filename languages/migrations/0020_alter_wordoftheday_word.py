# Generated by Django 4.2.1 on 2024-04-11 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0019_dictionary_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordoftheday',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.dictionary'),
        ),
    ]
