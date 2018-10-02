# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Tipas, Irasas
import datetime


def visi(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.GET.has_key('id'):
                a=request.GET['id']
                Irasas.objects.filter(pk=a).update(pab_data=datetime.datetime.now())
            visas_sarasas = Irasas.objects.order_by('reg_data')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/visi.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(autorius=request.user)
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/visi.html', context)
    else:
        return HttpResponseRedirect('login/')

def atlikti(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=False)
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/atlikti.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=False, autorius=request.user)
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/atlikti.html', context)
    else:
        return HttpResponseRedirect('login/')

def neatlikti(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.GET.has_key('id'):
                a=request.GET['id']
                Irasas.objects.filter(pk=a).update(pab_data=datetime.datetime.now())
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=True)
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/index.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=True, autorius=request.user)
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/index.html', context)
    else:
        return HttpResponseRedirect('login/')
def perziura_tipai(request, tipas_id):
    if request.user.is_authenticated and request.user.is_superuser:
        sarasas_pagal_tipus = Irasas.objects.filter(prob_tipas_id=tipas_id)
        context = {'sarasas_pagal_tipus': sarasas_pagal_tipus}
        return render(request, 'helpdesk/tipai.html', context)
    else:
        return HttpResponseRedirect('../../')

def perziura_vienas(request, irasas_id):
    if request.user.is_authenticated and request.user.is_superuser:
        konkretus_irasas = Irasas.objects.filter(pk=irasas_id)
        context = {'konkretus_irasas': konkretus_irasas}
        return render(request, 'helpdesk/irasai.html', context)
    else:
        return HttpResponseRedirect('../../')

def naujas(request):
    if request.user.is_authenticated:
        print(request.POST)
        print(request.POST.keys())
        new_record = {}
        for k,v in request.POST.iteritems():
            if k == 'csrfmiddlewaretoken':
                continue
            new_record[k] = v
        print(new_record)
        if new_record:
            q=Irasas(problemos_aprasymas=new_record.get('problemos_aprasymas'), kabineto_nr=new_record.get('kabineto_nr'),\
                    autorius=new_record.get('autorius'), reg_data=datetime.datetime.now(), pab_data=None, komentaras="",\
                    prob_tipas_id=new_record.get('prob_tipas_id'))
            q.save()
            return HttpResponseRedirect('../')
        else:
            pass
        return render(request, 'helpdesk/naujas.html')
    else:
        return HttpResponseRedirect('login/')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'helpdesk/login.html')
    else:
        return render(request, 'helpdesk/login.html')

def logout(request):
    def logout_view(request):
        logout(request)
        return HttpResponseRedirect('')

def nvartotojas(request):
    if request.user.is_authenticated and request.user.is_superuser:
        print(request.POST)
        print(request.POST.keys())
        new_user = {}
        for k,v in request.POST.iteritems():
            if k == 'csrfmiddlewaretoken':
                continue
            new_user[k] = v
        print(new_user)
        if new_user:
            user=User.objects.create_user(username=new_user.get('username'), password=new_user.get('password'),\
                    is_superuser=new_user.get('is_superuser'))
            user.save()
            return HttpResponseRedirect('../')
        else:
            pass
        return render(request, 'helpdesk/nvartotojas.html')
    else:
        return HttpResponseRedirect('../login/')

