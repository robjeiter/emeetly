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

# api keys
PAGE_ACCESS_TOKEN = ""
VERIFY_TOKEN = ""
GOOGLE_API_KEY = ""

#conversational strings
welcome_text = "Welcome to eMeetly, your most intuitive dating experience! What would you like to do next?"
sayhi = "Hi "
getstartedtext = "So, let’s get started! Whom would you like to date?"
sharelocation = "Good choice! Next please share your location to find people near you!"
question2 = "Great age! Please complete the next sentence: \n\nMy closests friends would describe me as ..."
question3 = "Great! One last sentence to complete: \n\nI am passionate about ..."
completedintro = "Good job! You just finished your profile! Below is what it looks like:"
userprofilequestion = "This is what your user profile looks like. Swipe right to see it all. Would you like to continue or change it?"
continueanswertext = "Awesome! Next we need to set up your profile pictures. You need to upload minimum one picture and can upload up to three pictures! Please send us your picture now!"
imageanswer1 = "Nice picture! Please send us another picture!"
imageanswer2 = "Wow! Lovely picture! We need one more picture!"
upcontinue = "Congratulations! You're profile is all set!" # As a last step you need to grant us some Facebook permissions and then you are ready to meet people!
citystatus1 = "Currently there are not enough people signed up in "
citystatus2 = "! We will notify you when people are joining eMeetly in "
upchangetext1 = "So let's change it! Complete this sentence: \n\nHi, my name is "
upimages = "Alright! So please send us your new pictures! Start with the first one!"
errormessage = "Ooops, looks like something went wrong! Please try to send me a text message"
fmmessage = "Please click on one of the three buttons below and I promise I can do wonders!"

#userprofile strings
upintro = "Now, help us set up your user profile by completing three sentences. Let's start with this one: "
himynameis = "Hi, my name is "
changeuserprofile = "So let's change it! Complete this sentence: "
passionateabout = "and I am passionate about ..."
iampassionateabout = "I am passionate about "
myclosestfriends = "My closests friends would describe me as "
iamcurrentlyin = "I am currently in"
andiam = "and I am"
yearsold = "years old."
yearsinnumbers = "Write your age that will appear in the gap preferably in numbers!"
matchintro = "Let us next introduce you to "

#location strings
goodjobslookslikeyourin ="Good job! Looks like you are in "

#quiz strings
quizstaytuned = "We will release the quiz feature very soon! Stay tuned!"

#button strings
mainbutton1 = "Start Dating"
mainbutton2 = "Reset your profile"
mainbutton3 = "Take the quiz"
mainbutton4 = "Learn more"
girlsbutton = "Girls"
boysbutton = "Boys"
continuebutton = "Continue"
changetextbutton = "Change the text"
changeimagesbutton = "Change the images"
interestedbutton = "I'd like to connect"
notinterestedbutton = "I am not interested"

#matches
itsamatch1 = "Awesome! "
itsamatch2 = " and you liked each other!"
itsamatchg1 = "At eMeetly we respect your privacy. That's why we put you in control. How would you like to connect with "
itsamatchg2 = "Other Application"
whatsapp = "Sure! Please enter your phone number that is linked to your WhatsApp account!"
insta = "Sure! Please provide your Snapchat user name!"
otherapp = "No problem. Please type the name of the app that you would like to connect!"
otherapp2 = "Great! Now please type your number or user name that is linked to this app so that "
otherapp3 = " can get in touch with you!"
itsamatchsend = "That's it. We will now share your "
itsamatchsend2 = " contact details "
itsamatchsend3 = " to "
imbutton1 = "Confirm"
imbutton2 = "Change"
imbutton3 = "Don't share!"
msent = "Awesome. That's it!"
msent2 = "Currently no other people are available on eMeetly in your location. We will inform you as soon as this changes."
mchange = "No problem. So let's change this! What application would you like to use?"
mcancel = "No worries. We will not share anything you won't want us to share!"
contact1 = "Great things have happened on eMeetly "
contact2 = "We would like to notify you that "
contact3 = " and you liked each other! "
contact4 = "Here's again "
contact5 = "'s profile:"
contact6 = "Now it is time for you to get in touch with "
contact7 = "You can contact "
contact8 = " on "
contact9 = "Here is her phone number: "
contact10 = "Here is her user name: "
contact11 = "Make sure you properly introduce yourself mentioning that you both matched on eMeetly!"
contact12 = "Here are her contact details: "
nointerest = "Ok!"
nomatchyet = "Ok, we will notify you in case a match occurs!"
nomoreusers = "There are currently no more active users in your city. We will notify when more people join eMeetly in "
newusers = "New users are joining eMeetly in "


#quiz
quiz0 = "Good start! We will ask you 5 questions! Please answer honestly! Let's start off:"
quiz1 = "Do you smoke?"
quiz2 = "Do you have pets at home?"
quiz3 = "Have you studied at university or are you studying right now?"
quiz4 = "Do you have tattoos?"
quiz5 = "What are you looking for at eMeetly?"
qa = "Yes"
qb = "No"
q5a = "Long term dating"
q5b = "Short term dating"
q5c = "Just meeting people"
qend = "Thank you for taking the Quiz! We will take your answers into account when suggesting new people for you!"
qf1 = "What would you like to do next?"
qf2 = "Set up my profile"
qf3 = "Learn more"
