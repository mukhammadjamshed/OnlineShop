# Generated by Django 4.2.6 on 2023-11-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_ordermodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
