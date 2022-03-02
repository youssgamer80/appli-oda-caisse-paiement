from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # payement urls

    path('all-payement/',views.getAllPayement),
    path('create-payement/',views.createPaymement),

    # counter data urls
    path('counte-data-items/',views.soldeCagnotte),

    # motif urls 

    path('list-of-motif/',views.getAllMotif),
    path('create-new-motif/',views.createMotif),
    path('deleted-motif/<int:id>',views.deleteMotif),
    path('update-motif/<int:id_motif>',views.updateMotif),

    # academicien urls 

    path('create-academicien/',views.AcademicienCreate),
    path('view-all-academicien/',views.AllAcademicien),
    path('get-single-academicien/<str:matricule>',views.OneAcademicien),
    path('academicien-update-data/<int:id_acad>',views.AcademicienUpdate),
    path('delete-academicien/<int:id_acad>',views.deletAcademicien)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)