# Generated by Django 4.0.5 on 2022-06-12 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_employer_brief_alter_employer_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('requirements', models.TextField()),
                ('type', models.CharField(choices=[('on site', 'on site'), ('remote', 'remote')], max_length=120)),
                ('Start_date', models.DateField()),
                ('city', models.CharField(choices=[('Riyadh', 'Riyadh'), ('Tabuk', 'Tabuk'), ('Jeddah', 'Jeddah')], max_length=120)),
                ('category', models.CharField(choices=[('Developer', 'Developer'), ('Designer', 'Designer'), ('Writer', 'Writer'), ('Marketing', 'Marketing'), ('Translator', 'Translator'), ('Videographer', 'Videographer'), ('Accountant', 'Accountant'), (' HR manager', 'HR manager')], max_length=120)),
                ('image', models.TextField()),
                ('employer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employer')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('completed', 'completed')], default='pending', max_length=120)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.jobseeker')),
            ],
        ),
    ]