# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#apsirasome objektus, ju atributus ir funkcijas
class Tipas(models.Model):
    prob_tipas=models.CharField(max_length=30)
    def __str__(self):
        return self.prob_tipas

class Irasas(models.Model):
    """ForeignKey padeda prie Iraso prijungti Tipus
    DateTimeField reikia leisti kad butu tuscias, kitaip negalima bus sukurti
    iraso kuris nebutu issprestas"""
    prob_tipas = models.ForeignKey(Tipas, on_delete=models.CASCADE)
    problemos_aprasymas = models.CharField(max_length=200)
    kabineto_nr = models.CharField(max_length=30)
    autorius = models.CharField(max_length=50)
    reg_data = models.DateTimeField('Iraso data')
    pab_data = models.DateTimeField('Atlikimo data', blank=True, null=True)
    komentaras = models.CharField(max_length=200)
    def __str__(self):
        return self.problemos_aprasymas
    def atliktas(self):
        return self.pab_data != None

