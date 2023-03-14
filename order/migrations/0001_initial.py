# Generated by Django 4.1.7 on 2023-03-14 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_items', models.PositiveIntegerField()),
                ('total_value', models.FloatField()),
                ('status', models.CharField(choices=[('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'), ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado')], default='C', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255)),
                ('product_id', models.PositiveIntegerField()),
                ('variation', models.CharField(blank=True, max_length=255, null=True)),
                ('variation_id', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('promotional_price', models.FloatField(default=0)),
                ('quantity', models.PositiveIntegerField()),
                ('image', models.CharField(max_length=2000)),
                ('slug', models.CharField(max_length=265)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]
