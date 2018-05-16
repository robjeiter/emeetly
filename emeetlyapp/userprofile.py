from pprint import pprint
from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
#from emeetlyapp import views
from django.views import generic
from django.http.response import HttpResponse
import json, requests, random, re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from emeetlyapp.models import User
from emeetlyapp.messages import simple_message

#buttons
from emeetlyapp.textstrings import mainbutton1, mainbutton2, mainbutton3, mainbutton4, girlsbutton, boysbutton, continuebutton, changetextbutton, changeimagesbutton
#apis
from emeetlyapp.textstrings import PAGE_ACCESS_TOKEN, VERIFY_TOKEN, GOOGLE_API_KEY
#userprofile
from emeetlyapp.textstrings import upintro, himynameis, changeuserprofile, passionateabout, iampassionateabout, myclosestfriends, iamcurrentlyin, andiam, yearsold, yearsinnumbers, matchintro, interestedbutton, notinterestedbutton

#web view height ratio lets you control the height. Highest: Full

#show the user his own profile
def show_userpictures(fbid):
	user = User.objects.get(userid=fbid)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	introtext1 = user.intro1
	introtext2 = user.intro2
	introtext3 = user.intro3
	imageurl1 = user.imageurl1
	imageurl2 = user.imageurl2
	imageurl3 = user.imageurl3
	city = user.city
	intro1 = himynameis+user_details['first_name']+", "+iamcurrentlyin+" "+city+" "+andiam+" "+introtext1+" "+yearsold
	intro2 = myclosestfriends +introtext2
	intro3 = iampassionateabout +introtext3

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"generic", "image_aspect_ratio":"square","elements":[{"title":user_details['first_name'],
	"image_url":imageurl1,
	"subtitle":intro1,
	"buttons":[{"type":"postback",
	"title":continuebutton,"payload":"upcontinue"},{"type":"postback",
	"title":changetextbutton,"payload":"upchangetext"},{"type":"postback",
	"title":changeimagesbutton,"payload":"upimages"}]},{"title":user_details['first_name'],
	"image_url":imageurl2,
	"subtitle":intro2,
	"buttons":[{"type":"postback",
	"title":continuebutton,"payload":"upcontinue"},{"type":"postback",
	"title":changetextbutton,"payload":"upchangetext"},{"type":"postback",
	"title":changeimagesbutton,"payload":"upimages"}]},
	{"title":user_details['first_name'],
	"image_url":imageurl3,
	"subtitle":intro3,
	"buttons":[{"type":"postback",
	"title":continuebutton,"payload":"upcontinue"},{"type":"postback",
	"title":changetextbutton,"payload":"upchangetext"},{"type":"postback",
	"title":changeimagesbutton,"payload":"upimages"}]}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	pprint(status.json())
	pprint("wip")

#show the user the profile of a potential match and sent it to the user that is looking for a match
def show_pm_profile(uid, pmid):
	pprint("made it until here")
	user = User.objects.get(userid=pmid)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%pmid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	text = matchintro + user_details['first_name']+"!"
	simple_message(uid, text)
	introtext1 = user.intro1
	introtext2 = user.intro2
	introtext3 = user.intro3
	imageurl1 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image1.jpg"
	imageurl2 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image2.jpg"
	#imageurl3 = "https://storage.cloud.google.com/eimagestorage/rob1.jpg?_ga=2.9924277.-1862101233.1513003688"
	imageurl3 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image3.jpg"
	pprint(imageurl1)
	city = user.city
	intro1 = himynameis+user_details['first_name']+", "+iamcurrentlyin+" "+city+" "+andiam+" "+introtext1+" "+yearsold
	intro2 = myclosestfriends +introtext2
	intro3 = iampassionateabout +introtext3

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":uid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"generic", "image_aspect_ratio":"square","elements":[{"title":user_details['first_name'],
	"image_url":imageurl1,
	"subtitle":intro1,
	"buttons":[{"type":"postback",
	"title":interestedbutton,"payload":"interested"},{"type":"postback",
	"title":notinterestedbutton,"payload":"notinterested"}]},{"title":user_details['first_name'],
	"image_url":imageurl2,
	"subtitle":intro2,
	"buttons":[{"type":"postback",
	"title":interestedbutton,"payload":"interested"},{"type":"postback",
	"title":notinterestedbutton,"payload":"notinterested"}]},
	{"title":user_details['first_name'],
	"image_url":imageurl3,
	"subtitle":intro3,
	"buttons":[{"type":"postback",
	"title":interestedbutton,"payload":"interested"},{"type":"postback",
	"title":notinterestedbutton,"payload":"notinterested"}]}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	pprint(status.json())
	pprint("wip")

def recall_profile(uid, pmid):
	pprint("made it until here")
	user = User.objects.get(userid=pmid)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%pmid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	introtext1 = user.intro1
	introtext2 = user.intro2
	introtext3 = user.intro3
	imageurl1 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image1.jpg"
	imageurl2 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image2.jpg"
	imageurl3 = "https://s3.amazonaws.com/eimagestorage/"+pmid+"image3.jpg"
	pprint(imageurl1)
	city = user.city
	intro1 = himynameis+user_details['first_name']+", "+iamcurrentlyin+" "+city+" "+andiam+" "+introtext1+" "+yearsold
	intro2 = myclosestfriends +introtext2
	intro3 = iampassionateabout +introtext3

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":uid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"generic", "image_aspect_ratio":"square","elements":[{"title":user_details['first_name'],
	"image_url":imageurl1,
	"subtitle":intro1,},{"title":user_details['first_name'],
	"image_url":imageurl2,
	"subtitle":intro2,},
	{"title":user_details['first_name'],
	"image_url":imageurl3,
	"subtitle":intro3,}]}}}, "tag":"PAIRING_UPDATE"})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	pprint(status.json())
	pprint("wip")
