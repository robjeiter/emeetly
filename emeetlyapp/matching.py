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
from emeetlyapp.messages import three_button_message
from django.db import connection

#import textstrings
#conversational
from emeetlyapp.textstrings import welcome_text, sayhi, question2, question3, completedintro, userprofilequestion, continueanswertext, imageanswer1, imageanswer2, upcontinue, citystatus1, citystatus2, upchangetext1, upimages, errormessage, getstartedtext,sharelocation
#matches
from emeetlyapp.textstrings import itsamatch1, itsamatch2, itsamatchg1, itsamatchg2, whatsapp, insta, otherapp, otherapp2, otherapp3, itsamatchsend, itsamatchsend2, itsamatchsend3, imbutton1, imbutton2, imbutton3, msent, msent2, mchange, mcancel, contact1, contact2, contact3, contact4, contact5, contact6, contact7, contact8, contact9, contact10, contact11, contact12, nointerest, nomatchyet, nomoreusers, newusers

#define the profile of the user that is looking for a match
def matching(fbid):
    user = User.objects.get(userid=fbid)
    uid = fbid
    ucity = user.region
    ugender = user.gender
    lookingfor = user.lookingfor
    if lookingfor == "girls":
        ulookingfor = "female"
    elif lookingfor == "boys":
        ulookingfor = "male"
    pprint(ulookingfor)
    matchingquery2(uid, ucity, ugender, ulookingfor)



def matchingquery2(uid, ucity, ugender, ulookingfor):
    for person in User.objects.filter(region=ucity,gender=ulookingfor,picturestatus="completed"):
        pmid = person.userid
        interest = PotentialMatches.objects.filter(pmid=pmid, user__userid=uid)
        if not interest:
            show_pm_profile(uid, pmid)
            user = User.objects.get(userid=uid)
            user.lastshownpmid = pmid
            user.save()
            pprint("we have somebody to show here")
            break
    else:
        statustext = nomoreusers+ucity+"!"
        simple_message(uid, statustext)
        pprint("nothin to show")


#check if a match occured
def checkifmatch(fbid, interest):
    u = User.objects.get(userid=fbid)
    pid = u.lastshownpmid
    #save that the user liked the pm
    p = PotentialMatches.objects.update_or_create(pmid=pid, user=u, defaults = {'userisinterestedinpm': interest})
    #p.save()
    #now check if there is a match; if pm likes user as well
    #1.) check if the user that has the id of the potential match has exists & check whether he already has seen the other user (potential match)
    #pm = User.objects.get(userid=pid)
    #this needs to be done that when it is empty it wont cause trouble
    #pm = PotentialMatches.objects.filter(pmid=fbid, user__userid=pid)
    #pprint(str(pm))
    pprint("checkifmatch executed")
    #2.) check whether the user has shown interest in the other user
    #i = pm.userisinterestedinpm
    #i = "fun"
    try:
        i = PotentialMatches.objects.filter(pmid=fbid, user__userid=pid).get().userisinterestedinpm
        if i == "yes":
            matched(fbid, pid)
            pprint("matched yes")
            #this is the match case
        elif i == "no":
            #this is the case that no match occured. the other user has already seen, but didnt like
            no_match_yet(fbid, pid)
            pprint("no match, next")
    except PotentialMatches.DoesNotExist:
        i = None
        if not i:
            no_match_yet(fbid, pid)
            notify_newuser(pid, fbid)
            #this is the case when the other user did not yet see that user
            #here you need to do something. you need to notify the other user to take a look
            pprint("not yet seen")
        else:
            pprint("oops. something went wrong")

#case profile is shown to user but user is not interested.
def record_no_interest(fbid, interest):
        u = User.objects.get(userid=fbid)
        pid = u.lastshownpmid
        #save that the user dit not like the pm
        p = PotentialMatches.objects.update_or_create(pmid=pid, user=u, defaults = {'userisinterestedinpm': interest})
        text = nointerest
        simple_message(fbid, text)
        matching(fbid)

#this is the scenario where we fun no match quite yet. one user has liked the user, but the other user did not (yet) like postback
def no_match_yet(fbid, pid):
    text = nomatchyet
    simple_message(fbid, text)
    matching(fbid)

#a match happened. WoW! Magic! now check if the user is a woman or a man and proceed with match
def matched(userid, matchid):
    m = User.objects.get(userid=matchid)
    matchname = m.firstname
    u = User.objects.get(userid=userid)
    username = u.firstname
    gender = u.gender
    if gender == "female":
        text = itsamatch1+str(matchname)+itsamatch2
        simple_message(userid, text)
        gtext = itsamatchg1+str(matchname)+"?"
        b1 = "WhatsApp"
        p1 = "whatsapp"
        b2 = "Snapchat"
        p2 = "instagram"
        b3 = itsamatchg2
        p3 = "otherapp"
        three_button_message(userid, gtext, b1, p1, b2, p2, b3, p3)
        u.matchtrigger = "female"
        u.save()
    elif gender == "male":
        g = User.objects.get(userid=matchid)
        text = nomatchyet
        simple_message(userid, text)
        matching(userid)
        male_triggered_match(userid, matchid)
        #now send a message to the girl that there was a match (show again the profile of the guy she matched)

