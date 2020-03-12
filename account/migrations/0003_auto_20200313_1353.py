# Generated by Django 3.0.3 on 2020-03-13 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200312_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='discount_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.DiscountPlan'),
        ),
        migrations.AlterField(
            model_name='user',
            name='discount_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.DiscountInformation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Subscription'),
        ),
    ]
