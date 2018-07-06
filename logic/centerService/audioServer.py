# -*- coding: utf-8 -*-
'''
语音服务器
'''
def application(env, start_response):
	# print env
	# print start_response
	sPath = env["PATH_INFO"]
	sMethod = env["REQUEST_METHOD"]
	sQuery = env["QUERY_STRING"]
	if sMethod == "POST":
		try:
			request_body_size = int(env.get('CONTENT_LENGTH', 0))
		except ValueError, ve:
			request_body_size = 0
		if request_body_size <= 0 or request_body_size > 1024 * 1024:
			# 0<size<=1m
			start_response('403 FORBIDDEN', [('Content-Type', 'text/html')])
			yield '<h1>Audio Too Long</h1>'
		else:
			request_body = env["wsgi.input"].read(request_body_size)
			start_response('200 OK',[('Content-Type','text/html;charset=utf8')])
			yield str(uploadAudio(request_body))
	elif sMethod == "GET":
		if len(sQuery) > 0:
			dQuery = urlparse.parse_qs(sQuery)
			audioIdx = int(dQuery.get("aId", [0])[0])
			if audioIdx:
				start_response('200 OK',[('Content-Type','text/html;charset=utf8')])
				yield downloadAudio(audioIdx)
			else:
				start_response('404 Not Found',[('Content-Type','text/html')])
				yield '<h1>Not Found</h1>'
		else:
			start_response('404 Not Found',[('Content-Type','text/html')])
			yield '<h1>Not Found</h1>'
	else:
		start_response('404 Not Found',[('Content-Type','text/html')])
		yield '<h1>Not Found</h1>'

def initServer():
	iPort = config.CENTER_AUDIO_PORT
	oServer = gevent.pywsgi.WSGIServer(('', iPort), application, log=sys.stdout)
	print "starting audio server on port {}".format(iPort)
	return oServer

def uploadAudio(sContent):
	audioObj = centerService.audio.newAudio(sContent)
	if audioObj:
		return audioObj.audioIdx
	return 0

def downloadAudio(audioIdx):
	audioObj = centerService.audio.gAudioKeeper.getObj(audioIdx)
	if audioObj:
		return audioObj.audioContent
	return ""


import sys
import gevent.pywsgi
import urlparse
import config
import centerService.audio
