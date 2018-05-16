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
from emeetlyapp.models import User
from emeetlyapp.models import PotentialMatches
from emeetlyapp.s3images import upload_s3
from emeetlyapp.userprofile import show_userpictures
from emeetlyapp.matching import matching, checkifmatch, receive_payload, process_status, record_no_interest
from emeetlyapp.quiz import process_quiz_payload, question1
from emeetlyapp.location import coordinates_to_city

#import textstrings
#conversational
from emeetlyapp.textstrings import welcome_text, sayhi, question2, question3, completedintro, userprofilequestion, continueanswertext, imageanswer1, imageanswer2, upcontinue, citystatus1, citystatus2, upchangetext1, upimages, errormessage, getstartedtext,sharelocation, fmmessage
#api key
from emeetlyapp.textstrings import PAGE_ACCESS_TOKEN, VERIFY_TOKEN, GOOGLE_API_KEY
#buttons
from emeetlyapp.textstrings import mainbutton1, mainbutton2, mainbutton3, mainbutton4, girlsbutton, boysbutton, continuebutton, changetextbutton, changeimagesbutton
#userprofile
from emeetlyapp.textstrings import upintro, himynameis, changeuserprofile, passionateabout, iampassionateabout, myclosestfriends, iamcurrentlyin, andiam, yearsold, yearsinnumbers
#quiz
from emeetlyapp.textstrings import quizstaytuned
#location
from emeetlyapp.textstrings import goodjobslookslikeyourin


# Helper function
def post_facebook_message(fbid, received_message):
    # Remove all punctuations, lower case the text and split it based on space
	user_message = re.sub(r"[^a-zA-Z0-9\s]",' ',received_message).lower().split()
	incoming_message = received_message
	answer_text = ''

	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic,locale', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()

	if isinstance(incoming_message, str):
		user = User.objects.get(userid=fbid)
		status = user.messagestatus
		if status == "1":
			user.intro1 = incoming_message
			user.messagestatus = "2"
			user.save()
			answer_text = question2
			send_message(fbid, answer_text)
		elif status == "2":
			user.intro2 = incoming_message
			user.messagestatus = "3"
			user.save()
			answer_text = question3
			send_message(fbid, answer_text)
		elif status == "3":
			picturestatus = user.picturestatus
			user.intro3 = incoming_message
			if picturestatus == "completed":
				user.messagestatus = "8"
				user.picturestatus = "completed"
				user.save()
				answer_text = userprofilequestion
				send_message(fbid, answer_text)
				show_userpictures(fbid)
			else:
				answer_text = continueanswertext
				user.messagestatus = "5"
				user.introstatus = "completed"
				user.save()
				send_message(fbid, answer_text)
			#send_message(fbid, completedintro)
			#show_profile(fbid)
		elif status == "4" or status == "5" or status == "6" or status == "7":
			answer_text ="4, 5, 6 or 7"
		elif status == "1a":
			answer_text = sayhi+user_details['first_name']+'! '+ welcome_text
			button1 = mainbutton1
			button2 = mainbutton2
			button3 = mainbutton3
			payload1 = "1astartdating"
			payload2 = "1aupdateprofile"
			payload3 = "quiz"
			threeb_structured_message(fbid, answer_text, button1, payload1, button2, payload2, button3, payload3)
		elif status == "MW" or status == "MI" or status == "MO" or status == "MO2":
			process_status(fbid, incoming_message)
		elif status == "FM":
			answer_text = fmmessage
			send_structured_message(fbid, answer_text)
		else:
			pprint(user_details['locale'])
			answer_text = sayhi +user_details['first_name']+'! ' + welcome_text
			user.messagestatus = "FM"
			user.save()
			send_structured_message(fbid, answer_text)
	else:
		answer_text = errormessage
		send_message(fbid, answer_text)

#def handle_text(fbid, text):

def handle_payload(fbid, payload):
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic,gender', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	user = User.objects.get(userid=fbid)
	if payload == "quiz":
		question1(fbid)
	elif payload == "getstarted":
		answer_text = sayhi +user_details['first_name']+'! ' + welcome_text
		send_structured_message(fbid, answer_text)
	elif payload =="dating" or payload == "1aupdateprofile":
		answer_text = getstartedtext
		ask_lookingfor(fbid, answer_text)
		u = User.objects.update_or_create(userid=fbid, defaults = {'messagestatus': '0'})
	elif payload == "girls" or payload == "boys":
		answer_text = sharelocation
		request_location(fbid, answer_text)
		user.lookingfor = str(payload)
		user.gender = user_details['gender']
		user.firstname = user_details['first_name']
		user.save()
	elif payload == "changeprofile":
		status = user.messagestatus
		answer_text = changeuserprofile+"\n\n"+himynameis+user_details['first_name']+" "+andiam+" ... "+yearsold+" "+yearsinnumbers
		user.messagestatus = "1"
		user.save()
		send_message(fbid, answer_text)
	elif payload == "continue":
		answer_text = continueanswertext
		send_message(fbid, answer_text)
		#show_userpictures(fbid)
		status = user.messagestatus
		user.messagestatus = "5"
		user.save()
		#upload_s3()
	elif payload == "upcontinue":
		answer_text = upcontinue
		send_message(fbid, answer_text)
		user.messagestatus = "1a"
		user.save()
		city = user.city
		statustext = citystatus1+city+citystatus2+city+"!"
		#send_message(fbid, statustext)
		matching(fbid)
		#answer_text = upcontinue
		#title = "Log into Facebook"
		#onebutton_structured_message(fbid, answer_text, title)
		#user.messagestatus = "10"
		#user.save()
	elif payload == "upchangetext":
		answer_text = upchangetext1+user_details['first_name']+" "+andiam+" ... "+yearsold+" "+yearsinnumbers
		user.messagestatus = "1"
		user.save()
		send_message(fbid, answer_text)
	elif payload == "upimages":
		answer_text = upimages
		send_message(fbid, answer_text)
		user.messagestatus = "5"
		user.save()
	elif payload == "1astartdating":
		matching(fbid)
	#after a pm is shwon to a user
	elif payload == "interested":
		interest = "yes"
		checkifmatch(fbid, interest)
		pprint("ok the user is intersted")
	elif payload == "notinterested":
		interest = "no"
		record_no_interest(fbid, interest)
		pprint("ok user is not intersted")
	elif payload == "whatsapp" or payload == "instagram" or payload == "otherapp" or payload == "msend" or payload == "mcancel" or payload == "mchange":
		receive_payload(fbid, payload)
	elif payload == "smoker" or payload == "nonsmoker" or payload == "petsyes" or payload == "petsno" or payload == "uni" or payload == "nouni" or payload == "tattoos" or payload == "notattoos" or payload == "long" or payload == "short" or payload == "fun":
		process_quiz_payload(fbid, payload)




