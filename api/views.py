from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import *
from api.tests import retour
from .serializers import *
from rest_framework.views import APIView
from datetime import datetime
# Create your views here.

############## 1- Enregistrer les paiements #####################

@api_view(['POST'])
def postPayement(request):
    idacad = int(request.data['academicien'])
    motif = int(request.data['motif'])
    date=request.data['date']

    if Academicien.objects.filter(pk=idacad) and Motif.objects.filter(pk=motif):
        id_acad = Academicien.objects.get(pk=idacad)
        motif = Motif.objects.get(pk=motif)
        serializer = PayementSerializer(data=request.data)
        if serializer.is_valid():
            if not Payement.objects.filter(academicien=id_acad,motif=motif,date=date):
                serializer.save()
                return Response({"status":200})
            else:
                return Response({"status":400,"data":""})
        else :
            return Response({"status":401,"data":serializer.errors})
    else:
        return Response({"status":402,"data":""})


class ListPayementAPIView(ListAPIView):
	"""This endpoint list all of the available todos from the database"""
	queryset = Payement.objects.all()
	serializer_class = PayementSerializer


############## 2-CRUD des entités ###############################
####### 1- CRUD Académiciens #########

# a- Create des académiciens

@api_view(['POST'])
def addAcad(request):
    try:
        data = {}
        if request.method == 'POST':
            mat = request.data['matricule']
            if not Academicien.objects.filter(matricule=mat):
                serializer = AcademicienSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return retour(200,serializer.data)
                else:
                    return retour(301,data)
            else :
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)

@api_view(['GET'])
def getAcad(request):
   try:
        data = {}
        if request.method == 'GET':
            acad = Academicien.objects.filter(status=True)
            serializer = AcademicienSerializer(acad, many=True)
            return retour(200,serializer.data)
        else :
            return retour(400,data)
   except:
       return retour(405,data)

@api_view(['PUT'])
def putAcad(request,ide):
    try:
        data = {}
        if request.method == 'PUT':
            if Academicien.objects.filter(pk=ide):
                acad =  Academicien.objects.get(pk=ide)
                serializer = AcademicienSerializer(acad,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return retour(200,serializer.data)
                else:
                    return retour(301,data)
            else :
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)

@api_view(['DELETE'])
def delAcad(request,ide):
    try:
        data = {}
        if request.method == 'DELETE':
            if Academicien.objects.filter(pk=ide):
                acad =  Academicien.objects.get(pk=ide)
                acad.status = False
                acad.save()
                return retour(200,data)
            else :
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)
# b- Lire des académiciens

####### 1- CRUD Motif #########

# a- Create des motifs

@api_view(['POST'])
def addMotif(request):
    try:
        data = {}
        if request.method == 'POST':
            libelle = request.data['libelle']
            if not Motif.objects.filter(libelle__iexact=libelle):
                serializer = MotifSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return retour(200,serializer.data)
                else :
                    return retour(401,data)
            else:
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)

@api_view(['GET'])
def getMotif(request):
    try :
        data = {}
        if request.method == 'GET':
            motif = Motif.objects.filter(status=True)
            serializer = MotifSerializer(motif, many=True)
            return retour(200,serializer.data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)

@api_view(['PUT'])
def putMotif(request,ide):
    try:
        data = {}
        if request.method == 'PUT':
            if Motif.objects.filter(pk=ide):
                motif =  Motif.objects.get(pk=ide)
                if Motif.objects.filter(libelle__iexact=request.data['libelle']).exclude(pk=ide):
                    return retour(301,data)
                serializer = MotifSerializer(motif,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return retour(200,serializer.data)
                else:
                    return retour(301,data)
            else :
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)

@api_view(['DELETE'])
def delMotif(request,ide):
    try:
        data = {}
        if request.method == 'DELETE':
            if Motif.objects.filter(pk=ide):
                motif =  Motif.objects.get(pk=ide)
                motif.status = False
                motif.save()
                return retour(200,data)
            else :
                return retour(300,data)
        else :
            return retour(400,data)
    except:
        return retour(405,data)


############### 3-Liste de tous les payements

@api_view(['GET'])
def getPayementByDate(request,date):
    der =[]
    dos = {}
    if not Payement.objects.filter(date=date):
        return Response({'status':'400',"data": "Motif inexistant"})
    
    payements = Payement.objects.filter(date=date)
    for i in payements:
        dos = {
        "date":i.date,
        "montant":i.montant,
        "heure":i.heure,
        "nom":i.academicien.nom,
        "prenom":i.academicien.prenoms,
        "photo":i.academicien.photo.url,
        "matricule":i.academicien.matricule,
        "motif":i.motif.libelle,
        }
        der.append(dos)
    return JsonResponse({"status": "200", "data": der})
   

