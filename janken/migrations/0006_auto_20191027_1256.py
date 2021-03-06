# Generated by Django 2.2.6 on 2019-10-27 03:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('janken', '0005_auto_20191027_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='response',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='response',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='更新日時'),
        ),
    ]
