# Project Overview

This project is part of Udacity Full Stack Development Nanodegree 

This module creates a website and JSON API for a list of items grouped into a category. Users can edit or delete items they've creating. Adding items, deleteing items and editing items requiring logging in with Google and Facebook.

## Project Details

### Set up a Google Plus auth application.
1. go to https://console.developers.google.com/project and login with Google.
2. Create a new project
3. Name the project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. On the consent screen, type in a product name and save.
7. In Authorized javascript origins add:
```
http://0.0.0.0:8080
```
```
http://localhost:8080 
```
8. Click create client ID
9. Click download JSON and save it into the root director of this project. 
10. Rename the JSON file "client_secret.json"
11. In `main.html` and `login.html` replace the line "data-clientid="[something]" so that it uses your Client ID from the web applciation. 

### Set up Facebook auth application
1. Go to https://developers.facebook.com/ to register your app
2. Go to your app on the Facebook Developers Page.
3. Then click Settings in the left column.
4. Click Advanced
5. Scroll down to the Client OAuth Settings section
6. Add redirect URI (for example http://localhost:5000/) to the Valid OAuth redirect URIs section
7. In the file `fb_client_secrets.json` under the directory /vagrant/catalogue, replace the app_id and app_secret with your app configurations.

### Setup the Database & Start the Server
1. In the project ./vagrant folder, use the command vagrant up
2. The vagrant machine will install.
3. Once it's complete, type `vagrant ssh` to login to the VM.
4. Type `cd /vagrant/catalogue` 
5. type "pyhon install_db.py" this will create the database with the categories defined in that script.
6. type "python item_catalog.py" to start the server.

### Open in a webpage
Now you can open in a webpage by going to either:
```
http://0.0.0.0:8080
```
```
http://localhost:8080 
```
