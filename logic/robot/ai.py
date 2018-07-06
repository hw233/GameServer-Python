# -*- coding: utf-8 -*-

def startAI(who):
	setAI(who.id)
	
def setAI(roleId):
	'''设置AI
	'''
	who = robot.getClientRole(roleId)
	if not who:
		return
	
	who.startTimer(functor(setAI, roleId), rand(30, 60), "setAI")
	
	if not checkSetAI(who):
		return

	aiName = chooseKey(AIList, key="ratio", filt=lambda aiName,data:filtAI(who, aiName, data))
	if not aiName:
		return

	who.addAI(aiName)
	aiFunc = AIList[aiName]["ai"]
	aiFunc(roleId)
	
def checkSetAI(who):
	'''检查是否可以设置AI
	'''
	if who.inWar():
		return 0
	return 1

def filtAI(who, aiName, data):
	'''过滤AI
	'''
	if who.hasAI(aiName):
		return 0
	return 1



#===============================================================================
# AI列表
#===============================================================================
import robot.aiWalk

AIList = {
	"walk": {"ratio":30, "ai": robot.aiWalk.walk},
}


from common import *
import robot