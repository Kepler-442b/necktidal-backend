# Generated by Django 3.0.3 on 2020-03-13 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200313_1353'),
        ('music', '0008_auto_20200313_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Gender'),
        ),
    ]
