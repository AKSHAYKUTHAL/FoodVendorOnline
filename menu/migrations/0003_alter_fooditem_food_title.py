# Generated by Django 5.0 on 2023-12-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]