django_mysite
=============

This is the site I use to test deploy django project on AWS.

Guidance of push code to AWS:

	1. git add .
	2. git commit -m "comments"
	3. git aws.push
	4. eb status --verbose


Guidance of push static files to S3:

	1. manage.py collectstatic

