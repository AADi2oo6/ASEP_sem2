# Generated by Django 5.1.7 on 2025-05-07 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_alter_login_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='year',
            field=models.CharField(choices=[('4Y', '4Y'), ('SY', 'SY'), ('FY', 'FY'), ('TY', 'TY')], default=None, max_length=2, null=True),
        ),
    ]
