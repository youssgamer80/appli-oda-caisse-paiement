from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payement , Academicien , Motif
from .serializers import PayementSerializers , academicienSerialize , MotifSerialize
from rest_framework.decorators import   api_view , renderer_classes
from datetime import datetime
from rest_framework import status
from . import validators
import json
import os

today = datetime.now()


@api_view(['GET'])
def getAllPayement(request):
    allData = Payement.objects.filter(status=True)
    serializeData = PayementSerializers(allData,many=True)

    allAcademicien = Academicien.objects.all()
    allAcademicienSerialeData = academicienSerialize(allAcademicien,many=True)

    returnData = []

    for acad in allAcademicienSerialeData.data  :
        for paye in serializeData.data :
            if paye['id_academicien']==acad['id']:
                returnData.append(acad)


    return Response({'status':True,'content':returnData})

@api_view(['GET'])
def getSignlePayement(request ,id_academicien,id_motif):
    filterPayment = Payement.objects.filter(id_academicien=id_academicien)



@api_view(['GET'])
def soldeCagnotte(request):
    allData = Payement.objects.all()

    # view data
    serializeData = PayementSerializers(allData,many=True)

    AllAcademicien = Academicien.objects.all().count()
    AllMotif = Motif.objects.all().count()
    AllPayement = Payement.objects.all().count()

    solde = 0

    for money in serializeData.data:
        solde = solde + money['montant']

    return Response({'status':True,'solde':solde , 'nbre_academicien' : AllAcademicien , 'nbre_motif':AllMotif , 'nbre_payement':AllPayement})


@api_view(['GET'])
def getStatistique(request):

    allData = Payement.objects.all()
    serializeData = PayementSerializers(allData,many=True)

    mounth = {'01':{'payement':0 , 'retard':0},'02':{'payement':0 , 'retard':0},'03':{'payement':0 , 'retard':0},'04':{'payement':0 , 'retard':0},'05':{'payement':0 , 'retard':0},'06':{'payement':0 , 'retard':0},'07':{'payement':0 , 'retard':0},'08':{'payement':0 , 'retard':0},'09':{'payement':0 , 'retard':0},'10':{'payement':0 , 'retard':0},'11':{'payement':0 , 'retard':0},'12':{'payement':0 , 'retard':0}}

    for paye in serializeData.data:
        pass



@api_view(['GET'])
def getAllMotif(request):
    allMotif = Motif.objects.filter(status=True)
    serializeData = MotifSerialize(allMotif,many=True)


    return Response({'status':True,'content':serializeData.data})


@api_view(['POST'])
def createPaymement(request):
    allAcademicien = Academicien.objects.all()

    allPayement = Payement.objects.all()
    serializeAllPayement = PayementSerializers(allPayement,many=True)

    allAcademicienSerializeData = academicienSerialize(allAcademicien,many=True)

    allMotif = Motif.objects.all()
    motifSerialize = MotifSerialize(allMotif,many=True)

    body = json.loads(json.dumps(request.data))

    #valid = validators.validateApi(body,PayementSerializers)
    #if valid["success"] :

    isFound = False

    for data in allAcademicienSerializeData.data:
        if data["matricule"] == body["id_academicien"]:
            isFound = True

    if isFound:

            isMotif = False

            for motif in motifSerialize.data:
                if motif["id"] == body["id_motif"]:
                    isMotif = True

            if isMotif:

                y_1 , m_1 , d_1 = [int(x) for x in (str(today.date())).split('-')]

                isRegister = False

                for item in serializeAllPayement.data:
                    y_2 , m_2 , d_2 = [int(x) for x in (str(item['date'])).split('-')]
                    if [y_1,m_1,d_1] == [y_2,m_2,d_2] and item["id_motif"] == body["id_motif"]:
                        isRegister = True

                if isRegister:
                    return Response({'status':False , 'msg':'Pour ce motif cette personne est déjà enregistré pour la journée.'})
                else:
                    currentModif = Motif.objects.get(id=body["id_motif"])
                    currentAcademicien = Academicien.objects.get(matricule=body["id_academicien"])
                    paye = Payement(
                        id_academicien = currentAcademicien,
                        id_motif = currentModif ,
                        montant = body["montant"]
                    )
                    paye.save()

                    return Response({'status':True , 'msg':'Payement effectué avec succès'})
            else:
                return Response({'status':False , 'msg':'Cet notif est inconnu de nos registres  .'})
    else:
        return Response({'status':False , 'msg':'Desolé cet academicien est inconnu de nos registres .'})

    #else :
    #    return Response({'status':False , 'content':'Oups! une erreur s\'est produite lors de l\'enregistrement','code':status.HTTP_400_BAD_REQUEST,'errors':valid["errors"]})