def receive_payload(userid, payload):
    u = User.objects.get(userid=userid)
    #part 1
    if payload == "whatsapp":
        text = whatsapp
        u.messagestatus = "MW"
        u.preferredapp = "whatsapp"
        u.save()
        #update user.messagestatus to Mwhatsapp
        simple_message(userid, text)
    elif payload == "instagram":
        text = insta
        u.messagestatus = "MI"
        u.preferredapp = "insta"
        u.save()
        simple_message(userid, text)
    elif payload == "otherapp":
        text = otherapp
        u.messagestatus = "MO"
        u.preferredapp = "other"
        u.save()
        simple_message(userid, text)
    #part2
    elif payload == "msend":
        text = msent
        simple_message(userid, text)
        app = u.preferredapp
        mid = u.lastshownpmid
        share_contact(userid, mid, app)
        #check if more users are available and act accordingly
    elif payload == "mchange":
        text = mchange
        b1 = "WhatsApp"
        p1 = "whatsapp"
        b2 = "Snapchat"
        p2 = "instagram"
        b3 = itsamatchg2
        p3 = "otherapp"
        three_button_message(userid, text, b1, p1, b2, p2, b3, p3)
    elif payload == "mcancel":
        text = mcancel
        simple_message(userid, text)

def process_status(fbid, incoming_message):
    u = User.objects.get(userid=fbid)
    status = u.messagestatus
    trigger = u.matchtrigger
    if trigger == "female":
        boy = u.lastshownpmid
    elif trigger == "male":
        boy = u.lastmatchid
    b = User.objects.get(userid=boy)
    boyname = b.firstname
    b1 = imbutton1
    b2 = imbutton2
    b3 = imbutton3
    p1 = "msend"
    p2 = "mchange"
    p3 = "mcancel"
    if status == "MW":
        u.whatsappnr = incoming_message
        u.messagestatus = "1a"
        u.save()
        text = itsamatchsend +"WhatsApp" + itsamatchsend2 + "(" + incoming_message + ")" + itsamatchsend3 + str(boyname)
        three_button_message(fbid, text, b1, p1, b2, p2, b3, p3)
    elif status == "MI":
        u.instauser = incoming_message
        u.messagestatus = "1a"
        u.save()
        text = itsamatchsend +"Snapchat" + itsamatchsend2 + "(" + incoming_message + ")" + itsamatchsend3 + str(boyname)
        three_button_message(fbid, text, b1, p1, b2, p2, b3, p3)
    elif status == "MO":
        u.otherappname = incoming_message
        u.messagestatus = "MO2"
        u.save()
        text = otherapp2 + str(boyname) + otherapp3
        simple_message(fbid, text)
    elif status == "MO2":
        appname = u.otherappname
        u.otherappdetails = incoming_message
        u.messagestatus = "1a"
        u.save()
        text = itsamatchsend + appname + itsamatchsend2 + "(" + incoming_message + ")" + itsamatchsend3 + str(boyname)
        three_button_message(fbid, text, b1, p1, b2, p2, b3, p3)


def share_contact(uid, mid, app):
    u = User.objects.get(userid=uid)
    m = User.objects.get(userid=mid)
    uname = u.firstname
    mname = m.firstname
    text = contact1 + mname + "! " + contact2 + uname + contact3 + contact4 + uname + " " + contact5
    simple_message(mid, text)
    recall_profile(mid, uid)
    if app == "whatsapp":
        phone = u.whatsappnr
        text2 = contact6 + uname + "! " + contact7 + uname + contact8 + "WhatsApp! " + contact9 + phone + "! " + contact11
        simple_message(mid, text2)
    elif app == "insta":
        instagram = u.instauser
        text2 = contact6 + uname + "! " + contact7 + uname + contact8 + "Snapchat! " + contact10 + instagram + "! " + contact11
        simple_message(mid, text2)
    elif app == "other":
        appname = u.otherappname
        appdetails = u.otherappdetails
        text2 = contact6 + uname + "! " + contact7 + uname + contact8 + appname + "! " + contact12 + appdetails + "! " + contact11
        simple_message(mid, text2)

def male_triggered_match(uid, mid):
    pprint("mtrigger function")
    u = User.objects.get(userid=uid)
    #u is man
    m = User.objects.get(userid=mid)
    #m is woman
    m.matchtrigger = "male"
    m.lastmatchid = uid
    m.save()
    uname = u.firstname
    mname = m.firstname
    text = contact1 + mname + "! " + contact2 + uname + contact3 + contact4 + uname + " " + contact5
    simple_message(mid, text)
    recall_profile(mid, uid)
    gtext = itsamatchg1+uname+"?"
    b1 = "WhatsApp"
    p1 = "whatsapp"
    b2 = "Snapchat"
    p2 = "instagram"
    b3 = itsamatchg2
    p3 = "otherapp"
    three_button_message(mid, gtext, b1, p1, b2, p2, b3, p3)

def notify_newuser(usr, notyetshownuser):
    u = User.objects.get(userid=usr)
    city = u.city
    text = newusers + city + "!"
    simple_message(usr, text)
    show_pm_profile(usr, notyetshownuser)
    u.lastshownpmid = notyetshownuser
    u.save()
    pprint("hello from notify_newuser")
