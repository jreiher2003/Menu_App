from app import app, bcrypt, db
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import RegistrationForm, LoginForm
from app.models import Users


users_blueprint = Blueprint("users", __name__, template_folder="templates") 

@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    state = "".join(random.choice(string.ascii_uppercase) for i in xrange(32))
    login_session['state'] = state
    error = None
    form = LoginForm(request.form) 
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        remember_me = form.remember_me.data 
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=remember_me)
            flash("You have signed in successfully!", "success")
            return redirect(url_for("home.show_places"))
        else:
            flash("<strong>Invalid Credentials.</strong> Please try again.", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html", form=form, STATE=state, error=error)

@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    # session.pop('logged_in', None)
    flash("You just logged out", "warning")
    referer = request.headers.get("Referer")
    return redirect(referer or url_for("home.show_places"))

@users_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        email_check = Users.query.filter_by(email=form.email.data).first()
        if email_check is None:
            user = Users(
                username=form.username.data, 
                email=form.email.data,
                avatar=form.avatar.data,
                password=bcrypt.generate_password_hash(form.password.data)
                )
        else:
            flash("That email account already exists! forgot your password? <a href='#'>Click Here</a>")
            return redirect(url_for('users.signup'))
        db.session.add(user)
        db.session.commit()
        referer = request.headers.get("Referer")
        flash('Thanks for registering')
        return redirect(referer or url_for('home.show_places'))
    return render_template('signup.html', form=form, error=error)

##################################################################
################# google+ signin #################################
##################################################################
from flask import session as login_session 
import random, string 
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError 
import httplib2
import json 
from flask import make_response  
import requests 
from config import BaseConfig
import os

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@users_blueprint.route("/login2", methods=["GET","POST"])
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase) for i in xrange(32))
    login_session['state'] = state 
    return render_template('google_login.html', STATE=state)

@users_blueprint.route("/gconnect", methods=["POST"])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope="")
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
    
    # login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s<br><img src='%s'><br><h2>%s</h2>%s" % (login_session['username'], login_session['picture'], login_session['email'], login_session['user_id']))
    print "done!"
    return output

@users_blueprint.route("/gdisconnect")
def gdisconnect():
    try:
        access_token = login_session['access_token']
    except KeyError:
        flash("Already logged out", "info")
        return redirect(url_for('home.show_places'))
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        logout_user()
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
    
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#######################################################################################
###################  facebook login  ##################################################
#######################################################################################
from app.utils import *

@users_blueprint.route("/login3", methods=["GET","POST"])
def show_fb_login():
    state = "".join(random.choice(string.ascii_uppercase) for i in xrange(32))
    login_session['state'] = state 
    return render_template('fb_login.html', STATE=state)

@users_blueprint.route("/fbconnect", methods=["POST"])
def fb_connect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers['Content-Type'] = "application/json"
        return response 
    access_token = request.data
    print "access token received %s " % access_token
    fb_secrets = json.loads(open('fb_client_secrets.json', 'r').read())
    app_secret = fb_secrets['web']['app_secret']
    app_id = fb_secrets['web']['app_id']
    print "app id :",app_id
    print "app secret: ", app_secret
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "this is the result", result

    # get token to get user info from app_id
    token = result.split("&")[0]
    userinfo_url = 'https://graph.facebook.com/v2.5/me?%s&fields=name,id,email' % token 
    h = httplib2.Http()
    result2 = h.request(userinfo_url, 'GET')[1]

    data = json.loads(result2)
    
    # login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result3 = h.request(url, 'GET')[1]
    data1 = json.loads(result3)

    login_session['picture'] = data1["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s<br><img src='%s'>" % (login_session['username'], login_session['picture']))
    return output

@app.route("/fbdisconnect")
def dbdisconnect():
    try:
        facebook_id = login_session["facebook_id"]
    except KeyError:
        flash("Already logged out", "info")
        return redirect(url_for('home.show_places'))
    
    url = "https://graph.facebook.com/%s/permissions" % facebook_id 
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"