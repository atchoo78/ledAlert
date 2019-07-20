#!/usr/bin/env python

import Foundation
from AppKit import *
from PyObjCTools import AppHelper
import requests

BASEURI = "http://rpi3.local:8181"
LED_URL = BASEURI + "/led"

class GetSongs(NSObject):
	def getMySongs_(self, song):
		song_details = {}
		ui = song.userInfo()
		song_details = dict(zip(ui.keys(), ui.values()))
		playerState = (song_details['Player State'])
		if not('Stopped' in playerState):
			nowPlaying = song_details['Artist'] + ' : ' + song_details['Name']
			theArtist = song_details['Artist']
			theSong = song_details['Name']
			theAlbum = song_details['Album']
			if("Track ID" in song_details):   # trying to find another way around this, but it kind of works for now :)
				thePlayer = "Spotify" 
			else:
				thePlayer = "iTunes"
		else:
			return	   
	
			ledDisplay = requests.post(url = LED_URL, data = nowPlaying.encode('utf-8'))
					
nc = Foundation.NSDistributedNotificationCenter.defaultCenter()
GetSongs = GetSongs.new()
nc.addObserver_selector_name_object_(GetSongs, 'getMySongs:', 'com.apple.iTunes.playerInfo',None)
nc.addObserver_selector_name_object_(GetSongs, 'getMySongs:', 'com.spotify.client.PlaybackStateChanged',None)

AppHelper.runConsoleEventLoop()
