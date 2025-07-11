# Generated by Django 5.2.3 on 2025-06-27 02:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('total_points', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('submission_type', models.CharField(choices=[('file', 'File Upload'), ('text', 'Text Entry'), ('both', 'Both')], default='file', max_length=50)),
                ('is_group_assignment', models.BooleanField(default=False)),
                ('max_attempts', models.PositiveSmallIntegerField(default=1)),
                ('solution_file', models.FileField(blank=True, null=True, upload_to='assignment_solutions/')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(choices=[('midterm', 'Midterm Exam'), ('final', 'Final Exam'), ('quiz', 'Quiz'), ('project', 'Project')], max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField()),
                ('total_points', models.PositiveSmallIntegerField()),
                ('weight', models.PositiveSmallIntegerField(help_text='Weight in percentage', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.PositiveSmallIntegerField(blank=True, help_text='Duration in minutes', null=True)),
                ('instructions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('curve_adjustment', models.SmallIntegerField(default=0)),
                ('grading_scale', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('text_entry', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='submissions/%Y/%m/%d/')),
                ('grade', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('is_late', models.BooleanField(default=False)),
                ('attempt_number', models.PositiveSmallIntegerField(default=1)),
                ('graded_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-submitted_at'],
            },
        ),
    ]
