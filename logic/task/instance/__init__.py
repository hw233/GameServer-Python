# -*- coding: utf-8 -*-

#副本任务
from task.defines import *
from task.object import TeamTask as customTask


class InstanceTask(customTask):
	'''副本任务
	'''
	def onBorn(self, who, npcObj, **kwargs):#override
		self.initInstanceTask()	
		customTask.onBorn(self, who, npcObj, **kwargs)

	def initInstanceTask(self):
		'''设置副本任务类型-最后一个任务编号
		'''
		# self.instanceTaskType = 0	#副本任务类型
		# self.lastTaskId = 0		#最后一个任务编号
		raise NotImplementedError,'请在子类实现'

	def getInstanceTaskType(self):
		return self.instanceTaskType

	def customEvent(self, who, npcObj, eventName, *args):#override
		m = re.match("LND(\S+)", eventName)#
		if m:
			subEvent = m.group(1)
			npcObj = self.getLastNewNpc()
			if npcObj:
				self.doScript(who, npcObj, "TD{}".format(subEvent))

		m = re.match("INSTORY(\S+)", eventName)#副本特别的剧情
		if m:
			subEvent = m.group(1)
			npcObj = self.getLastNewNpc()
			if npcObj:
				self.doScript(who, npcObj, "STORY{}".format(subEvent))
				delattr(self, "storyNpcId")	#只播放剧情，不需要完成任务
				self.instanceStoryId = int(subEvent)

	def reward(self, who, rwdIdx, npcObj=None):#override
		'''每天第一次完成有奖励,以后只奖励侠义值
		'''
		normalReward = True
		actObj = activity.instance.getActivity()
		normalReward = actObj.addInstanceReward(who, self.id)
		if normalReward:#正常奖励
			customTask.reward(self, who, rwdIdx, npcObj)
		else:#只奖励侠义值
			self.rewardHelpPoint(who)
			#who.addHelpPoint(1, "instance_{}".format(self.id))

	def rewardHelpPoint(self,who):
		#每天通关某个副本之后再次挑战时，如果玩家等级高于对应副本上限10级
		#并且队伍中有队员在副本的等级范围内，则每场战斗可获得2点侠义值
		actObj = activity.instance.getActivity()
		minLevel = actObj.getInstanceData(self.instanceTaskType, "显示等级", 0)
		maxLevel = actObj.getInstanceData(self.instanceTaskType, "最大等级", 0)
		if who.level < maxLevel+10:
			return
		teamObj = who.getTeamObj()
		if not teamObj:
			return
		teamList = teamObj.getInTeamList()
		rewardTag = False
		for pid in teamList:
			target=getRole(pid)
			if minLevel <= target.level <= maxLevel:
				who.addHelpPoint(2, "instance_{}".format(self.id))
				break			

	def goAhead(self, who):#override
		'''前往
		'''
		actObj = activity.instance.getActivity()
		instanceSceneObj = actObj.getSceneByRole(who, self.instanceTaskType)
		sceneObj = who.sceneObj
		if instanceSceneObj and sceneObj and instanceSceneObj.id != sceneObj.id:
			teamObj = who.inTeam()
			if teamObj:
				actObj.cancelTeamMatch(who, teamObj)
			pid = who.id
			res = actObj.handleTeamConfirm(who, teamObj, self.instanceTaskType)
			if not res:
				return
			who = getRole(pid)
			if not who:
				return
		customTask.goAhead(self, who)

	def onLeave(self, pid, mode):
		customTask.onLeave(self, pid, mode)
		#退出队伍踢出场景
		actObj = activity.instance.getActivity()
		who = getRole(pid)
		if who:
			actObj.tranferRealScene(who)

		if self.team:
			actObj.leaveTeam(self.team, pid)
		#所有人退出
		if not self.roleList and self.team:
			teamId = self.team.id
			actObj.removeInstanceScene(teamId, self.instanceTaskType)

	def createNpc(self, npcIdx, who=None):#override
		'''创建Npc
		'''
		npcObj = customTask.createNpc(self, npcIdx, who)
		#npc场景ID设置为虚拟场景ID
		actObj = activity.instance.getActivity()
		sceneObj = actObj.getSceneByRole(who, self.instanceTaskType)
		if sceneObj:
			npcObj.sceneId = sceneObj.id
		return npcObj

	def transCode(self, code, _type="", who=None):#override
		if who and isinstance(code, str):
			if "BALV" in code:	#min(ALV, "最大等级")
				teamObj = who.inTeam()
				if teamObj:
					level = teamObj.getAvgLV()
				else:
					level = who.level
				actObj = activity.instance.getActivity()
				maxLv = actObj.getInstanceData(self.instanceTaskType, "最大等级", level)
				code = code.replace("BALV", str(min(level, maxLv)))
				
		return customTask.transCode(self, code, _type, who)

	def onMissionDone(self, who, npcObj):
		if self.id == self.lastTaskId:
			#完成后把队伍踢出场景
			if self.team.isLeader(who.id):
				sceneId, x, y = who.getLastRealPos()
				scene.doTransfer(who, sceneId, x, y)
				actObj = activity.instance.getActivity()
				actObj.removeInstanceScene(self.team.id, self.instanceTaskType)

	def storySpecialDuel(self, who):
		'''特殊处理第一个任务剧情
		'''
		teamObj = who.inTeam()
		if teamObj and teamObj.isLeader(who.id):
			roleList = teamObj.getInTeamList()
		else:
			roleList = [who.id]

		for roleId in roleList:
			roleObj = getRole(roleId)
			if roleObj:
				roleObj.endPoint.rpcTaskStoryStop(self.id)

from common import *
import activity.instance
import scene