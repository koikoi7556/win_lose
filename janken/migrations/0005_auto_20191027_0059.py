# Generated by Django 2.2.6 on 2019-10-26 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('janken', '0004_auto_20191026_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='response',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='janken.Response', verbose_name='レスポンス'),
        ),
        migrations.AlterField(
            model_name='match',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='response',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='response',
            name='image_link',
            field=models.TextField(max_length=2000, verbose_name='画像URL'),
        ),
    ]
