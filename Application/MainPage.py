from flask import Flask, url_for, redirect, \
    render_template, session, request, flash
import app as aa
from wtforms import Form, TextField, FieldList,TextAreaField, \
 validators, StringField, SubmitField,PasswordField
from flask_bootstrap import Bootstrap
from flask import jsonify ,json
from googletrans import Translator
import os
import subprocess
from textblob import TextBlob
import pandas as pd
import sqlite3
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 



access_token = "1090058577606336512-tJlBxmM8OD7Ujwmv0ibgFb3GSUNqD8"
access_token_secret = "UjqYk6spEvWgSc9tVasaGtNawprMy8K74XDWntIs3N1qP"
consumer_key = "szs3099CypNSKmnUXPWd7oK5s"
consumer_secret = "7tWGY0VXWuPrhFJvmaHaKXjpcg6id3dt0ty46tiuW4jp8vkfJF"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
trans = Translator()

app = Flask(__name__)

message = []
align = []
sentiment = []
confidence = []
color = []
text = []


def drawPieChart():
	conn = sqlite3.connect('../Twitter_Graph/twitter.db')
	c = conn.cursor()
	df = pd.read_sql("SELECT * FROM sentiment", conn)
	neutral = 0
	cyberbullying = 0
	not_cyberbullying = 0
	for i in df.sentiment:
		if i >= 0.0:
			not_cyberbullying += 1
		elif i < -0.01:
			cyberbullying += 1			
		elif i > -0.01 and i < 0.01:
			neutral += 1

	return cyberbullying,not_cyberbullying,neutral



@app.route("/",methods=['POST','GET'])
def Home():
	conn = sqlite3.connect('../Twitter_Graph/twitter.db')
	c = conn.cursor()
	df = pd.read_sql("SELECT * FROM sentiment", conn)
	count = 0
	for i in df.sentiment:
		if i > 0:
			count += 1
	chats = open('logs/chats.txt', 'r', encoding = 'latin-1').read().split('\n')
	for i in chats:
		if i == '':
			chats.remove(i)
	chats.reverse()
	label = open('logs/label.txt', 'r', encoding = 'latin-1').read().split('\n')
	for i in label:
		if i == '':
			label.remove(i)
	label.reverse()
	miss = open('logs/missed.txt', 'r', encoding = 'latin-1').read().split('\n')
	for i in miss:
		if i == '':
			miss.remove(i)

	##############Twitter Trends################
	trends1 = api.trends_place(23424848)
    #Korea = 23424868
    #USA   = 23424977
    #india = 23424848
	data = trends1[0]
	trends_cd = data['trends']
	name_of_trend = []
	for i in trends_cd:
		name_of_trend.append(i['name'])

	#results = twitter.trends.place(_id = 23424975)
	#print(name_of_trend)
	##############Twitter Trends################

	##############Pie Chart################
	c,nc,n = drawPieChart()

	##############Pie Chart################


	return render_template('index.html',count = count, c = c, nc = nc, n = n, chats_count = len(chats), chats = chats, label = label, miss = len(miss), name_of_trend = name_of_trend)

@app.route("/clearpage",methods=['POST','GET'])
def clearpage():
	global message
	message = []
	return render_template("chat.html", m = message)



@app.route("/twitter",methods=['POST','GET'])
def tweetexctractor():
	os.system("uxterm -e tweet &")
	return render_template('LandingPage.html')



@app.route("/ChatPage",methods=['POST','GET'])
def chatPage():
	
	if request.method == 'POST':
		#n = request.form['name']
		m = request.form['message']
	
		flag = 0

		if m != "" and not m in message:
			chats = open('logs/chats.txt', 'a')
			chats.write(m + '-' +'\n')
			chats.close()
			for i in message:
				if  m == i:
					flag = 1

			if flag == 0:			

				
				message.append(m)

				langValue = trans.detect(m)
				if(langValue.lang != 'en'):
					ConvertedText = trans.translate(m)
					#sent= aa.analyser(ConvertedText.text) #sa.analyzeSentiment(ConvertedText.text)
					sent = TextBlob(ConvertedText.text)
					if sent.sentiment.polarity >= 0.0:
						sentiment.append('Not Cyberbullying')
						label = open('logs/label.txt', 'a')
						label.write("Not Cyberbullying" + '\n')
						label.close()
						
					elif sent.sentiment.polarity <= -0.01:
						sentiment.append('Cyberbullying')
						label = open('logs/label.txt', 'a')
						label.write("Not Cyberbullying" + '\n')
						label.close()
						
					elif sent.sentiment.polarity > -0.01 and sent.sentiment.polarity < 0.0:
						miss = open('logs/missed.txt', 'a')
						miss.write(m + '\n')
						label = open('logs/label.txt', 'a')
						label.write("Not Detected" + '\n')
						label.close()
					#confidence.append(conf)
					

				else:
					#sent= aa.analyser(m)
					sent = TextBlob(m)
					if sent.sentiment.polarity >= 0.0:
						sentiment.append('Not Cyberbullying')
						label = open('logs/label.txt', 'a')
						label.write("Not Cyberbullying" + '\n')
						label.close()
					elif sent.sentiment.polarity < -0.01:
						sentiment.append('Cyberbullying')
						label = open('logs/label.txt', 'a')
						label.write("Cyberbullying" + '\n')
						label.close()
					elif sent.sentiment.polarity > -0.01 and sent.sentiment.polarity < 0.0:
						sentiment.append('Not Detected')
						miss = open('logs/missed.txt', 'a')
						miss.write(m + '\n')

				print(sent.sentiment.polarity)
				if sent.sentiment.polarity <= -0.01:
					color.append("red")
					text.append("Cyberbullying!")

				elif sent.sentiment.polarity >= 0.0:
					color.append("green")
					text.append("Not Cyberbullying!")
				elif sent.sentiment.polarity > -0.01 and sent.sentiment.polarity < 0.0:
					color.append("yellow")
					text.append("Neutral Statement!")

		print(color)
			
		l = len(message)
		print(sentiment)

		return render_template("cybcheck.html", m = message, l = l, align = align, clr = color, text = text)
	return render_template('cybcheck.html')


if __name__ == "__main__":
    app.run(debug=True,port=5001)