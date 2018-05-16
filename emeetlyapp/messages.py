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

#api key
from emeetlyapp.textstrings import PAGE_ACCESS_TOKEN, VERIFY_TOKEN, GOOGLE_API_KEY

def simple_message(fbid, answer_text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":answer_text}, "tag":"PAIRING_UPDATE"})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def two_button_message(fbid, answer_text, button1, payload1, button2, payload2):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback",
	"title":button1,"payload":payload1},{"type":"postback","title":button2,"payload":payload2}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def three_button_message(fbid, answer_text, button1, payload1, button2, payload2, button3, payload3):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback",
	"title":button1,"payload":payload1},{"type":"postback","title":button2,"payload":payload2},
	{"type":"postback","title":button3,"payload":payload3}]}}}, "tag":"PAIRING_UPDATE"})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def start_message(fbid, text, b1, b2):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":text,"buttons":[{"type":"postback","title":b1,"payload":"dating"},{"type":"web_url","url":"www.emeetly.com","title":b2}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
