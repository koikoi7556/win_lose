# Generated by Django 2.2.6 on 2019-10-26 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('janken', '0002_auto_20191026_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='image_link',
            field=models.TextField(max_length=1000, verbose_name='画像リンク'),
        ),
    ]