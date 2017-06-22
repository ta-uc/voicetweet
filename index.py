from flask import Flask, request, session
import flask
import tweepy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SEC']
CONSUMER_TOKEN=os.environ['CON_TOKEN']
CONSUMER_SECRET=os.environ['CON_SECRET']
CALLBACK_URL = 'url_for_server/verify'

@app.route("/")
def send_token():
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)

	try:
		redirect_url = auth.get_authorization_url()
		session['request_token'] = auth.request_token
	except tweepy.TweepError:
		return 'Error! Failed to get request token'

	return flask.redirect(redirect_url)

@app.route("/verify")
def get_verification():

	verifier = request.args['oauth_verifier']

	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	token = session.pop('request_token')
	auth.request_token = token

	try:
		    auth.get_access_token(verifier)
	except tweepy.TweepError:
		    return 'Error! Failed to get access token.'

	session['token'] = (auth.access_token, auth.access_token_secret)
	session['k'] = 1
	return flask.redirect(flask.url_for('ddevice'))

@app.route("/device")
def ddevice():
	if(session.get('k') != 1):
		return flask.redirect(flask.url_for('send_token'))
	return''' <div style="font-size: 6vw; margin-left: auto; margin-right: auto;margin-top:50px;width: 90%;height:50%;">
	          <a href="./vt?dvc=pc">     PC</a><br><br>
	          <a href="./vt?dvc=m">      Android</a>
		  </div>
	      '''

@app.route("/vt")
def showMainscreen():
	dvc = request.args["dvc"]
	if(session.get('k') != 1):
		return flask.redirect(flask.url_for('send_token'))
	return flask.render_template('index.html',dvc=dvc)

@app.route("/post", methods=['POST'])
def post():
	if(session.get('k') != 1):
		return flask.redirect(flask.url_for('send_token'))
	token, token_secret = session['token']
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)
	tweet = request.form['tw'].encode('utf-8')
	api.update_status(tweet)
	return ''
