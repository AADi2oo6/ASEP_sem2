# Generated by Django 5.1.7 on 2025-05-07 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0016_alter_facultystt_course_name_alter_facultystt_year_and_more'),
        ('login', '0017_alter_login_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultystt',
            name='course_name',
            field=models.CharField(choices=[('CS', 'CS'), ('IT', 'IT'), ('ENTC', 'ENTC'), ('AIDS', 'AIDS'), ('MEC', 'MEC'), ('AIML', 'AIML'), ('AI', 'AI')], max_length=100),
        ),
        migrations.AlterField(
            model_name='facultystt',
            name='teacher_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timetable_entries', to='login.flogin'),
        ),
        migrations.AlterField(
            model_name='facultystt',
            name='year',
            field=models.CharField(choices=[('TY', 'TY'), ('4Y', '4Y'), ('FY', 'FY'), ('SY', 'SY')], default=None, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='studentstt',
            name='course_name',
            field=models.CharField(choices=[('CS', 'CS'), ('IT', 'IT'), ('ENTC', 'ENTC'), ('AIDS', 'AIDS'), ('MEC', 'MEC'), ('AIML', 'AIML'), ('AI', 'AI')], default='AIML', max_length=100),
        ),
        migrations.AlterField(
            model_name='studentstt',
            name='year',
            field=models.CharField(choices=[('TY', 'TY'), ('4Y', '4Y'), ('FY', 'FY'), ('SY', 'SY')], default=None, max_length=2, null=True),
        ),
    ]
