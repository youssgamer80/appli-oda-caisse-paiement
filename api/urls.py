from django.urls import path,register_converter
from datetime import datetime
from . import views

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy-mm-dd')


urlpatterns = [

    ######## 1ère fonctionnalité
    path('paiements/add/', views.postPayement,),
    path('paiements/', views.ListPayementAPIView.as_view(),),

    ########2ème
    path('academicien/add/',views.addAcad),
    path('academicien/',views.getAcad),
    path('academicien/update/<int:ide>',views.putAcad),
    path('academicien/del/<int:ide>',views.delAcad),
    
    #######################CRUD Motif #################
    path('motif/add/',views.addMotif),
    path('motif/',views.getMotif),
    path('motif/update/<int:ide>',views.putMotif),
    path('motif/del/<int:ide>',views.delMotif),

    ######### 3ème fonctionnalités
    path('paiement/<yyyy-mm-dd:date>',views.getPayementByDate),
    path('paiement/mat/<str:mat>',views.getPayementByMatricule),
    path('paiement/motif/<int:lib>',views.getPayementByMotif),
    path('paiement/<yyyy-mm-dd:date>/<str:mat>/<str:lib>', views.getPayement),

    ####### 4ème fonctionnalité
    path('solde/<yyyy-mm-dd:date>',views.soldeDate),

    # statistiques
     # endpoint Calculs
    path('paiement/stat/motif/<int:lib>',views.getNombrePayementByMotif().as_view()),
    path('paiement/stat/motif/<int:lib>?<jj>/<mm>/<AA>',views.NombreDePaiementMotifParDate.as_view(), ),
    path('paiement/stat/classement', views.ClassementParPaiementAPIView.as_view()),
    path('paiement/stat/estimation/<jj>/<mm>/<AA>', views.Estimation.as_view()),


]