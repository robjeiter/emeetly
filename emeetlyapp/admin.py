from django.contrib import admin
from emeetlyapp.models import User, PotentialMatches
#, longi, lat, gender, info1, info2, info3, quiz1, quiz2, quiz3, quiz4, quiz5, quizstatus, age, lookingfor, activeprofile, messagestatus, intro1, intro2, intro3, matches, locations, imageurl1, imageurl2, imageurl3
# Register your models here.
admin.site.register(User)
admin.site.register(PotentialMatches)

