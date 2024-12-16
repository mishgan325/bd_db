from django.db import models


class Attack(models.Model):
    attack_name = models.CharField(max_length=255)
    framedata = models.IntegerField(blank=True, null=True)
    damage = models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.attack_name

    class Meta:

        managed = False
        db_table = 'attacks'


class CharacterAttack(models.Model):
    character = models.OneToOneField('GameCharacter', models.CASCADE, primary_key=True)
    attack = models.ForeignKey(Attack, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'character_attack'
        unique_together = (('character', 'attack'),)


class GameCharacter(models.Model):
    character_name = models.CharField(max_length=255)
    lore = models.CharField(max_length=255)

    def __str__(self):
        return self.character_name
    
    class Meta:
        managed = False
        db_table = 'game_characters'


class PlayerCharacterRank(models.Model):
    player = models.OneToOneField('Player', models.CASCADE, primary_key=True)
    character = models.ForeignKey(GameCharacter, models.CASCADE)
    character_rank = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_character_rank'
        unique_together = (('player', 'character'),)


class PlayerServer(models.Model):
    player = models.OneToOneField('Player', models.CASCADE, primary_key=True)
    server = models.ForeignKey('Server', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'player_server'
        unique_together = (('player', 'server'),)


class Player(models.Model):
    nickname = models.CharField(max_length=255)

    def __str__(self):
        return self.nickname

    class Meta:
        managed = False
        db_table = 'players'


class Server(models.Model):
    location = models.CharField(max_length=255)
    expiration_date = models.DateField()
    is_active = models.IntegerField()

    def __str__(self):
        return self.location

    class Meta:
        managed = False
        db_table = 'servers'
