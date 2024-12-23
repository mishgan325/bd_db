# Generated by Django 3.2.16 on 2024-12-16 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attack_name', models.CharField(max_length=255)),
                ('framedata', models.IntegerField(blank=True, null=True)),
                ('damage', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'attacks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GameCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255)),
                ('lore', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'game_characters',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'players',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('expiration_date', models.DateField()),
                ('is_active', models.IntegerField()),
            ],
            options={
                'db_table': 'servers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterAttack',
            fields=[
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='table_app.gamecharacter')),
            ],
            options={
                'db_table': 'character_attack',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerCharacterRank',
            fields=[
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='table_app.player')),
                ('character_rank', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'player_character_rank',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerServer',
            fields=[
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='table_app.player')),
            ],
            options={
                'db_table': 'player_server',
                'managed': False,
            },
        ),
    ]
