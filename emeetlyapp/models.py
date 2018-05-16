from django.db import models

class User(models.Model):
	userid = models.CharField(max_length=26,unique=True)
	firstname = models.CharField(max_length=26, null=True, blank=True)
	longi = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
	lat = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
	gender = models.CharField(max_length=10, null=True, blank=True)
	info1 = models.CharField(max_length=50, null=True, blank=True)
	info2 = models.CharField(max_length=50, null=True, blank=True)
	info3 = models.CharField(max_length=50, null=True, blank=True)
	quiz1 = models.CharField(max_length=15, null=True, blank=True)
	quiz2 = models.CharField(max_length=15, null=True, blank=True)
	quiz3 = models.CharField(max_length=15, null=True, blank=True)
	quiz4 = models.CharField(max_length=15, null=True, blank=True)
	quiz5 = models.CharField(max_length=15, null=True, blank=True)
	quizstatus = models.CharField(max_length=10, null=True, blank=True)
	age = models.IntegerField(null=True, blank=True)
	lookingfor = models.CharField(max_length=6, null=True, blank=True)
	activeprofile = models.CharField(max_length=4, null=True, blank=True)
	messagestatus = models.CharField(max_length=8, default='999')
	intro1 = models.CharField(max_length=140, null=True, blank=True)
	intro2 = models.CharField(max_length=140, null=True, blank=True)
	intro3 = models.CharField(max_length=140, null=True, blank=True)
	#matches = models.ManyToManyField('self')
	#notmatches = models.ManyToManyField('self')
	locations = models.ManyToManyField('self')
	imageurl1 = models.URLField(null=True, blank=True)
	imageurl2 = models.URLField(null=True, blank=True)
	imageurl3 = models.URLField(null=True, blank=True)
	city = models.CharField(max_length=20, null=True, blank=True)
	region = models.CharField(max_length=20, null=True, blank=True)
	introstatus = models.CharField(max_length=15, null=True, blank=True)
	picturestatus = models.CharField(max_length=15, null=True, blank=True)
	lastshownpmid = models.CharField(max_length=26, null=True, blank=True)
	whatsappnr = models.CharField(max_length=26, null=True, blank=True)
	instauser = models.CharField(max_length=26, null=True, blank=True)
	otherappname = models.CharField(max_length=26, null=True, blank=True)
	otherappdetails = models.CharField(max_length=26, null=True, blank=True)
	preferredapp = models.CharField(max_length=26, null=True, blank=True)
	matchtrigger = models.CharField(max_length=26, null=True, blank=True)
	lastmatchid = models.CharField(max_length=26, null=True, blank=True)

	def __str__(self):
		return self.userid

class PotentialMatches(models.Model):
		pmid = models.CharField(max_length=26, null=True, blank=True)
		userisinterestedinpm = models.CharField(max_length=15, default='notshown')
		user = models.ForeignKey('User',related_name='pms')

	#def __str__(self):
		#return self.pmid
