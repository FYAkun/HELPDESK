# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Irasas
import ctypes
import datetime


def visi(request):
    """view skirtas atvaizduoti visiems irasams,
    Patikrina ar vartotojas prisijunges:
    Jei vartotojas neprisijunges - nukreipia i prisijungimo langa.
    Jei vartotojas prisijunges,
    tikrina ar vartotojas yra superuser, jei taip,
    patikrinama ar nebuvo daromas GET, jei buvo - Irasas objekte uzdedama atlikimo data.
    Taip pat atvaizduojamas visas gedimu registras
    jei vartotojas ne superuser tiesiog atvaizduojamas jo uzregistruotu gedimu sarasas"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.GET.has_key('id'):
                a=request.GET['id']
                Irasas.objects.filter(pk=a).update(pab_data=datetime.datetime.now())
            visas_sarasas = Irasas.objects.order_by('reg_data').select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/visi.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(autorius=request.user).select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/visi.html', context)
    else:
        return HttpResponseRedirect('login/')

def atlikti(request):
    """View skirtas atvaizduoti atliktus darbus.
    Patikrinama ar prisijunges, jei ne - nukreipiama i login
    Jei prisijunges - sarasas atvaizduojamas pagal teises.
    Jei vartotojas - superuser, jis matys visus atliktus darbus
    Jei vartotojas - ne superuser, jis matys jo registruotus darbus"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=False).select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/atlikti.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=False, autorius=request.user).select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/atlikti.html', context)
    else:
        return HttpResponseRedirect('login/')

def neatlikti(request):
    """Pagrindinis gedimu registro view, rodo aktualius (neisprestus) gedimus
    Neprisijungus nukreipiama i login,
    prisijungus su superuser - atvaizduoja neatliktus darbus, leidzia juos atlikti,
    pasitelkiant GET forma.
    paprastam darbuotojui rodomi jo uzregistruoti sutrikimai, kurie dar nesutvarkyti"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.GET.has_key('id'):
                a=request.GET['id']
                Irasas.objects.filter(pk=a).update(pab_data=datetime.datetime.now())
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=True).select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/neatlikti.html', context)
        else:
            visas_sarasas = Irasas.objects.filter(pab_data__isnull=True, autorius=request.user).select_related('prob_tipas')
            context = {'visas_sarasas': visas_sarasas}
            return render(request, 'helpdesk/neatlikti.html', context)
    else:
        return HttpResponseRedirect('login/')

def perziura_tipai(request, tipas_id):
    """view skirtas perziureti gedimus su tuo paciu tipu.
    si funkcija prieinama tik superuser, paprasti vartotojai nukreipiami i pagrindini langa."""
    if request.user.is_authenticated and request.user.is_superuser:
        sarasas_pagal_tipus = Irasas.objects.filter(prob_tipas_id=tipas_id).select_related('prob_tipas')
        context = {'sarasas_pagal_tipus': sarasas_pagal_tipus}
        return render(request, 'helpdesk/tipai.html', context)
    else:
        return HttpResponseRedirect('../../')

def perziura_vienas(request, irasas_id):
    """view skirtas atsidaryti konkreciam irasui is gedimu registro,
    prieinamas tik superuser, naudojamas jei superuser nori suteikti irasui komentara, kuri matytu vartotojas
    pvz tiketina sprendimo data ir t.t.
    Komentaras irasomas uzpildzius forma ir paspaudus mygtuka.
    sugeneruojamas POST, is post isrenkamas komentaras ir priskiriamas prie atitinkamo Iraso, per iraso id."""
    if request.user.is_authenticated and request.user.is_superuser:
        new_comment = {}
        for k,v in request.POST.iteritems():
            if k == 'csrfmiddlewaretoken':
                continue
            new_comment[k] = v
        if new_comment:
            Irasas.objects.filter(pk=irasas_id).update(komentaras=new_comment.get('komentaras'))
            return HttpResponseRedirect('../../')
        else:
            konkretus_irasas = Irasas.objects.filter(pk=irasas_id).select_related('prob_tipas')
            context = {'konkretus_irasas': konkretus_irasas}
            return render(request, 'helpdesk/irasai.html', context)
    else:
        return HttpResponseRedirect('../../')

def naujas(request):
    """Naujo iraso view.
    Vartotojai gali uzpildyti forma, kuria submitinus
    sugeneruojamas POST, is jo informacija ciklo pagalba sudedama i dicta,
    jei randamas dictas - paimamas vartotojo username, ir sukuriamas naujas irasas,
    kuriame patalpinama informacija is formos, vartotojo username ir dabartine data"""
    if request.user.is_authenticated:
        new_record = {}
        for k,v in request.POST.iteritems():
            if k == 'csrfmiddlewaretoken':
                continue
            new_record[k] = v
        print(new_record)
        if new_record:
                u=request.user
                q=Irasas(problemos_aprasymas=new_record.get('problemos_aprasymas'), kabineto_nr=new_record.get('kabineto_nr'),\
                        autorius=u, reg_data=datetime.datetime.now(), pab_data=None, komentaras="",\
                        prob_tipas_id=new_record.get('prob_tipas_id'))
                q.save()
                return HttpResponseRedirect('../')
        else:
            pass
        return render(request, 'helpdesk/naujas.html')
    else:
        return HttpResponseRedirect('login/')

def login(request):
    """standartinis django login view, prisijungimui prie sistemos.
    Paimami prisijungimo duomenys is formos - ir bandoma vartotoja atpazinti.
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'helpdesk/login.html')
    else:
        return render(request, 'helpdesk/login.html')

def logout(request):
    """standartinis django logout view, atsijungimui nuo sistemos"""
    logout(request)
    return HttpResponseRedirect('')

def nvartotojas(request):
    """naujo vartotojo kurimo view.
    is uzpildytos formos sugeneruojamas POST, is jo informacija ciklo pagalba sudedama i dicta,
    aptikus dicta, tikrinama ar tokio vartotojo sistemoje dar nera.
    Radus toki vartotoja - sistema ismeta klaida, kad toks vartotojas jau yra.
    Neradus tokio vartotojo - sistema sukuria nauja vartotoja, suhashina jo slaptazodi ir patalpina i DB prie kitu useriu"""
    if request.user.is_authenticated and request.user.is_superuser:
        new_user = {}
        for k,v in request.POST.iteritems():
            if k == 'csrfmiddlewaretoken':
                continue
            new_user[k] = v
        if new_user:
            new_username=new_user.get('username')
            if User.objects.filter(username=new_username).exists():
                ctypes.windll.user32.MessageBoxW(0, "Toks vartotojas jau yra", "Klaida", 0 + 4096)
            else:
                user=User.objects.create_user(username=new_username, password=new_user.get('password'),\
                    is_superuser=new_user.get('is_superuser'))
                user.save()
                return HttpResponseRedirect('../')
        else:
            pass
        return render(request, 'helpdesk/nvartotojas.html')
    else:
        return HttpResponseRedirect('../login/')
