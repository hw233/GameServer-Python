# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity
#副本活动

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
		101:{"名称":"竹林除妖","资源":1040,"着陆点x":32,"着陆点y":17},
		102:{"名称":"幻波池","资源":1060,"着陆点x":77,"着陆点y":9},
	}

	configInfo = {
	}

	instanceData = {
		1:{"名字":"竹林除妖","活动中心编号":16,"场景编号":101,"难度":1,"显示等级":45,"最大等级":60,"奖励":(246001,234201),"简介":"据传言附近村民最近离奇失踪，怕是有妖人在作祟。村民们人心惶惶，不敢迈出家门。乡绅们出资邀请侠客帮忙解决。"},
		2:{"名字":"幻波池","活动中心编号":22,"场景编号":102,"难度":2,"显示等级":55,"最大等级":70,"奖励":(246001,234202),"简介":"某真人苦受心魔之苦，尔等前去消除心魔幻影助其缓解心魔"},
		3:{"名字":"两仪法阵","活动中心编号":16,"场景编号":101,"难度":1,"显示等级":99,"最大等级":80,"奖励":(246001,234201),"简介":"天地初开，一切皆为混沌，是为无极，无极生太极，太极生两仪，两仪为阴阳。"},
		4:{"名字":"四象迷宫","活动中心编号":16,"场景编号":101,"难度":2,"显示等级":99,"最大等级":90,"奖励":(246001,234202),"简介":"东方为苍龙象，北方为玄武象，西方为白虎象，南方为朱雀象"},
	}
