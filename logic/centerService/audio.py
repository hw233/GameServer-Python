# -*- coding: utf-8 -*-

def newAudio(sContent):
	global gAudioKeeper, giAudioIdx
	giAudioIdx += 1
	audioObj = cAudio(giAudioIdx, sContent)
	gAudioKeeper = keeper.cKeeper() # 语音保持容器
	gAudioKeeper.addObj(audioObj, giAudioIdx)
	return audioObj


class cAudio(object):
	'''语音
	'''
	def __init__(self, idx, sContent):
		self.audioIdx = idx
		self.audioContent = sContent

def init():
	global gAudioKeeper, giAudioIdx
	gAudioKeeper = keeper.cKeeper() # 语音保持容器
	giAudioIdx = 0


import keeper