@api_view(['GET'])
def getPayementByMotif(request,lib):
    if not Motif.objects.filter(pk=lib):
        return Response({'status':'400'})
    moti = Motif.objects.get(pk=lib)
    payements = Payement.objects.filter(motif=moti.id)
    serializer = PayementSerializer(payements, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getPayementByMatricule(request,mat):

    if not Academicien.objects.filter(matricule=mat):
        return Response({'status':'400'})
        
    acad = Academicien.objects.get(matricule=mat)
    payements = Payement.objects.filter(academicien=acad.pk)
    serializer = PayementSerializer(payements, many = True)
    return Response({"status": "200", "data": serializer.data})

@api_view(['GET'])
def getPayement(request,date,mat,lib):
    if not Payement.objects.filter(date=date) :
        return Response({'status':'400'})
    if not Academicien.objects.filter(matricule=mat):
        return Response({'status':'401'})

    if  not Motif.objects.filter(pk=lib):
        return Response({'status':'402'})

    acad = Academicien.objects.get(matricule=mat)
    moti = Motif.objects.get(pk=lib)
    payements = Payement.objects.filter(date=date,academicien=acad.pk,motif=moti)
    serializer = PayementSerializer(payements, many = True)
    return Response({"status": "200", "data": serializer.data})

########## 4-Solde de la caisse à un moment donné

@api_view(['GET'])
def soldeDate(request,date):
    if not Payement.objects.filter(date=date):
        return Response({'status':'400'})
    soldes = Payement.objects.filter(date=date).aggregate(comme=Sum('montant'))
    ab = soldes['comme']
    return Response({"status": "200", "data": {"solde":ab}})

@api_view(['GET'])
def solde(request):
    if not Payement.objects.all():
        return Response({'status':'400'})
    soldes = Payement.objects.all().aggregate(comme=Sum('montant'))
    ab = soldes['comme']
    return Response({"status": "200", "data": {"solde":ab}})



# Calculs statistiques
class getNombrePayementByMotif(APIView):
    '''Class qui retourne le nombre de payement par motif'''

    def get(self, request, lib):
        nombreRetardEtMr = {}
        if not Motif.objects.filter(pk=lib):
            return Response({'status': '400'})
        moti = Motif.objects.get(pk=lib)
        nombreRetardEtMr[moti.libelle] = Payement.objects.filter(motif=Motif.objects.filter(
            libelle=moti.libelle).values_list('id', flat=True).first()).count()
        return Response(nombreRetardEtMr)


class NombreDePaiementMotifParDate(APIView):
    '''Class qui retourne le nombre de payement pour retart ou pour avoir dit Mr dans une date donnée'''

    def get(self, request,lib, jj, mm, AA):
        nombreRetardEtMrAuneDateDonne = {}
        slug = AA+'-'+mm+'-'+jj
        if not Motif.objects.filter(pk=lib):
            return Response({'status': '400'})
        moti = Motif.objects.get(pk=lib)
        nombreRetardEtMrAuneDateDonne[moti] = Payement.objects.filter(date=slug, motif=Motif.objects.filter(
            libelle=moti).values_list('id', flat=True).first()).count()
        return Response(nombreRetardEtMrAuneDateDonne)

# endpoint du classement des payeurs
class ClassementParPaiementAPIView(APIView):
 # Classement des payement par montant
    def get(self, request):
        result = {}
        queryset = Academicien.objects.all().order_by('-sommeTotalPaieyer')
        for i in queryset:
            result[i.nom + " "+ i.prenoms]= i.sommeTotalPaieyer

        return Response(result)

class Estimation(APIView):
    """Estimation périodoque du solde total"""
    def get(self, request, jj, mm, AA):
        date_format = "%Y-%m-%d"
        slug = AA+'-'+mm+'-'+jj
        date =datetime.now().date()
        # dateFuture : periode pour l'estimation
        dateFuture = datetime.strptime(str(slug),date_format)
        # formatage de la date courante
        date = datetime.strptime(str(date),date_format)
        nbjour = dateFuture - date
        moyenneTotal = Payement.objects.aggregate(Avg('montant'))
        moyenneJour = moyenneTotal["montant__avg"]/Payement.objects.all().count()
        ab =Payement.objects.aggregate(comme=Sum('montant'))
        soldeTotal = ab['comme']
        estimation = soldeTotal+ (moyenneJour*nbjour.days)
        return Response(estimation)
