# Generated by Django 5.2.1 on 2025-05-24 14:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glace', '0002_create_tub_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('flavor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glace.flavor')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoops', to='glace.order')),
            ],
        ),
    ]
