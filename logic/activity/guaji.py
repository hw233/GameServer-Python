# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		1001:'''成功领取除妖卫道任务''',
		1002:'''你身上已经有除妖卫道的任务了''',
		1003:'''你今天已经完成除妖卫道的任务了，明天再来吧 !''',
		1004:'''挂机设置成功，战斗后生效''',
		2001:'''已成功冻结$point双倍点数''',
		2002:'''无双倍点数可冻结''',
		2003:'''已成功领取$point双倍点数''',
		2004:'''领取达到上限''',
		3001:'''已开启离线降魔功能，当下线后即会进行离线降魔''',
		3002:'''当前储备生命或真气过低，请及时补充''',
		3003:'''活跃需达到#C0975#n点，才可开启离线挂机''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
		"需要活跃":75,
	}
#导表结束

	def transToAnleiScene(self, who, sceneId):
		'''传送到挂机暗雷场景
		'''
		if sceneId not in anleiData.sceneFight:
			raise "[guaji]invalid anlei scene:%d" % sceneId
			return
		if not scene.tryTransfer(who, sceneId):
			return
		# toDo 通知客户端巡逻
		
	def setAutoFight(self, who, isAuto):
		'''设置自动战斗
		'''
		if who.inWar():
			self.doScript(who, None, "TP1004")
		who.setAutoFight(isAuto)
		
	def setRoleDefaultPerform(self, who, performId):
		'''设置玩家默认技能
		'''
		if who.inWar():
			self.doScript(who, None, "TP1004")
		who.setDefaultPerform(performId)
		rpcConfigChange(who, "rolePfId")
		
	def setPetDefaultPerform(self, who, performId):
		'''设置宠物默认技能
		'''
		if who.inWar():
			self.doScript(who, None, "TP1004")
		petObj = who.petCtn.getFighter()
		if not petObj:
			return
		petObj.setDefaultPerform(performId)
		rpcConfigChange(who, "petPfId")

	def setRoleOfflinePerform(self, who, performId):
		'''设置玩家离线挂机法术
		'''
		if who.inWar():
			self.doScript(who, None, "TP1004")
		who.setOfflinePerform(performId)
		rpcConfigChange(who, "roleOfflinePfId")

	def setPetOfflinePerform(self, who, performId):
		'''设置宠物离线挂机法术
		'''
		if who.inWar():
			self.doScript(who, None, "TP1004")
		petObj = who.petCtn.getFighter()
		if not petObj:
			return
		petObj.setOfflinePerform(performId)
		rpcConfigChange(who, "petOfflinePfId")

	def trySetOfflineTask(self, who, isOfflineTask):
		'''尝试设置离线挂机
		'''
		if isOfflineTask and not self.validActPoint(who):
			self.doScript(who, None, "TP3003")
			return
		who.setOfflineTask(isOfflineTask)
		rpcConfigChange(who, "isOfflineTask")
		if isOfflineTask:
			if who.reserveHp < (who.reserveHpMax * 0.1) or who.reserveMp < (who.reserveMpMax * 0.1):
				self.doScript(who, None, "TP3002")
			else:
				self.doScript(who, None, "TP3001")
				
	def validActPoint(self, who):
		'''检查活跃值
		'''
		if who.getActPoint() < self.configInfo["需要活跃"]:
			return False
		return True

	def setConfig(self, who, **attrList):
		'''设置挂机
		'''
		for attrName, attrVal in attrList.iteritems():
			if attrName == "rolePfId":
				self.setRoleDefaultPerform(who, attrVal)
			elif attrName == "petPfId":
				self.setPetDefaultPerform(who, attrVal)
			elif attrName == "roleOfflinePfId":
				self.setRoleOfflinePerform(who, attrVal)
			elif attrName == "petOfflinePfId":
				self.setPetOfflinePerform(who, attrVal)
			elif attrName == "isOfflineTask":
				self.trySetOfflineTask(who, attrVal)

	def giveTask(self, who):
		'''领取除妖卫道任务
		'''
		taskId = 10301
		taskObj = task.hasTask(who, taskId)
		if taskObj:
			self.doScript(who, None, "M1002")
			return
		if who.day.fetch("monsterCntTask"):
			self.doScript(who, None, "M1003")
			return
		
		task.newTask(who, None, taskId)
		who.day.set("monsterCntTask", 1)
		self.doScript(who, None, "M1001")
		
	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("101-传送到挂机暗雷场景")
			txtList.append("102-设置自动战斗")
			txtList.append("103-设置玩家默认技能")
			txtList.append("104-设置宠物默认技能")
			txtList.append("105-领取除妖卫道任务")
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 101:
			try:
				sceneId = int(args[0])
			except:
				message.tips(who, "参数：场景编号")
				return
			self.transToAnleiScene(who, sceneId)
		elif cmdIdx == 102:
			try:
				isAuto = int(args[0])
			except:
				message.tips(who, "参数：0或1")
				return
			self.setAutoFight(who, isAuto)
		elif cmdIdx == 103:
			try:
				performId = int(args[0])
			except:
				message.tips(who, "参数：法术编号")
				return
			self.setRoleDefaultPerform(who, performId)
		elif cmdIdx == 104:
			try:
				performId = int(args[0])
			except:
				message.tips(who, "参数：宠物id 法术编号")
				return
			self.setPetDefaultPerform(who, performId)
		elif cmdIdx == 105:
			self.giveTask(who)

	def onNewHour(self, day, hour, wday):
	#玩家刷小时时
		import role
		role.callForAllRoles(whetherCancelOffline)
	

		
# ================================================================
# rpc相关的
# ================================================================

def getActivityGuaji():
	return activity.getActivity("guaji")

def whetherCancelOffline(who):
	#检查所有玩家是否符合取消挂机的条件
	if not who.isOfflineTask():
		return
	hour = getDatePart(partName="hour")
	if hour < 8:
		return
	actObj = getActivityGuaji()
	if actObj.validActPoint(who):
		return
	who.setOfflineTask(False)
	rpcConfigChange(who, "isOfflineTask")

def rpcTrans(who, reqMsg):
	'''传送到挂机暗雷场景
	'''
	actObj  = getActivityGuaji()
	sceneId = reqMsg.iValue
	actObj.transToAnleiScene(who,sceneId)

def rpcSetAutoFight(who, reqMsg):
	'''设置自动战斗
	'''
	actObj = getActivityGuaji()
	isAuto = reqMsg.bValue
	actObj.setAutoFight(who,isAuto)

def rpcSetConfig(who, reqMsg):
	'''设置挂机
	'''
	attrList = {}
	for attrObj, attrVal in reqMsg.ListFields():
		attrName = attrObj.name
		attrList[attrName] = attrVal
	actObj = getActivityGuaji()
	actObj.setConfig(who, **attrList)

def rpcGetConfig(who, reqMsg):
	'''获取挂机设置
	'''
	rpSendConfig(who)

def rpcGetTask(who,reqMsg):
	'''领取除妖卫道任务
	'''
	actObj = getActivityGuaji()
	actObj.giveTask(who)

def rpcMonsterCnt(who,reqMsg):
	'''请求当前除妖数
	'''
	return who.day.fetch("killMonsterCnt",0)

def rpSendConfig(who):
	'''发送挂机设置
	'''
	msg = packConfigMsg(who)
	who.endPoint.rpcActGuajiConfig(**msg)

def packConfigMsg(who, *attrNameList):
	'''打包挂机设置
	'''
	if not attrNameList:
		attrNameList = (
			"rolePfId", # 人物法术
			"petPfId", # 宠物法术
			"roleOfflinePfId", # 离线降魔的人物法术
			"petOfflinePfId", # 离线降魔的宠物法术
			"isOfflineTask", # 是否离线降魔
			"offlineTaskRing", # 剩余离线降魔次数
		)
	
	petObj = who.petCtn.getFighter()

	msg = {}
	for attrName in attrNameList:
		if attrName == "rolePfId":
			msg[attrName] = who.getDefaultPerform()
		elif attrName == "petPfId":
			msg[attrName] = petObj.getDefaultPerform() if petObj else war.defines.CMD_TYPE_PHY
		elif attrName == "roleOfflinePfId":
			msg[attrName] = who.getOfflinePerform()
		elif attrName == "petOfflinePfId":
			msg[attrName] = petObj.getOfflinePerform() if petObj else war.defines.CMD_TYPE_PHY
		elif attrName == "isOfflineTask":
			msg[attrName] = who.isOfflineTask()
		elif attrName == "offlineTaskRing":
			msg[attrName] = task.offlineTask.getOfflineRing(who)

	return msg

def rpcConfigChange(who, *attrNameList):
	msg = packConfigMsg(who, *attrNameList)
	who.endPoint.rpcActGuajiConfigChange(**msg)

def rpcPetChange(who):
	rpcConfigChange(who,"petPfId","petOfflinePfId")

from common import *
import task
import message
import anleiData
import scene
import activity
import war.defines
import task.offlineTask
