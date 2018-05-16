from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views import generic
from django.http.response import HttpResponse
import json, requests, random, re
from pprint import pprint
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from emeetlyapp.models import User, PotentialMatches
from emeetlyapp.userprofile import show_pm_profile, recall_profile
from emeetlyapp.messages import simple_message
from emeetlyapp.messages import two_button_message
from emeetlyapp.messages import three_button_message
from emeetlyapp.messages import start_message
from django.db import connection

#import textstrings
#quiz
from emeetlyapp.textstrings import quiz0, quiz1, quiz2, quiz3, quiz4, quiz5, qa, qb, q5a, q5b, q5c, qend, qf1, qf2, qf3

def question1(fbid):
    simple_message(fbid, quiz0)
    p1 = "smoker"
    p2 = "nonsmoker"
    two_button_message(fbid, quiz1, qa, p1, qb, p2)

def question2(fbid):
    p1 = "petsyes"
    p2 = "petsno"
    two_button_message(fbid, quiz2, qa, p1, qb, p2)

def question3(fbid):
    p1 = "uni"
    p2 = "nouni"
    two_button_message(fbid, quiz3, qa, p1, qb, p2)

def question4(fbid):
    p1 = "tattoos"
    p2 = "notattoos"
    two_button_message(fbid, quiz4, qa, p1, qb, p2)

def question5(fbid):
    p1 = "long"
    p2 = "short"
    p3 = "fun"
    three_button_message(fbid, quiz5, q5a, p1, q5b, p2, q5c, p3)

#hnadle all quiz ansers and save accordingly
def process_quiz_payload(fbid, payload):
    user = User.objects.get(userid=fbid)
    if payload == "smoker" or payload == "nonsmoker":
        question2(fbid)
        user.quiz1 = payload
        user.save()
    elif payload == "petsyes" or payload == "petsno":
        question3(fbid)
        user.quiz2 = payload
        user.save()
    elif payload == "uni" or payload == "nouni":
        question4(fbid)
        user.quiz3 = payload
        user.save()
    elif payload == "tattoos" or payload == "notattoos":
        question5(fbid)
        user.quiz4 = payload
        user.save()
    elif payload == "long" or payload == "short" or payload == "fun":
        user.quiz5 = payload
        user.quizstatus = "completed"
        user.save()
        text = qend
        simple_message(fbid, text)
        start_message(fbid, qf1, qf2, qf3)
