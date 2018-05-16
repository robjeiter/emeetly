import boto
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','emeetlyproject.settings')
from boto.s3.key import Key
import urllib.request
import django
from pprint import pprint
from django.shortcuts import render
# Import settings
django.setup()


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
END_POINT = 'us-east-1'                          # eg. us-east-1
S3_HOST = 's3.us-east-1.amazonaws.com'                            # eg. s3.us-east-1.amazonaws.com
BUCKET_NAME = 'eimagestorage'


def upload_s3(url, fbid, imagenr):
	pprint("uploading to s3")
	#store image in static folder
	urllib.request.urlretrieve(url, "static/img/" + fbid + imagenr + ".jpg")
	#file loaction
	fname = "static/img/" + fbid + imagenr + ".jpg"
	#concatenate the filename
	uploaded_fname = fbid + imagenr + ".jpg"
	s3 = boto.s3.connect_to_region(END_POINT,
    	                       aws_access_key_id=AWS_ACCESS_KEY_ID,
        	                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            	               host=S3_HOST)

	bucket = s3.get_bucket(BUCKET_NAME)
	k = Key(bucket)
	k.key = uploaded_fname
	k.set_contents_from_filename(fname)
	#delete the image after the process is done
	os.remove(fname)
