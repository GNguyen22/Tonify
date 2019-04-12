# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
import json
import requests
import operator
import sqlite3
# Create your views here.

def index(request):
   return render(request, 'index.html', {})

def getAuthToken():
   params = {"grant_type" : "client_credentials"}
   headers = {"Authorization": "Basic OGVjNWE2N2RhNGExNDg4NWIwZWY4YWJkZDAyMDhlNDk6NTgwZGY0MzI4NmE3NGJjYjk1MDExNjVkYjQzN2IzZTc="}
   res = requests.post("https://accounts.spotify.com/api/token", data=params, headers=headers)
   return json.loads(res.text)['access_token']

def returnPlaylist(request):
   print(request.method)
   print(request.POST)
   profile = sqlite3.connect('personalization.db')
   c = profile.cursor()
   if (request.method == 'POST'):

      print(request.POST)
      text = request.POST['input']
      userName = request.POST['userName']
      c.execute("SELECT favorite_genre from profile WHERE name = ?", (userName,))
      genre = (c.fetchone())[0]
      #print("here and then genre")
      print(genre)
      auth_token = getAuthToken()
      sentiment_values = analyzeTone(text)
      playlist = generatePlaylist(sentiment_values, auth_token, genre)
      return JsonResponse(playlist)
   else:
      return HttpResponse("Incorrect http method", status=405);

def storeUser(request):
   print(request.method)
   print(request.POST)
   profile = sqlite3.connect('personalization.db')
   c = profile.cursor()
   if (request.method == 'POST'):
      print(request.POST)
      userName = request.POST['input']
      c.execute("SELECT * from profile WHERE name = ?", (userName,))
      existingUN = c.fetchone()
      if existingUN is None: # does not exist
         c.execute("INSERT INTO profile (name, email, favorite_genre) VALUES('%s', 'test@gmail.com', 'Pop')" % userName)
      else: # already exists
         pass
      profile.commit()
      profile.close()
      return JsonResponse({})
   else:
      return HttpResponse("Incorrect http method", status=405);

def storeGenre(request):
   print(request.method)
   print(request.POST)
   profile = sqlite3.connect('personalization.db')
   c = profile.cursor()
   if (request.method == 'POST'):
      print(request.POST)
      genre = request.POST['input']
      userName = request.POST['userName']
      print(genre)
      print(userName)
      c.execute("UPDATE profile SET favorite_genre = ? WHERE name = ?", (genre, userName,))
      profile.commit()
      profile.close()
      return JsonResponse({})
   else:
      return HttpResponse("Incorrect http method", status=405);


def analyzeTone(text):
   url = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
   params = {"version": "2018-11-16", "text" : text, "features" : "emotion"}
   print(params)
   auth = ("96218d67-7e51-44e3-911f-f96e0c14570b", "rj86GIfAotc0")
   res = requests.get(url, params=params, auth=auth)
   print(json.loads(res.text))

   return json.loads(res.text)["emotion"]["document"]["emotion"]

def top_emotion(sentiment_values):
   emotion = max(sentiment_values, key=sentiment_values.get)
   return emotion

def artist_seed(emotion):
   seed = "3wyVrVrFCkukjdVIdirGVY"
   if emotion == "anger":
      seed = "7dGJo4pcD2V6oG8kP0tJRR"
   elif emotion == "fear":
      seed = "26bcq2nyj5GB7uRr558iQg"
   elif emotion == "joy":
      seed = "5YGY8feqx7naU7z4HrwZM6"
   elif emotion == "sadness":
      seed = "3TVXtAsR1Inumwj472S9r4"
   return seed


def song_seed(emotion):
   seed = "43ZyHQITOjhciSUUNPVRHc"
   if emotion == "anger":
      seed = "6PPRKnwToRK9GjTCV03vlG"
   elif emotion == "fear":
      seed = "2KH16WveTQWT6KOG9Rg6e2"
   elif emotion == "joy":
      seed = "5Q0Nhxo0l2bP3pNjpGJwV1"
   elif emotion == "sadness":
      seed = "2z3htsNRuhDN923ITatc56"
   return seed

def generatePlaylist(sentiment_values, auth_token, genre):
   valence = sentiment_values["joy"]
   top = top_emotion(sentiment_values)
   seed_artist = artist_seed(top)
   seed_song = song_seed(top)
   #loudness, dancability, energy, acoustics, valence
   anger_mood = [0.0, 0.20, 0.80, 0.20, 0.20]
   fear_mood = [-30.0, 0.20, 0.20, 0.20, 0.20]
   joy_mood = [0.0, 0.80, 0.80, 0.20, 0.80]
   sadness_mood = [-30.0, 0.20, 0.20, 0.80, 0.20]
   cur_mood = []
   if top == "anger":
      cur_mood = anger_mood[:]
   elif top == "fear":
      cur_mood = fear_mood[:]
   elif top == "joy":
      cur_mood = joy_mood[:]
   elif top == "sadness":
      cur_mood = sadness_mood[:]

   url = "https://api.spotify.com/v1/recommendations"
   #params = {"min_energy" : valence,"max_mode" : "5", "market" : "US", "min_danceability" : valence, "seed_tracks" : seed_song , "seed_artists" : seed_artist , "target_popularity" : "30", "min_valence" : valence, "seed_genre" : genre, }
   genre = genre.lower()
   #params = {"seed_tracks" : seed_song , "seed_artists" : seed_artist , "seed_genres" : genre, }
   params = {"target_loudness" : cur_mood[0], "target_danceability" : cur_mood[1], "target_energy" : cur_mood[2], "target_acousticness" : cur_mood[3], "target_valence" : cur_mood[4], "seed_genres" : genre, }
   headers = {"Authorization": "Bearer " + auth_token}

   print(headers)
   print(params)
   res = requests.get(url, headers=headers, params=params)
   print(res)
   print(res.text)
   print(json.loads(res.text))
   return json.loads(res.text)
