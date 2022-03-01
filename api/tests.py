from django.shortcuts import render
from django.http import JsonResponse
import json

def retour(numero,donnee):
	data = dict({"status":numero,"data":donnee})
	return JsonResponse(data)

def body(request):
	a=request.body.decode('utf-8')
	dictioner = json.loads(a)
	return dictioner

def lister(dictioner,*args):
    liste=[*args]
    if liste == list(dictioner):
        return True
    else :
        return False