#导表结束
	def init(self):
		role.geOffLine += self.roleOffLine
		role.geLogin+=self.roleOnLine

	def getInstanceData(self, index, key, default=0):
		return self.instanceData.get(index, {}).get(key, default)

	def enterInstance(self, who, index):
		'''进入副本
		'''
		if index not in self.instanceData:
			return

		teamObj = who.getTeamObj()
		if not teamObj:
			message.tips(who, "副本任务凶险，请找多几个同伴（最少3人）再来")
			return
		if not teamObj.isLeader(who.id):
			message.tips(who, "你已处于队伍中，请回归队伍")
			return

		if not who.validInTeamSize(3):
			message.tips(who, "副本任务凶险，请找多几个同伴（最少3人）再来")
			return

		res = self.handleTeamConfirm(who, teamObj, index)
		if not res:
			return
		self.giveInstanceTask(who, teamObj, index)

	def giveInstanceTask(self, who, teamObj, index):
		'''给副本任务
		'''
		if index not in gdAllInstanceTaskParentId:
			return
		sceneObj = self.getInstanceScene(teamObj.id, index)
		if not sceneObj:
			sceneIdx = self.getInstanceData(index, "场景编号", 0)
			sceneObj = self.addScene(sceneIdx, "instanceScene")
			sceneObj.instanceInfo = (teamObj.id, index)
			# sceneObj.eventOnEnter += self.onEnterScene
			# sceneObj.eventOnLeave += self.onLeaveScene
			sceneObj.denyTeam = "副本"
		if not scene.tryTransfer(who, sceneObj.id, None, None):
			return
		func = gdAInstanceTask.get(index, None)
		if func:
			func(who)

		#加活跃
		perPoint = activity.center.getPerActPoint(self.getInstanceData(index, "活动中心编号", 0))
		for pid in teamObj.getInTeamList():
			roleObj = getRole(pid)
			if not roleObj:
				continue
			lInstanceActPoint = roleObj.day.fetch("instanceActPoint", [])
			if index in lInstanceActPoint:
				continue
			
			lInstanceActPoint.append(index)
			roleObj.addActPoint(perPoint)
			roleObj.day.set("instanceActPoint", lInstanceActPoint)

	def onEnterScene(self, who, oldScene, newScene):
		'''进入场景时
		'''
		if oldScene is newScene:
			return

	def onLeaveScene(self, who, oldScene, newScene):
		'''离开场景时
		'''
		if oldScene is newScene:
			return

	def createScene(self, sceneIdx):
		'''创建副本场景
		'''
		sceneObj = customActivity.createScene(self, sceneIdx)
		info = self.getSceneInfo(sceneIdx)
		sceneObj.landX = info.get("着陆点x", 0)
		sceneObj.landY = info.get("着陆点y", 0)
		return sceneObj

	def getInstanceScene(self, teamId, instanceType):
		'''根据队伍获取场景
		'''
		for sceneObj in self.getSceneListByType("instanceScene"):
			_teamId,_instanceType = getattr(sceneObj, "instanceInfo", (0,0))
			if teamId == _teamId and _instanceType == instanceType:
				return sceneObj
		return None

	def getSceneByRole(self, who, instanceType):
		'''根据队伍获取场景
		'''
		teamObj = who.getTeamObj()
		if not teamObj:
			return None
		return self.getInstanceScene(teamObj.id, instanceType)

	def removeInstanceScene(self, teamId, instanceType):
		'''删除场景
		'''
		sceneObj = self.getInstanceScene(teamId, instanceType)
		if sceneObj:
			self.removeScene(sceneObj)

	def cancelTeamMatch(self, who, teamObj):
		'''取消组队自动匹配
		'''
		targetArgs = team.platform.getTeamTarget(teamObj.id)
		if targetArgs.get("automatch", 0):
			team.platform.setTeamAutoMatch(teamObj.id, 0)
			team.platformservice.rpcChangeTeamTarget(who, teamObj)

	def handleTeamConfirm(self, who, teamObj, index):
		'''全队人员确认
		'''
		if teamObj.size != teamObj.inTeamSize:
			message.tips(who, "请先召回暂离队员才能进入副本")
			return False

		#每个队员等级必须全部满足
		minLevel = self.getInstanceData(index, "显示等级", 0)
		if who.level < minLevel:
			message.tips(who, "您的等级不足{}级".format(minLevel))
			return False

		lTemp = []
		for roleId in teamObj.getOnlineList():
			if roleId == who.id:
				continue
			roleObj = getRole(roleId)
			if roleObj:
				if roleObj.level < minLevel:
					lTemp.append("#C01{}#n".format(roleObj.name))
		if lTemp:
			message.tips(who, "队员{}等级不足{}级".format("、".join(lTemp), minLevel))
			return False

		#难度大于2，要每个队员弹出确认框
		difficulty = self.getInstanceData(index, "难度", 0)
		if difficulty < 2:
			return True
		message.tips(who, "队员确认中，请稍等")
		instanceName = self.getInstanceData(index, "名字", "")
		msg = "#C02{}#n副本为#C02精英副本#n，难度较大，请确定做好充足准备进入。\nQ取消#30\nQ确定".format(instanceName)
		leader = teamObj.leader
		teamId = teamObj.id

		dJobs = {}
		lTeamConfirm = getattr(teamObj, "teamInstanceConfirm", [])
		for pid in teamObj.getInTeamList():
			if pid == leader:	#队长不用确认
				continue
			if pid in lTeamConfirm:#已经确认过不用再确认
				continue
			dJobs[pid] = myGreenlet.cGreenlet.spawn(message.confirmBox, pid, msg)
		gevent.joinall(dJobs.values(),None,True)

		res = True
		for pid,job in dJobs.iteritems():
			if not job.value:
				res = False
				continue
			obj = getRole(pid)
			if not obj:
				res = False
			elif not obj.getTeamObj():
				res = False
			elif obj.getTeamObj().id != teamId:
				res = False
			elif not pid in teamObj.getInTeamList():
				res = False
			if job.value != 2:
				message.teamMessage(teamId, "#C02{}#n#C09拒绝#n进入#C02{}#n副本".format(obj.name, instanceName))
				res = False
				continue
			message.teamMessage(teamId, "#C02{}#n确认进入#C02{}#n副本".format(obj.name, instanceName))
			lTeamConfirm.append(pid)
		setattr(teamObj, "teamInstanceConfirm", lTeamConfirm)

		if teamObj.size != teamObj.inTeamSize:
			message.tips(who, "请先召回暂离队员才能进入副本")
			return False

		return res

	def leaveTeam(self, teamObj, pid):
		'''离开队伍
		'''
		lTeamConfirm = getattr(teamObj, "teamInstanceConfirm", [])
		if pid in lTeamConfirm:
			lTeamConfirm.remove(pid)
			setattr(teamObj, "teamInstanceConfirm", lTeamConfirm)

	def tranferRealScene(self, who):
		'''传回实场景
		'''
		if getattr(who, "instanceOffLine", False):
			return
		sceneObj = who.sceneObj
		if sceneObj.isTempScene():
			#统一传回副本NPC
			npcObj = npc.getNpcByIdx(10212)
			if npcObj:
				sceneId, x, y = npcObj.sceneId, npcObj.x, npcObj.y
			else:
				sceneId, x, y = who.getLastRealPos()
			scene.doTransfer(who, sceneId, x, y)

	def roleOnLine(self, who):
		if hasattr(who, "instanceOffLine"):
			delattr(who, "instanceOffLine")

	def roleOffLine(self, who):
		'''离线处理
		'''
		for taskType, taskParentId in gdAllInstanceTaskParentId.iteritems():
			taskObj = task.hasTask(who, taskParentId)
			if taskObj:
				taskObj.onLeave(who.id, LEAVE_TASK_OFFLINE)
		who.instanceOffLine = True

	def addInstanceReward(self, who, taskId):
		'''判断是否有正常奖励,每天第一次完成有奖励,以后只奖励侠义值
		'''
		normalReward = True
		instanceReward = who.day.fetch("instanceReward", [])
		if taskId in instanceReward:
			normalReward = False
		else:
			instanceReward.append(taskId)
			who.day.set("instanceReward", instanceReward)
		return normalReward


#================================================

def getActivity():
	return activity.getActivity("instance")


def rpcActInstanceEnter(who, reqMsg):
	'''进入副本
	'''
	if who.inWar():
		return
	iSelect = reqMsg.iValue
	actObj = getActivity()
	actObj.enterInstance(who, iSelect)

	
from common import *
import message
import activity
import scene
import sceneData
import myGreenlet
import gevent
import team.platform
import team.platformservice
from team.defines import *
import role
import npc
import task.bamboo
import task.magicWave
import activity.center

#副本类型
BAMBOO_INSTANCE = 1 #竹林除妖 
MAGIC_WAVE_INSTANCE = 2	#幻波池

gdAllInstanceTaskParentId = {
	BAMBOO_INSTANCE:task.bamboo.TASK_INSTANCE_PARENT_ID,	#竹林除妖
	MAGIC_WAVE_INSTANCE:task.magicWave.MAGIC_WAVE_TASK_PARENT_ID,#幻波池
}


#副本任务
gdAInstanceTask = {
	BAMBOO_INSTANCE:task.bamboo.giveBambooTask,	#竹林除妖
	MAGIC_WAVE_INSTANCE:task.magicWave.task.magicWave.giveMagicWaveTask,#幻波池
}

