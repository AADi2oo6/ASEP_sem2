# Generated by Django 5.1.7 on 2025-05-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_login_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='year',
            field=models.CharField(choices=[('FY', 'FY'), ('4Y', '4Y'), ('TY', 'TY'), ('SY', 'SY')], default=None, max_length=2, null=True),
        ),
    ]
