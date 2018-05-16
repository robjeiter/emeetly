from django.contrib import admin
from django.conf.urls import include, url
from emeetlyapp import views
from .views import fbotview
from emeetlyapp import landingpage
from .landingpage import show_landingpage
from .landingpage import privacy
from .landingpage import login



urlpatterns = [
	url(r'imsommerdesjahres1999jadawareschonsehrschoen/?$', fbotview.as_view()),
	url(r'^$', landingpage.show_landingpage, name='eMeetly'),
	url(r'^privacy/', landingpage.privacy, name='privacy'),
	url(r'^login/', landingpage.login, name='login'),
]
