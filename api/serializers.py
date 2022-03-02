from .models import Payement , Academicien , Motif
from rest_framework import serializers

class PayementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payement

        fields = '__all__'

        id_academicien = serializers.CharField(required=True)
        id_motif = serializers.CharField(required=True)
        montant = serializers.CharField(required=True)
        

class academicienSerialize(serializers.ModelSerializer):

    class Meta:
        model = Academicien

        fields = ['nom' , 'matricule' , 'prenoms' , 'id' , 'date' , 'photo']

    nom = serializers.CharField(required=True)
    prenoms = serializers.CharField(required=True)
    matricule = serializers.CharField(required=True)

class MotifSerialize(serializers.ModelSerializer):
    class Meta:
        model = Motif

        fields = '__all__'
    
    motif = serializers.CharField(required=True)