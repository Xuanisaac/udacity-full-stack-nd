# nd_full_stack_linux_server_configuration
This project is part of Udacity Full Stack Nanodegree Progrom. 
>In this project, a Linux virtual machine is configured to host  web application [Item Catalog](https://github.com/Xuanisaac/nd_full_stack_item_catalogue), to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers.
## Usage 
- The application is hosted on http://52.45.152.121/
- SSH as grader using command `ssh grader@52.45.152.121 -p 2200` given you have the private key
- the password for grader is '123' which will be handy when running sudo

# Server Configuation Steps
## Step 1: Update packages and Change timezone to Eastern Time (UTC-5)

To update all currently installed packages:

```shell
sudo apt-get update
sudo apt-get upgrade
```

To configure the local timezone to UTC:

```shell
sudo dpkg-reconfigure tzdata
```
Then select `Eastern` to make the configuration changes.

## Step 2: Enable Firewall and configure network

### In Virtual Machine Shell

- Edit `/etc/ssh/sshd_config` using your favorite text editor

```shell
sudo vim /etc/ssh/sshd_config
```

- Then change Port and some new options:

```
# Package generated configuration file
# See the sshd_config(5) manpage for details

# What ports, IPs and protocols we listen for
Port 2200
DenyUsers root
AllowUsers grader

# Change value to no
PermitRootLogin no
```

- Save the file and restart SSH Server:

```shell
sudo service ssh restart
```

- Download `NTP`
```shell
sudo apt-get install ntp
```

- Finally, to enable firewall and accept only specific ports:

```shell
# Enable Firewall
sudo ufw enable

# Add Rule for port 2200
sudo ufw allow 2200/tcp

# Add Rule for port 80
sudo ufw allow 80/tcp

# Add Rule for port 123
sudo ufw allow 123/udp
```

- You may need to add firewall manually in the cloud computing platform (for example, Amazon Lightsail, Google Cloud)

## Step 2: Create a new user(grader) with sudo permission

### Create a new user named grader
1. `sudo adduser grader`
2. `vim /etc/sudoers`
3. `touch /etc/sudoers.d/grader`
4. `vim /etc/sudoers.d/grader`, type in `grader ALL=(ALL:ALL) ALL`, save and quit

### Set ssh login using keys
1. generate keys on local machine using`ssh-keygen` ; then save the private key in `~/.ssh` on local machine
2. deploy public key on developement enviroment

	On you virtual machine:
	```
	$ su - grader
	$ mkdir .ssh
	$ touch .ssh/authorized_keys
	$ vim .ssh/authorized_keys
	```
	Copy the public key generated on your local machine to this file and save
	```
	$ chmod 700 .ssh
	$ chmod 644 .ssh/authorized_keys
 	```

## Step 3: Install PostgreSQL, create database(grader) for user(grader)

```shell
# install PostgreSQL
sudo apt-get install postgresql

# login as postgres in linux terminal
su postgres

# login to postgresql shell
psql

# inside psql create database

psql> CREATE DATABASE catalog;

# create user catalog

psql> CREATE USER catalog;

# give user full permission under catalog database

psql> GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;

# Finally, set password for user catalog

psql> ALTER USER catalog PASSWORD '<Select-Your-Own-Password>';

# Quit from postgresql shell

psql> \q

```

## Step 4: Install and configure Apache to serve a Python mod_wsgi application

```shell
# install apache and prerequisites
sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

# install mod_wsgi apache module
sudo apt-get install libapache2-mod-wsgi

```

## Step 5: Install Catalog App

```shell
# First install git
sudo apt-get install git
# Change to directory /var/www/
cd /var/www/
# create folder called FlaskApp
mkdir FlaskApp && cd FlaskApp

# Download the git repository
sudo git clone https://github.com/Xuanisaac/nd_full_stack_item_catalogue

# Copy the main app directory "catalogue" out of the folder to FlaskApp
# Create a `flask.wsgi` inside `FlaskApp` directory
sudo vim /var/www/FlaskApp/flask.wsgi

# change the item_catalog.py to __init__.py
cd /var/www/FlaskApp/catalogue
mv item_catalog.py __init__.py

# change file permissions
sudo chmod 755 /var/www/FlaskApp/catalog -R
```
### Install Application Dependencies

```shell
# install pip
sudo apt-get install python-pip

# install httplib2
sudo pip install httplib2

# install oauth2client
sudo pip install oauth2client

# install flask
sudo pip install flask

# install sqlalchemy
sudo pip install sqlalchemy

# install psycopg2
sudo pip install psycopg2
```

### Modify app so that it could work with apache and postgresql

#### Modify item_database_config line 63

```
engine = create_engine('sqlite:///item_catalog.db')
```

To

```
engine = create_engine('postgresql://catalog:<Select-Your-Own-Password>@localhost/catalog')
```

Change <Select-Your-Own-Password> with your own password which you ahev set in psql for catalog user.

After that fire this script `item_database_config.py` to build tables inside catalog database

```
sudo python item_database_config.py
```

#### Modify `database_operations.py`

```
engine = create_engine('sqlite:///item_catalog.db')
```

To

```
engine = create_engine('postgresql://catalog:<Select-Your-Own-Password>@localhost/catalog')
```

#### Modify new `__init__.py`
```
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
UPLOAD_FOLDER = 'images'
```
To
```
CLIENT_ID = json.loads(open('/var/www/FlaskApp/client_secret.json', 'r').read())['web']['client_id']
UPLOAD_FOLDER = '/var/wwww/FlaskApp/images'
```

#### Write `wsgi/flask.wsgi`

Open it with your favorite editor and paste the following codes:

```sell
import os
import sys
import logging


logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from catalogue import app as application
application.secret_key = 'Add your sercret key'
```

#### Change Google and Facebook OAUTH callback 
1. Go to Google cloud console where you registered your app.
2. Go to Project API credentials and add the IP address and the server host name to the Javascript origins and redirected URIs list
3. Go to Facebook Developers dashboard where you registered your app
4. Change the domain name
5. Update the `cilent_secrets.json` and `fb_client_secrets.json` file under the directory of `/var/www/FlaskApp/catalogue`

### Configure apache2

Create a new file `FlaskApp.conf` inside `/etc/apache2/sites-available/`

```shell
<VirtualHost *:80>
        ServerName 52.45.152.121
        ServerAdmin gustuvhx94@gmail.com
        WSGIScriptAlias / /var/www/FlaskApp/flask.wsgi
        WSGIDaemonProcess myapp user=www-data group=www-data threads=1
        WSGIScriptReloading On
        <Directory /var/www/FlaskApp/FlaskApp/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/FlaskApp/catalogue/static
        <Directory /var/www/FlaskApp/catalogue/static/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /templates /var/www/FlaskApp/catalogue/templates
        Alias /uploads /var/www/FlaskApp/catalogue/images
        <Directory /var/www/FlaskApp/catalogue/templates/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /images /var/www/FlaskApp/catalogue/images
        <Directory /var/www/FlaskApp/catalogue/images/>
                Options Indexes MultiViews
                AllowOverride None
                Order allow,deny
                Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Enable Virtual Host
```
sudo a2ensite FlaskApp
```
Restart apache2

```
sudo service apache2 restart
```
# References

- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- Udacity Course: [Configuring Linux Web Servers](https://www.udacity.com/course/configuring-linux-web-servers--ud299)
- Udacity Forums: 
 - [Target WSGI script cannot be loaded. No such file](https://discussions.udacity.com/t/target-wsgi-script-cannot-be-loaded-no-such-file/44819)
- Digital Ocean Tutorials:
  - [How To Install and Use PostgreSQL on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
  - [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- Stack Overflow:
  - [Convert SQLITE SQL dump file to POSTGRESQL](http://stackoverflow.com/questions/4581727/convert-sqlite-sql-dump-file-to-postgresql)
  - [import sql dump into postgresql database](http://stackoverflow.com/questions/6842393/import-sql-dump-into-postgresql-database)
  - [Delete rows with foreign key in PostgreSQL Flask](http://stackoverflow.com/questions/28514025/delete-rows-with-foreign-key-in-postgresql-flask)
