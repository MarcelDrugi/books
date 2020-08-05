# Generated by Django 3.0.7 on 2020-08-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('published_date', models.CharField(blank=True, max_length=4, null=True)),
                ('average_rating', models.FloatField(blank=True, null=True)),
                ('ratings_count', models.IntegerField(blank=True, null=True)),
                ('thumbnail', models.TextField(blank=True, null=True)),
                ('authors', models.ManyToManyField(to='books.Authors')),
                ('categories', models.ManyToManyField(to='books.Categories')),
            ],
        ),
    ]