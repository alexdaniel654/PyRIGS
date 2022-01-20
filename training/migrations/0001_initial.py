# Generated by Django 3.2.11 on 2022-01-04 20:08

import RIGS.models
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('RIGS', '0043_auto_20211027_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Training Categories',
            },
        ),
        migrations.CreateModel(
            name='TrainingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='training.trainingcategory')),
            ],
            options={
                'ordering': ['category__reference_number', 'reference_number'],
                'unique_together': {('reference_number', 'active', 'category')},
            },
        ),
        migrations.CreateModel(
            name='TrainingLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('department', models.IntegerField(blank=True, choices=[(0, 'Sound'), (1, 'Lighting'), (2, 'Power'), (3, 'Rigging'), (4, 'Haulage')], null=True)),
                ('level', models.IntegerField(choices=[(0, 'Technical Assistant'), (1, 'Technician'), (2, 'Supervisor')])),
                ('icon', models.CharField(blank=True, max_length=20, null=True)),
                ('prerequisite_levels', models.ManyToManyField(blank=True, related_name='prerequisites', to='training.TrainingLevel')),
            ],
            bases=(models.Model, RIGS.models.RevisionMixin),
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('RIGS.profile', RIGS.models.RevisionMixin),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TrainingLevelRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.IntegerField(choices=[(0, 'Training Started'), (1, 'Training Complete'), (2, 'Passed Out')])),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.trainingitem')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='training.traininglevel')),
            ],
            options={
                'unique_together': {('level', 'item')},
            },
            bases=(models.Model, RIGS.models.RevisionMixin),
        ),
        migrations.CreateModel(
            name='TrainingLevelQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed_on', models.DateTimeField(null=True)),
                ('confirmed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirmer', to='training.trainee')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.traininglevel')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level_qualifications', to='training.trainee')),
            ],
            options={
                'ordering': ['-confirmed_on'],
                'unique_together': {('trainee', 'level')},
            },
            bases=(models.Model, RIGS.models.RevisionMixin),
        ),
        migrations.CreateModel(
            name='TrainingItemQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.IntegerField(choices=[(0, 'Training Started'), (1, 'Training Complete'), (2, 'Passed Out')])),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.trainingitem')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications_granted', to='training.trainee')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications_obtained', to='training.trainee')),
            ],
            options={
                'order_with_respect_to': 'item',
                'unique_together': {('trainee', 'item', 'depth')},
            },
        ),
    ]