def location_handler(fbid, lat, longi):
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	googleapiurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}".format(lat, longi, GOOGLE_API_KEY)
	location = requests.get(googleapiurl).json()
	city = location['results'][0]['address_components'][2]['long_name']
	#answer_text = "Oh, you are currently in "+city+"! eMeetly is not yet available in "+city+". We will notify you when we are arriving there!"
	answer_text = goodjobslookslikeyourin+city+"! "+upintro+"\n\n"+himynameis+user_details['first_name']+" "+andiam+" ... "+yearsold+" "+yearsinnumbers
	user = User.objects.get(userid=fbid)
	user.messagestatus = "1"
	user.lat = lat
	user.longi = longi
	user.save()
	send_message(fbid, answer_text)
	coordinates_to_city(fbid, location)

def image_handler(fbid, url):
	user = User.objects.get(userid=fbid)
	status = user.messagestatus
	if status == "5":
		user.imageurl1 = url
		user.messagestatus = "6"
		user.save()
		answer_text = imageanswer1
		send_message(fbid, answer_text)
		imagenr = "image1"
		upload_s3(url, fbid, imagenr)
	elif status == "6":
		user.imageurl2 = url
		user.messagestatus = "7"
		user.save()
		answer_text = imageanswer2
		send_message(fbid, answer_text)
		imagenr = "image2"
		upload_s3(url, fbid, imagenr)
	elif status == "7":
		user.imageurl3 = url
		user.messagestatus = "8"
		user.picturestatus = "completed"
		user.save()
		answer_text = userprofilequestion
		send_message(fbid, answer_text)
		imagenr = "image3"
		upload_s3(url, fbid, imagenr)
		show_userpictures(fbid)


def send_message(fbid, answer_text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":answer_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)



def send_structured_message(fbid, answer_text):
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback","title":mainbutton1,"payload":"dating"},{"type":"postback","title":mainbutton3,"payload":"quiz"},{"type":"web_url","url":"www.emeetly.com","title":mainbutton4}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def onebutton_structured_message(fbid, answer_text, title):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"web_url","url":"https://a4bcac73.ngrok.io/login","title":title}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def binary_structured_message(fbid, answer_text, button1, payload1, button2, payload2):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback","title":button1,"payload":payload1},{"type":"postback","title":button2,"payload":payload2}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


def threeb_structured_message(fbid, answer_text, button1, payload1, button2, payload2, button3, payload3):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback",
	"title":button1,"payload":payload1},{"type":"postback","title":button2,"payload":payload2},
	{"type":"postback","title":button3,"payload":payload3}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


def ask_lookingfor(fbid, answer_text):
	user_details_url = "https://graph.facebook.com/v2.6%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'acces_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template",
	"payload":{"template_type":"button","text":answer_text,"buttons":[{"type":"postback",
	"title":boysbutton,"payload":"boys"},{"type":"postback","title":girlsbutton,"payload":"girls"}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


def request_location(fbid, answer_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text": answer_text,"quick_replies":[{"content_type":"location"}]}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)



class fbotview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # RE: Handle the user input such as messages or payloads such as strings and location
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        entry = incoming_message['entry']
        message = entry[0]
        message1 = message['messaging']
        message2 = message1[0]
        fbid = message2['sender']['id']
        #case if payload of structured message
        pprint(incoming_message)
        if 'postback' in message2:
            payload = message2['postback']['payload']
            #pprint(payload)
            handle_payload(fbid, payload)
        elif 'message' in message2:
       	    handler = message2['message']
       	    pprint(handler)
       	    if 'text' in handler:
                text = message2['message']['text']
                u = User.objects.update_or_create(userid=fbid)
                #pprint(text, fbid)
                post_facebook_message(fbid, text)
            elif 'attachments' in handler:
                fetcher1 = handler['attachments']
                fetcher2 = fetcher1[0]
                if fetcher2['type'] == "location":
                    lat = fetcher2['payload']['coordinates']['lat']
                    longi = fetcher2['payload']['coordinates']['long']
                    location_handler(fbid, lat, longi)
                elif fetcher2['type'] == "image":
                	imageurl = fetcher2['payload']['url']
                	image_handler(fbid, imageurl)
                	#pprint(imageurl)

        return HttpResponse()