@api_view(['POST'])
def createMotif(request):
        isFound = False
        body = json.loads(json.dumps(request.data))
        singleMotif = Motif.objects.all()
        singleMotif = MotifSerialize(singleMotif,many=True)

        valid = validators.validateApi(body,MotifSerialize)

        if valid["success"] :

            for data in singleMotif.data:
                if data['motif']==body['motif']:
                        isFound = True

            if isFound:
                return Response({'status':False , 'msg':'Oups! desolé ce motif est déjà enregistré .'})
            else:
                s = Motif(**body)
                s.date = today.date()
                s.save()
                return Response({'status':True , 'msg':'Hey, votre motif à belle et bien été enregistré ....'})
        else :
            return Response({'status':False , 'content':'Oups! une erreur s\'est produite lors de l\'enregistrement','code':status.HTTP_400_BAD_REQUEST,'errors':valid["errors"]})

@api_view(['DELETE'])
def deletePayement(request , id_paye):
    allData = Payement.objects.all()
    serializeData = PayementSerializers(allData,many=True)

    isFound = False

    for data in serializeData.data:
        if data['id'] == id:
            isFound = True

    if isFound:
        paye = Payement.objects.get(id=id_paye)
        paye.status = False
        paye.save()

        return Response({'status':True , 'msg':'Suppression effectué avec succès .'})

    else:
        return Response({'status':False , 'msg':'Element inexistant, suppression impossible.'})

@api_view(['DELETE'])
def deleteMotif(request,id):
        isFound = False
        body = json.loads(json.dumps(request.data))
        singleMotif = Motif.objects.all()
        singleMotif = MotifSerialize(singleMotif,many=True)

        for data in singleMotif.data:
            if data['id']==id:
                    isFound = True
        if isFound:
            s=Motif.objects.get(id=id)
            s.status = False
            s.save()
            return Response({'status':True , 'msg':'Ce motif a été supprimé avec succès....'})


        else:
            return Response({'status':True , 'msg':'Ce motif n\'existe pas....'})

@api_view(['PUT'])
def updateMotif(request,id_motif):
        isFound = False
        body = json.loads(json.dumps(request.data))
        singleMotif = Motif.objects.all()
        singleMotif = MotifSerialize(singleMotif,many=True)

        for data in singleMotif.data:
            if data['id']==id_motif:
                    isFound = True
        if isFound:

            valid = validators.validateApi(body,MotifSerialize)

            if valid["success"] :

                isExist = False

                for data in singleMotif.data:
                    if data['motif']==body['motif'] and data['id']!=id_motif:
                        isExist = True

                if isExist :
                    return Response({'status':False , 'msg':'Oups! desolé ce motif est déjà enregistré .'})
                else:
                    s=Motif.objects.get(id=id_motif)
                    s.motif= body['motif']
                    s.save()
                    return Response({'status':True , 'msg':'le motif a été modifié avec succès'})
            else:
                return Response({'status':False , 'content':'Oups! une erreur s\'est produite lors de l\'enregistrement','code':status.HTTP_400_BAD_REQUEST,'errors':valid["errors"]})
        else:
            return Response({'status':True , 'msg':'Ce motif n\'existe pas veuillez l\'ajouter....'})

@api_view(['GET'])
def AllAcademicien(request):
        academiciens=Academicien.objects.all()
        serializers=academicienSerialize(academiciens, many=True)
        return Response({'status':True , 'content':serializers.data})

