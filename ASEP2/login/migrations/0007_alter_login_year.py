# Generated by Django 5.1.7 on 2025-05-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_flogin_fno_login_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='year',
            field=models.CharField(choices=[('SY', 'SY'), ('4Y', '4Y'), ('TY', 'TY'), ('FY', 'FY')], default=None, max_length=2, null=True),
        ),
    ]
