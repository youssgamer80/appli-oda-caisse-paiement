from rest_framework import serializers
from .models import *
from rest_framework.fields import CurrentUserDefault

class AcademicienSerializer(serializers.ModelSerializer):

	class Meta:
		model = Academicien
		fields = ['matricule', 'id', 'nom', 'prenoms','photo']

class PayementSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = Payement
		fields = ('__all__')

class MotifSerializer(serializers.ModelSerializer):

	class Meta:
		model = Motif
		fields = ['libelle', 'id']