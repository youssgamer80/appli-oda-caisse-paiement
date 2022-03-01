from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete

# Create your models here.

class Academicien(models.Model):
    status = models.BooleanField(default = False,verbose_name="Statut du academicien")
    matricule = models.CharField(max_length=120, unique=True)
    nom = models.CharField(max_length=50)
    prenoms = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photo', default='', blank = True, null = True,)
    sommeTotalPaieyer=models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)], null=True, blank=True)
    def __str__(self):
        return self.nom+' '+self.prenoms  
    class Meta:
        verbose_name_plural = 'Academiciens'
class Motif(models.Model):
    status = models.BooleanField(default = False, verbose_name="Statut du motif")
    libelle = models.CharField(max_length=200)
    lien = models.ManyToManyField(Academicien, through = 'Payement', related_name='paiement', blank=True, verbose_name = 'Lien')
    def __str__(self):
        return self.libelle

class Payement(models.Model):
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    montant = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(0.01), MaxValueValidator(500)])
    academicien = models.ForeignKey(Academicien, related_name = 'pay_acad', on_delete = models.CASCADE)
    motif = models.ForeignKey(Motif, related_name = 'pay_motif', on_delete = models.CASCADE)
    def __str__(self):
        return "Payement de " + str(self.montant)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['date', 'academicien', 'motif'], name='uniqueKey')]
        verbose_name_plural = 'Payements'
    


def update_academicien_sommeTotalPaieyer(instance, created, **kwargs):
    academicien = instance.academicien
    total = sum([p.montant for p in academicien.pay_acad.all()])
    academicien.sommeTotalPaieyer=total
    academicien.save()

def delete_and_update_academicien_sommeTotalPaieyer(instance, **kwargs):
    academicien = instance.academicien
    total = sum([p.montant for p in academicien.pay_acad.all()])
    academicien.sommeTotalPaieyer=total
    academicien.save()


post_save.connect(
receiver=update_academicien_sommeTotalPaieyer,
sender=Payement
)

post_delete.connect(
receiver=delete_and_update_academicien_sommeTotalPaieyer,
sender=Payement
)
