from django.db import models
from datetime import datetime

today = datetime.now()

# Create your models here.

class Academicien(models.Model):
    id = models.AutoField(primary_key=True)
    matricule = models.CharField(max_length=6,unique=True)
    nom = models.CharField(max_length=255)
    prenoms = models.CharField(max_length=255)
    date = models.DateField(default=today.date())
    photo = models.CharField(max_length=255)
    class Meta:
        db_table = 'academicien'

class Motif(models.Model):
    id = models.AutoField(primary_key=True)
    libelle_motif = models.CharField(max_length=255)
    statut = models.BooleanField(default=True)
    #date = models.DateField(default=today.date())

    class Meta:
        db_table = 'motif'

class Payement(models.Model):
    id = models.AutoField(primary_key=True)
    id_academicien = models.ForeignKey(Academicien, on_delete=models.CASCADE ,db_column="id_academicien",related_name='id_academicien')
    date = models.DateField(default=today.date())
    montant = models.BigIntegerField(default=True)
    status = models.BooleanField(default=True)
    id_motif  = models.ForeignKey(Motif, on_delete=models.CASCADE ,db_column="id_motif",related_name='id_motif')
    class Meta:
        db_table = 'payement'
