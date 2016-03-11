Provisioning a new site
=======================

## Required packages

* nginx
* Python 3
* Git
* pip
* virtualenv
* psycopg2
* postgresql

eg, on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip python3-dev libq-dev postgresql postgresql-contrib
	sudo pip3 install virtualenv psycopg2

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
	sites
		SITENAME	
			database
			source
			static
			virtualenv	
