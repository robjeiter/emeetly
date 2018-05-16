from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from emeetlyapp import views
from django.views import generic
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import requests


def show_landingpage(request):
	return render(request, 'index.html')


def privacy(request):
	return render(request, 'privacy.html')

@xframe_options_exempt
def login(request):
	#return HttpResponse("This page is safe to load in a frame on any site.")
	return render(request, 'login.html')