@api_view(['GET'])
def OneAcademicien(request, matricule):
        allAcademicien=Academicien.objects.all()
        dataAllacdemicien=academicienSerialize(allAcademicien, many=True)

        isFound=False

        if matricule and matricule!="":

            for data in dataAllacdemicien.data :
                    if data['matricule']==matricule:
                            isFound=True

            if isFound:

                onacademicien=Academicien.objects.get(matricule=matricule)
                getserializer=academicienSerialize(onacademicien, many=False)
                return Response({'status':True , 'content':getserializer.data})

            else:
                return Response({'status':False , 'content':'Oups! la reference de cet academicien n\'a pas été trouvé impossible de vous transmettre les informations .'})
        else:
             return Response({'status':False , 'content':'Oups! reference non trouvé, cet academicien semble ne pas exister dans nos registres .','code':status.HTTP_400_BAD_REQUEST})

@api_view(['DELETE'])
def deletAcademicien(request, id_acad):

        allAcademicien=Academicien.objects.all()

        allAcademicien_seriralizer=academicienSerialize(allAcademicien, many=True)

        isFound=False

        for data in allAcademicien_seriralizer.data:

                if data['id']==id_acad:
                    isFound=True
                    academicienDeleted = data

        if isFound:

            if os.path.isfile('media/'+academicienDeleted['photo']) :

                os.remove('media/'+academicienDeleted['photo'])

                academicienDeleted = Academicien.objects.get(id=id_acad)
                academicienDeleted.delete()

                return Response({'status': True , 'content':'Hey, la suppression à été effectué avec succès .'})

            else :
                return Response({'status': False , 'content':'Oups! une erreur est survenue lors de la suppression merci de réessayer .'})

        else:

            return Response({'status':False , 'content':'Oups! la reference de cet academicien n\'a pas été trouvé impossible de faire la suppression .'})

@api_view(['POST'])
def AcademicienCreate(request):

    body = request.data
    allAcademicien = Academicien.objects.all()
    Acadserializers = academicienSerialize(allAcademicien,many=True)

    isFound = False

    for acad in Acadserializers.data:
        if body["matricule"] == acad["matricule"]:
            isFound = True

    if isFound :
        return Response({'status':False , 'content':'Desolé cet academicien est déjà connu de nos registres.'})

    else:


        upload = request.FILES['photo']

        fss = FileSystemStorage()

        file_ext = os.path.splitext(upload.name)[1]



        if file_ext in ['.png'  , '.jpeg' , '.jpg'] :

            file_name_to_save = body["matricule"]+file_ext

            data={
                "nom":body["nom"],
                "prenoms":body["prenoms"],
                "matricule":body["matricule"],
                "photo":file_name_to_save,
            }

            valid = validators.validateApi(data,academicienSerialize)

            if valid["success"]:

                fss.save(file_name_to_save, upload)
                Acadserializers = valid["data"]
                Acadserializers.save()

                return Response({'status':True ,  'content':'Hey, enregistremednt effectué avec succès ...','code':status.HTTP_201_CREATED})
            else :
                return Response({'status':False , 'content':'Oups! une erreur s\'est produite lors de l\'enregistrement','code':status.HTTP_400_BAD_REQUEST,'errors':valid["errors"]})

        else:
            return Response({'status':False , 'content':'Oups! votre photo ne respect pas le format autorisé merci de réessayer . '})




@api_view(['PUT'])
def AcademicienUpdate(request,id_acad):

    body = json.loads(json.dumps(request.data))

    Academserializers = Academicien.objects.all()
    Academerialize= academicienSerialize(Academserializers,many=True)

    isFound = False

    for acad in Academerialize.data:
        if acad['id'] == id_acad:
            isFound = True


    if isFound:

        isExist = False

        for acad in Academerialize.data:
            if acad["matricule"] == body["matricule"]:
                isExist = True

        if isExist:

            return Response({'status':False , 'content':'Le nouveau matricule renseigné appartient déjà à un autre academicien, impossible de faire la modification .'})

        else:

            valid = validators.validateApi(body,academicienSerialize)

            if valid["success"]:
                s = Academicien.objects.get(id=id_acad)

                s.nom = body['nom']
                s.matricule = body['matricule']
                s.prenoms = body['prenoms']

                s.save()

                return Response({'status':True , 'content':'Hey, modification effectué avec succès ...','code':status.HTTP_201_CREATED})
            else :
                return Response({'status':False , 'content':'Oups! une erreur s\'est produite lors de l\'enregistrement','code':status.HTTP_400_BAD_REQUEST,'errors':valid["errors"]})


    else:
        return Response({'status':False , 'content':'Oups! la reference transmise ne correspond à aucun academcien de nos registres .'})
