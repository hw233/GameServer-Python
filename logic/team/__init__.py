# -*- coding: utf-8 -*-
'''队伍相关
'''
import u

if "gTeamList" not in globals():
	gTeamList = u.cKeyMapProxy()  # 队伍列表
	
def makeTeam(who):
	'''创建队伍
	'''
	if checkDennyTeam(who, None, "组队"):
		return None

	teamObj = team.object.Team()
	teamObj.setLeader(who)
	team.platformservice.setTeamDefaultTarget(who, teamObj)
	team.service.rpcTeamInfo(teamObj)
	team.service.rpcTeamBroadcastMake(teamObj)
	gTeamList.addObj(teamObj, teamObj.id)
	return teamObj


def checkTeamDennyAdd(who, teamObj, opName, showTips=True):
	'''检查队伍能否加人
	'''
	denyMsg = ""
	roleLeader = getRole(teamObj.leader)
	sceneObj = scene.getScene(roleLeader.sceneId)
	if sceneObj and hasattr(sceneObj, "denyTeamAddMember"):
		if opName in ("自动匹配", "接受申请", "邀请入队"):
			denyMsg = "{}内不可{}".format(sceneObj.denyTeamAddMember, opName)
		else:
			denyMsg = "目标在{}内不可{}".format(sceneObj.denyTeamAddMember, opName)
	
	if denyMsg:
		if showTips:
			message.tips(who, denyMsg)
		return True
	return False
	
def checkDennyTeam(who, targetObj, opName, teamObj=None):
	'''检查是否禁止组队
	'''
	denyMsg = ""
	if opName in ("组队", "申请入队",):
		sceneObj = scene.getScene(who.sceneId)
		if sceneObj.denyTeam:
			denyMsg = "{}场内不可组队".format(sceneObj.denyTeam)
		elif who.denyTeam:
			reason = who.denyTeam.values()[0]
			denyMsg = "{}中不可组队".format(reason)
	elif opName =="自动匹配":
		sceneObj = scene.getScene(who.sceneId)
		if sceneObj.denyTeam:
			denyMsg = "{}场内不可自动匹配".format(sceneObj.denyTeam)
		elif who.denyTeam:
			reason = who.denyTeam.values()[0]
			denyMsg = "{}中不可自动匹配".format(reason)
	else:
		sceneObj = scene.getScene(targetObj.sceneId)
		if sceneObj.denyTeam:
			denyMsg = "目标在{}场内，无法组队".format(sceneObj.denyTeam)
		elif targetObj.denyTeam:
			reason = targetObj.denyTeam.values()[0]
			denyMsg = "目标{}中，无法组队".format(reason)
		
	if denyMsg:
		message.tips(who, denyMsg)
		return True
	return False

def checkDenyQuitTeam(who, opName):
	'''检查是否禁止退出队伍
	'''
	denyQuitTeam = getattr(who, 'denyQuitTeam', None)
	print "checkDenyQuitTeam=",denyQuitTeam,opName
	if not denyQuitTeam:
		return
	denyMsg = ""
	if opName in ("暂离队伍", "退出队伍", ):
		if denyQuitTeam:
			denyMsg = "{}场内不可{}".format(denyQuitTeam, opName)

	if denyMsg:
		message.tips(who, denyMsg)
		return True
	return False

def getTeam(teamId):
	return gTeamList.getProxy(teamId)

def getAllTeam():
	for teamObj in gTeamList.getAll().itervalues():
		yield teamObj

def onUpLevel(who):
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	if teamObj.isLeader(who.id):
		teamObj.updateBuddyList()
	teamObj.attrChange(who.id,"level")
	
from common import *
import team.object
import team.service
import team.platformservice
import message
import scene