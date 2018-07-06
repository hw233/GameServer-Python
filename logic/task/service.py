# -*- coding: utf-8 -*-
# 任务服务
import endPoint
import task_pb2
import time

class cService(task_pb2.terminal2main):

	@endPoint.result
	def rpcTaskAbort(self, ep, who, reqMsg): return rpcTaskAbort(who, reqMsg)
	
	@endPoint.result
	def rpcTaskQuest(self, ep, who, reqMsg): return rpcTaskQuest(who, reqMsg)
	
	@endPoint.result
	def rpcTaskQuestGoAhead(self, ep, who, reqMsg): return rpcTaskQuestGoAhead(who, reqMsg)

	@endPoint.result
	def rpcTaskPetSelect(self, ep, who, reqMsg): return rpcTaskPetSelect(who, reqMsg)

	@endPoint.result
	def rpcTaskLookPetInfo(self, ep, who, reqMsg): return rpcTaskLookPetInfo(who, reqMsg)
	
	@endPoint.result
	def rpcTaskStoryStop(self, ep, who, reqMsg): return rpcTaskStoryStop(who, reqMsg)

	@endPoint.result
	def rpcTaskAskForHelp(self, ep, who, reqMsg): return rpcTaskAskForHelp(who, reqMsg)


def checkTaskOP(who, taskId):
	'''检查任务操作
	'''
	teamObj = who.inTeam()
	if teamObj and not teamObj.isLeader(who.id): # 在队，只有队长才能操作
		return None

	taskObj = who.taskCtn.getItem(taskId)
	if not taskObj and teamObj:
		taskObj = teamObj.taskCtn.getItem(taskId)
	if not taskObj or not taskObj.inGame(who):
		return None
	return taskObj

def rpcTaskAbort(who, reqMsg):
	'''放弃任务
	'''
	taskId = reqMsg.id
	taskObj = who.taskCtn.getItem(taskId)
	if not taskObj:
		teamObj = who.inTeam()
		if teamObj and teamObj.isLeader(who.id):
			taskObj = teamObj.taskCtn.getItem(taskId)
	if not taskObj or not taskObj.inGame(who):
		return
	if not taskObj.canAbort():
		message.tips(who, "此任务不可放弃")
		return
	
	writeLog("task/abort", "%d %d" % (who.id, taskObj.id))
	taskObj.abort(who)
				
def rpcTaskQuest(who, reqMsg):
	'''任务请求
	'''
	if who.inWar():
		return
	
	taskId = reqMsg.taskId
	npcId = reqMsg.npcId

	ti = getSecond()
	if hasattr(who, "taskQuestCount") and who.taskQuestCount["time"] == ti:
		who.taskQuestCount["count"] += 1
		if who.taskQuestCount["count"] >= 5:
			message.debugClientMsg(who, "rpcTaskQuest请求太繁忙")
			return
	else:
		who.taskQuestCount = {"time":ti, "count":1}

	taskObj = checkTaskOP(who, taskId)
	if not taskObj:
		return
	
	npcObj = getNpc(npcId)
	if npcObj:
		npcObj = npcObj.this()
	else:
		return

	if not scene.isNearBy(who, npcObj, 30):
		message.tips(who, "距离太远了")
		return

	taskObj.quest(who, npcObj)
		
def rpcTaskQuestGoAhead(who, reqMsg):
	'''请求目标坐标
	'''
	if who.inWar():
		return
	
	taskId = reqMsg.id
	
	ti = getSecond()
	if hasattr(who, "taskGoAheadCount") and who.taskGoAheadCount["time"] == ti:
		who.taskGoAheadCount["count"] += 1
		if who.taskGoAheadCount["count"] >= 5:
			message.debugClientMsg(who, "rpcTaskQuestGoAhead请求太繁忙")
			return
	else:
		who.taskGoAheadCount = {"time":ti, "count":1}
	
	taskObj = checkTaskOP(who, taskId)
	if not taskObj:
		return

	taskObj.goAhead(who)

def rpcTaskStoryStop(who, reqMsg):
	'''结束客户端剧情
	'''
	taskId = reqMsg.iValue
	taskObj = checkTaskOP(who, taskId)
	if not taskObj:
		return

	storyInfo = taskObj.fetch("storyInfo")
	if not storyInfo:
		return
	taskObj.delete("storyInfo")

	teamObj = who.inTeam()
	if teamObj and teamObj.isLeader(who.id):
		roleList = teamObj.getInTeamList()
	else:
		roleList = [who.id]

	for roleId in roleList:
		roleObj = getRole(roleId)
		if roleObj:
			roleObj.endPoint.rpcTaskStoryStop(taskObj.id)
			
	eventIdx = storyInfo["storyEventIdx"]
	if not eventIdx:
		return
	eventInfo = taskObj.getEventInfo(eventIdx)
	if not eventInfo:
		return
	
	npcObj = None
	npcId = storyInfo["storyNpcId"]
	if npcId:
		npcObj = getNpc(npcId)
		if npcObj:
			npcObj = npcObj.this()
	taskObj.doScript(who, npcObj, eventInfo["成功"])

