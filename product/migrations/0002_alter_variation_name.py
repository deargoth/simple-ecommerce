# Generated by Django 4.0.6 on 2023-02-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
