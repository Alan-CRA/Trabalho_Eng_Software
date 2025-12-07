import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Streaming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_id', models.PositiveIntegerField(unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('lancamento', models.CharField(blank=True, max_length=20, null=True)),
                ('tempo', models.PositiveIntegerField(blank=True, null=True)),
                ('sinopse', models.TextField(blank=True, null=True)),
                ('nota_media', models.FloatField(blank=True, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=300, null=True)),
                ('backdrop_path', models.CharField(blank=True, max_length=300, null=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atores', models.ManyToManyField(blank=True, to='filmes.ator')),
                ('genero', models.ManyToManyField(blank=True, to='filmes.genero')),
                ('streaming', models.ManyToManyField(blank=True, to='filmes.streaming')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.PositiveIntegerField()),
                ('comentario', models.TextField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('filme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmes.filme')),
            ],
            options={
                'unique_together': {('user', 'filme')},
            },
        ),
    ]
