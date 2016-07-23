#!/bin/bash 
apt-get -qqy update 
apt-get -qqy install postgresql python-psycopg2
apt-get -y install libq-dev 
apt-get -y install python-dev
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip

 

