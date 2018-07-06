# -*- coding: utf-8 -*-


def triggerEvent(w, event):
	'''触发事件
	'''
	if event == "倒地" and w.isRole():
		roleDead(w)  #特殊处理
		return
	if not w.isBuddy() and not w.isPet():
		return
	who = getRole(w.ownerId)
	if not who :
		return
	entityType,entityNo = getEntity(w,who)
	if not entityType:
		return
	if not checkCnt(w, event):
		return
	probability = wordsData.getProbability(event) * 100
	if rand(1,100) <= probability:
		content = who.words.getWords(entityType,entityNo,strToEvent[event])
		if content:
			w.war.say(w,content,strToEvent[event])
			addCnt(w, event)

def getEntity(w, who):
	if w.isBuddy():
		return 2,w.id
	elif w.isPet():
		petObj = who.petCtn.getItem(w.id)
		if petObj:
			return 1,petObj.idx
	return 0,0

def addCnt(w, event):
	if event == "登场":
		if not hasattr(w.war, "startWords"):
			w.war.startWords = 1
		else:
			w.war.startWords += 1

def checkCnt(w, event):
	if event == "登场" and getattr(w.war,"startWords",0)>=2:
		return False
	return True

def roleDead(w):
	probability = wordsData.getProbability("主人倒地") * 100
	if rand(1,100) > probability:
		return
	for fw in w.getFriendList():
		if (fw.isPet() or fw.isBuddy()) and fw.ownerIdx == w.idx:
			who = getRole(w.id)
			if not who:
				return
			entityType,entityNo = getEntity(fw,who)
			if not entityType:
				continue
			content = who.words.getWords(entityType,entityNo,WORDS_ROLE_DEAD)
			if content:
				w.war.say(fw,content,WORDS_ROLE_DEAD)
				break

from common import *
from words.defines import *
import wordsData