def rpcTaskAskForHelp(who, reqMsg):
	'''任务求助
	'''
	if not who.getGuildObj():
		message.tips(who, "你还没加入仙盟，无法发送求助信息")
		return
	taskId = reqMsg.iValue
	taskObj = who.taskCtn.getItem(taskId)
	if not taskObj:
		message.tips(who, "没有对应的任务，无法求助")
		return
	if not getattr(taskObj, "askForHelp", None):
		message.tips(who, "该任务不能求助")
		return
	taskObj.askForHelp(who)


#===============================================================================
# 服务端发往客户端
#===============================================================================
def rpcTaskAdd(who, taskObj):
	'''增加任务
	'''
	taskMsg = packetTask(who, taskObj)
	who.endPoint.rpcTaskAdd(taskMsg)
			
def rpcTaskAll(who):
	'''登录一次性发送所有任务包
	'''
	taskMsgList = []
	for taskObj in who.taskCtn.getAllValues():
		taskMsgList.append(packetTask(who, taskObj))
		
	taskMsgAll = task_pb2.taskMsgAll()
	taskMsgAll.taskMsgList.extend(taskMsgList)
	who.endPoint.rpcTaskAll(taskMsgAll)
	
def packetTask(who, taskObj):
	'''打包任务信息
	'''
	# 任务npc
	taskNpcList = []
	for npcObj in taskObj.getTaskNpcList().itervalues():
		taskNpcList.append(packetNpc(npcObj))
	
	# 任务关联的非任务npc
	sceneNpcList = taskObj.getSceneNpcList().keys()
	
	# 任务所需物品
	propsList = [packetNeed(propsNo,amount) for propsNo,amount in taskObj.getPropsNeeded().iteritems()]
	
	taskTime = taskObj.getTime()
	if taskTime is None:
		taskTime = 0

	taskMsg = task_pb2.taskMsg()
	taskMsg.id = taskObj.id
	taskMsg.targetType = taskObj.targetType
	taskMsg.icon = taskObj.icon
	taskMsg.title = taskObj.getTitle(who)
	taskMsg.intro = taskObj.getIntro(who)
	taskMsg.detail = taskObj.getDetail(who)
	taskMsg.rewardDesc = taskObj.rewardDesc
	taskMsg.npcList.extend(taskNpcList)
	taskMsg.sceneNpcList.extend(sceneNpcList)
	taskMsg.propsList.extend(propsList)
	taskMsg.time = taskTime
	taskMsg.canAbort = taskObj.canAbort()
	taskMsg.isDone = taskObj.isDone()
	
	return taskMsg
	
def packetNpc(npcObj):
	npcMsg = task_pb2.npcMsg()
	npcMsg.id = npcObj.id
	npcMsg.name = npcObj.name
	npcMsg.shape = npcObj.shape
	npcMsg.shapeParts.extend(npcObj.shapeParts)
	npcMsg.colors.extend(npcObj.getColors())
	npcMsg.sceneId = npcObj.sceneId
	npcMsg.x = npcObj.x
	npcMsg.y = npcObj.y
	npcMsg.d = npcObj.d
	npcMsg.type = npcObj.npcType
	npcMsg.title = npcObj.title
	npcMsg.action = npcObj.action
	npcMsg.effectId = npcObj.effectId
	return npcMsg

def packetNeed(idx, amount):
	needMsg = task_pb2.needMsg()
	needMsg.no = idx
	needMsg.amount = amount
	return needMsg

def rpcTaskDel(who, taskObj):
	'''删除任务
	'''
	who.endPoint.rpcTaskDel(taskObj.id)
	
def rpcTaskChange(who, taskObj, *attrNameList):
	'''改变任务信息
	'''
	msg = {
		"id": taskObj.id,
	}
	for attrName in attrNameList:
		msg[attrName] = taskObj.getValByName(attrName, who)
			
	who.endPoint.rpcTaskChange(**msg)
			
def refreshTask(who, taskObj):
	'''刷新任务
	'''
	taskMsg = packetTask(who, taskObj)
	who.endPoint.rpcTaskChange(taskMsg)

def packet4Hyperlink(who,taskObj):
	'''超链接信息
	'''
	taskMsg = task_pb2.taskMsg()
	taskMsg.id = taskObj.id
	taskMsg.title = taskObj.getTitle(who)
	introFunc = getattr(taskObj, "getHyperlinkIntro", taskObj.getIntro)
	taskMsg.intro = introFunc(who)
	taskMsg.detail = taskObj.getDetail(who)

	return taskMsg

def rpcTaskPetSelect(who, reqMsg):
	'''领取宠物任务
	'''
	petNo = reqMsg.iValue
	npcObj = npc.getNpcByIdx(10208)
	if npcObj:
		npcObj.givePetTask(who, petNo)

def rpcTaskLookPetInfo(who, reqMsg):
	'''查看宠物任务宠物信息
	'''
	petNo = reqMsg.iValue
	npcObj = npc.getNpcByIdx(10208)
	if npcObj:
		npcObj.lookPetInfo(who, petNo)
		
def storyPlay(who, taskObj, storyId):
	'''播放客户端剧情
	'''
	msg = {
		"taskId": taskObj.id,
		"storyId": storyId
	}
	who.endPoint.rpcTaskStoryPlay(**msg)


from common import *
import message
import scene
import npc