# Generated by Django 2.0.6 on 2019-07-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tlist',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=120, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('age', models.CharField(blank=True, max_length=40, null=True)),
                ('expect_salary', models.CharField(blank=True, max_length=60, null=True)),
                ('edu_exp', models.CharField(blank=True, max_length=120, null=True)),
                ('work_exp', models.CharField(blank=True, max_length=20, null=True)),
                ('collage', models.CharField(blank=True, max_length=40, null=True)),
                ('professional', models.CharField(blank=True, max_length=60, null=True)),
                ('expect_place', models.CharField(blank=True, max_length=60, null=True)),
                ('expect_job', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'db_table': 't_resume',
            },
        ),
    ]
