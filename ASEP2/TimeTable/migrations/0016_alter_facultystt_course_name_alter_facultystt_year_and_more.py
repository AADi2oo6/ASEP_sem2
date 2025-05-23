# Generated by Django 5.1.7 on 2025-05-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0015_alter_facultystt_course_name_alter_facultystt_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultystt',
            name='course_name',
            field=models.CharField(choices=[('CS', 'CS'), ('AIDS', 'AIDS'), ('MEC', 'MEC'), ('ENTC', 'ENTC'), ('AI', 'AI'), ('AIML', 'AIML'), ('IT', 'IT')], max_length=100),
        ),
        migrations.AlterField(
            model_name='facultystt',
            name='year',
            field=models.CharField(choices=[('FY', 'FY'), ('TY', 'TY'), ('SY', 'SY'), ('4Y', '4Y')], default=None, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='studentstt',
            name='course_name',
            field=models.CharField(choices=[('CS', 'CS'), ('AIDS', 'AIDS'), ('MEC', 'MEC'), ('ENTC', 'ENTC'), ('AI', 'AI'), ('AIML', 'AIML'), ('IT', 'IT')], default='AIML', max_length=100),
        ),
        migrations.AlterField(
            model_name='studentstt',
            name='year',
            field=models.CharField(choices=[('FY', 'FY'), ('TY', 'TY'), ('SY', 'SY'), ('4Y', '4Y')], default=None, max_length=2, null=True),
        ),
    ]
