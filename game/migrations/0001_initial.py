# Generated by Django 3.2 on 2021-05-07 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_draw', models.BooleanField(default=False)),
                ('host_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
                ('players', models.ManyToManyField(to='game.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('venue', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('teams', models.ManyToManyField(to='game.Team')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champion_team', to='game.team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamRoundScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.round')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.team')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerRoundScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.round')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='looser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loose_team', to='game.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.stage'),
        ),
        migrations.AddField(
            model_name='game',
            name='teams',
            field=models.ManyToManyField(related_name='participated_teams', to='game.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winning_team', to='game.team'),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.team')),
            ],
        ),
    ]