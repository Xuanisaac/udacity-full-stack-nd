import json
import httplib2
import requests
import string
import random
import os
from flask import Flask, url_for, redirect, request, render_template, flash
from flask import session as login_session
from flask import jsonify, make_response, send_from_directory
from item_database_config import Item
from database_operations import DatabaseOperations
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from werkzeug import secure_filename

# Stubs from https://github.com/udacity/ud330/blob/master/Lesson4/step2/project.py
app = Flask(__name__)

db = DatabaseOperations()
credentials = {}
token_info = {}

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Main Page
@app.route('/')
@app.route('/catalog/')
def showCategories():
    createLoginSession()
    categories = db.getListOfCategories()
    latestItems = db.getLatestItems()
    return render_template('category_list.html',
                           categories=categories,
                           items=latestItems,
                           user_id=login_session.get('user_id'),
                           STATE=login_session.get('state'))


@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    # if user already sign in redirect to home
    if 'user_id' in login_session:
        redirect('/')
    createLoginSession()
    # generate random state to protect system from anti-forgery state token
    return render_template("login.html", STATE=login_session.get('state'))


@app.route('/catalog/<int:category_id>/')
def showItemsForCategory(category_id):
    createLoginSession()
    categories = db.getListOfCategories()
    category = db.getCategoryBy(category_id)
    items = db.getItemsFor(category_id)
    return render_template('category.html',
                           main_category=category,
                           categories=categories,
                           items=items,
                           user_id=login_session.get('user_id'),
                           STATE=login_session.get('state'))


@app.route('/catalog/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    createLoginSession()
    categories = db.getListOfCategories()
    item = db.getItemBy(item_id)
    print uploaded_file(item[0].image_url)
    return render_template('item.html',
                           categories=categories,
                           item=item,
                           main_category=category_id,
                           user_id=login_session.get('user_id'),
                           STATE=login_session.get('state'))


# Send uploadedfiles.
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# CRUD Operations
@app.route('/catalog/<int:category_id>/addItem', methods=['GET', 'POST'])
def addItemToCategory(category_id):
    if 'username' not in login_session:
        return redirect(url_for('showCategories'))

    else:
        category = db.getCategoryBy(category_id)
        if request.method == 'POST':
            if checkIfClientAuthorizedWith(request.form['state']) is False:
                return responseWith('Invalid authorization paramaters.', 401)
            print 'Trying to upload file.'
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print 'Trying to save file'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print 'File upload complete'
                new_item = Item(name=request.form['name'],
                                image_url=filename,
                                description=request.form['description'],
                                category_id=category.id,
                                creator_id=login_session['user_id'])
                db.addToDatabase(new_item)
                return redirect(url_for('showItemsForCategory', category_id=category.id))
            else:
                return responseWith('Bad image.', 422)
        else:
            return render_template('addItem.html',
                                   category=category,
                                   STATE=login_session.get('state'))


@app.route('/category/<int:category_id>/editItem/<int:item_id>/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showCategories'))

    item_to_edit = db.getItemBy(item_id)

    if request.method == 'POST':
        if checkIfClientAuthorizedWith(request.form['state']) is False:
            return responseWith('Invalid authorization paramaters.', 401)

        if request.form['name']:
            item_to_edit[0].name = request.form['name']

        if request.form['description']:
            item_to_edit[0].description = request.form['description']
        print 'Checking to see if we have a new file.'
        if request.files['file']:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item_to_edit[0].image_url = filename
            else:
                return responseWith('Bad Image', 422)

        db.addToDatabase(item_to_edit[0])

        return redirect(url_for('showItem',
                                category_id=item_to_edit[1].id,
                                item_id=item_to_edit[0].id,
                                STATE=login_session.get('state')))
    else:
        return render_template('editItem.html',
                               category=item_to_edit[1],
                               item=item_to_edit[0],
                               STATE=login_session.get('state'))


@app.route('/category/<int:category_id>/deleteItem/<int:item_id>/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showCategories'))

    item_to_delete = db.getItemBy(item_id)

    if request.method == 'POST':
        if checkIfClientAuthorizedWith(request.form['state']) is False:
            return responseWith('Invalid authorization paramaters.', 401)

        db.deleteFromDatabase(item_to_delete[0])

        return redirect(url_for('showItemsForCategory',
                                category_id=item_to_delete[1].id))
    else:
        return render_template('deleteItem.html',
                               category=item_to_delete[1],
                               item=item_to_delete[0],
                               STATE=login_session.get('state'))


# Google connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    try:
        login_session['picture'] = data['picture']
    except Exception as e:
        login_session['picture'] = ""
    try:
        login_session['username'] = data['name']
    except Exception as e:
        login_session['username'] = ""
    try:
        login_session['email'] = data['email']
    except Exception as e:
        login_session['email'] = ""
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = db.getUserBy(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Facebook connect
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    # print "log in session", login_session['username']
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
    # see if user exists

    user_id = db.getUserBy(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect('/')
    else:
        flash("You were not logged in")
        return redirect('/')


# JSON API
@app.route('/catalog.json/')
def categoriesJSON():
    categories = db.getListOfCategories()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/category/<int:category_id>/items.json/')
def itemsJSON(category_id):
    items = db.getItemsFor(category_id)
    return jsonify(items=[item.serialize for item in items])


# oAuth Flow and Error Checking
def checkIfClientAuthorizedWith(client_state):
    return client_state == login_session['state']


# Utility Methods
def allowed_file(filename):
    if '..' in filename or filename.startswith('/'):
        return False
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def createLoginSession():
    if login_session.get('state') is None:
        login_session['state'] = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                         for x in xrange(32))


def responseWith(message, response_code):
    response = make_response(json.dumps(message), response_code)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
