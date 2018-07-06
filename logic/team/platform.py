# -*- coding: utf-8 -*-

class TeamTarget(object):
	def __init__(self, targetNo, subTarget=0):
		self.targetNo = targetNo
		self.subTarget = subTarget

		self.teamIdList = []
		self.playerIdList = []

	def getTeamIdList(self):
		return self.teamIdList

	def getPlayerIdList(self):
		return self.playerIdList

	def addTemaId(self, teamId):
		if teamId not in self.teamIdList:
			self.teamIdList.append(teamId)

	def removeTeamId(self, teamId):
		if teamId in self.teamIdList:
			self.teamIdList.remove(teamId)

	def addPlayerId(self, pid):
		if pid not in self.playerIdList:
			self.playerIdList.append(pid)

	def removePlayerId(self, pid):
		if pid in self.playerIdList:
			self.playerIdList.remove(pid)
	


class TeamPlatform(object):
	'''队伍平台
	'''
	def __init__(self):
		self.TeamTargetArgs = {}	#{teamId:{目标}}
		self.PlayerTargetArgs = {}	#{id:{目标}}
		self.PlayerTargetTemp = {}	#自动匹配加入队伍后，保存玩家目标，以便被踢出队伍后继续匹配
		self.initTargetObj()

	def initTargetObj(self):
		'''目标
		'''
		self.targetObj = {}
		for target, info in teamTargetData.gdData.iteritems():
			subTargetData = info.get("可选目标", {})
			if not subTargetData:
				self.targetObj[(target, 0)] = TeamTarget(target, 0)
				continue
			for subtarget,_ in subTargetData.iteritems():
				self.targetObj[(target, subtarget)] = TeamTarget(target, subtarget)

		#print self.targetObj


	def getTargetObj(self, target, subtarget=0):
		key = (target, subtarget)
		return self.targetObj.get(key, None)

	def printTarget(self):
		print self.TeamTargetArgs,self.PlayerTargetArgs,self.PlayerTargetTemp
		for key,obj in self.targetObj.iteritems():
			if obj.teamIdList and obj.playerIdList:
				print key, obj.teamIdList,"----",obj.playerIdList

	###############
	#队长
	def addTeamMatch(self, teamId, targetArgs):
		'''队伍加入匹配
		'''
		self.removeTeamMatch(teamId)
		target = targetArgs.get("target", 0)
		if not target:
			return
		self.TeamTargetArgs[teamId] = targetArgs
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if targetObj:
				targetObj.addTemaId(teamId)

	def getTeamTarget(self, teamId):
		return self.TeamTargetArgs.get(teamId, {})

	def getTeamAuto(self, teamId):
		return self.TeamTargetArgs.get(teamId, {}).get("automatch", 0)

	def setTeamAutoMatch(self, teamId, auto):
		'''自动匹配
		'''
		targetArgs = self.TeamTargetArgs.get(teamId, None)
		if not targetArgs:
			return
		targetArgs["automatch"] = auto

	def removeTeamMatch(self, teamId):
		'''删除匹配目标
		'''
		targetArgs = self.TeamTargetArgs.pop(teamId, None)
		if not targetArgs:
			return
		target = targetArgs.get("target", 0)
		if not target:
			return
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if targetObj:
				targetObj.removeTeamId(teamId)

	def teamSetQuickType(self, teamId, quickType):
		'''设置便捷组队方式
		'''
		targetArgs = self.TeamTargetArgs.get(teamId, None)
		if not targetArgs:
			return
		targetArgs["quickType"] = quickType

	def getTeamQuickType(self, teamId):
		'''获取便捷组队方式
		'''
		targetArgs = self.TeamTargetArgs.get(teamId, None)
		if not targetArgs:
			return 0
		return targetArgs.get("quickType", 0)

	###############
	#玩家
	def addPlayerMatch(self, who, targetArgs):
		'''玩家加入匹配
		'''
		self.removePlayerMatch(who)
		self.PlayerTargetTemp.pop(who.id, None)
		target = targetArgs.get("target", 0)
		if not target:
			return
		self.PlayerTargetArgs[who.id] = targetArgs
		if not who.eRemove.contain(self.roleRemoveEventHandler):
			who.eRemove+=self.roleRemoveEventHandler	#关注玩家remove事件

		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if targetObj:
				targetObj.addPlayerId(who.id)

	def transPlayerTarget(self, who):
		'''自动匹配加入队伍后，临时保存玩家目标，以便被踢出队伍后继续匹配
		'''
		targetArgs = self.PlayerTargetArgs.pop(who.id, None)
		if targetArgs:
			self.PlayerTargetTemp[who.id] = targetArgs

	def getPlayerTargetTemp(self, who):
		return self.PlayerTargetTemp.get(who.id, None)

	def setPlayerAutoMatch(self, who, auto):
		'''玩家设置自动匹配
		'''
		targetArgs = self.PlayerTargetArgs.get(who.id, None)
		if not targetArgs:
			return
		targetArgs["automatch"] = auto

	def removePlayerMatch(self, who):
		'''删除玩家匹配目标
		'''
		targetArgs = self.PlayerTargetArgs.pop(who.id, None)
		if not targetArgs:
			return
		if who.eRemove.contain(self.roleRemoveEventHandler):
			who.eRemove-=self.roleRemoveEventHandler
		target = targetArgs.get("target", 0)
		if not target:
			return

		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if targetObj:
				targetObj.removePlayerId(who.id)


	def roleRemoveEventHandler(self, who):
		'''玩家remove事件
		'''
		self.removePlayerMatch(who)
		self.PlayerTargetTemp.pop(who.id, None)

	def getPlayerTarget(self, who):
		return self.PlayerTargetArgs.get(who.id, {})

	def getPlayerAuto(self, who):
		return self.PlayerTargetArgs.get(who.id, {}).get("automatch", 0)

	def playerSetQuickType(self, who, quickType):
		'''便捷组队方式
		'''
		targetArgs = self.PlayerTargetArgs.get(who.id, None)
		if not targetArgs:
			return
		targetArgs["quickType"] = quickType

	##################
	def getMatchPlayerCnt(self, who):
		'''获取目标相同的玩家数量
		'''
		targetArgs = self.PlayerTargetArgs.get(who.id, None)
		if not targetArgs:
			return 0
		target = targetArgs.get("target", 0)
		if not target:
			return 0
		playerIdList = []
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if not targetObj:
				continue
			pidList = targetObj.getPlayerIdList()
			for pid in pidList:
				if pid in playerIdList:
					continue
				tempTarget = self.PlayerTargetArgs.get(pid, {})
				if not tempTarget.get("automatch", 0):
					continue
				playerIdList.append(pid)
		return len(playerIdList)

	def getMatchPlayer(self, teamId, auto=False):
		'''获取正在匹配的玩家
		'''
		targetArgs = self.TeamTargetArgs.get(teamId, None)
		if not targetArgs:
			return []
		target = targetArgs.get("target", 0)
		if not target:
			return []

		playerIdList = []
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if not targetObj:
				continue
			pidList = targetObj.getPlayerIdList()
			for pid in pidList:
				if pid in playerIdList:
					continue
				if auto:
					tempTarget = self.PlayerTargetArgs.get(pid, {})
					if not tempTarget.get("automatch", 0):
						continue
				playerIdList.append(pid)
		return playerIdList

	def getMatchTeamCnt(self, teamId, *excludeList):
		'''获取目标相同的队伍数量
		'''
		targetArgs = self.TeamTargetArgs.get(teamId, None)
		if not targetArgs:
			return 0
		target = targetArgs.get("target", 0)
		if not target:
			return 0
		teamIdList = []
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if not targetObj:
				continue
			tIdList = targetObj.getTeamIdList()
			for teamId in tIdList:
				if teamId in excludeList:
					continue
				if teamId in teamIdList:
					continue
				if not team.getTeam(teamId):
					continue
				#tempTarget = self.TeamTargetArgs.get(teamId, {})
				# if not tempTarget.get("automatch", 0):
				# 	continue
				teamIdList.append(teamId)
		return len(teamIdList)


	def getMatchTeam(self, who, auto=False, *excludeList):
		'''获取正在匹配的队伍
		'''
		targetArgs = self.PlayerTargetArgs.get(who.id, None)
		if not targetArgs:
			return []
		target = targetArgs.get("target", 0)
		if not target:
			return []

		teamIdList = []
		subtargetList = targetArgs.get("subtarget", [0])
		for subtarget in subtargetList:
			targetObj = self.getTargetObj(target, subtarget)
			if not targetObj:
				continue
			tIdList = targetObj.getTeamIdList()
			for teamId in tIdList:
				if teamId in excludeList:
					continue
				if teamId in teamIdList:
					continue
				if not team.getTeam(teamId):
					continue
				if auto:
					tempTarget = self.TeamTargetArgs.get(teamId, {})
					if not tempTarget.get("automatch", 0):
						continue
				teamIdList.append(teamId)
		return teamIdList


import teamTargetData

if 'mainService' in SYS_ARGV:
	if 'gTeamPlatformObj' not in globals():
		gTeamPlatformObj = TeamPlatform()

def TeamPlatformObj():
	return gTeamPlatformObj

#设置匹配目标
def addTeamMatch(teamId, targetArgs):
	gTeamPlatformObj.addTeamMatch(teamId, targetArgs)

def addPlayerMatch(who, targetArgs):
	gTeamPlatformObj.addPlayerMatch(who, targetArgs)

#自动/取消匹配 1：自动匹配 0：取消匹配
def setTeamAutoMatch(teamId, auto):
	gTeamPlatformObj.setTeamAutoMatch(teamId, auto)

def setPlayerAutoMatch(who, auto):
	gTeamPlatformObj.setPlayerAutoMatch(who, auto)

#队伍解散
def teamRelease(teamId):
	gTeamPlatformObj.removeTeamMatch(teamId)

#退出队伍,队伍目标变为玩家目标,取消自动匹配状态
def teamQuit(who, teamId):
	temp = gTeamPlatformObj.getTeamTarget(teamId)
	if temp:
		targetArgs = {}
		targetArgs["target"] = temp.get("target", 0)
		targetArgs["subtarget"] = temp.get("subtarget", [])
		gTeamPlatformObj.addPlayerMatch(who, targetArgs)
		gTeamPlatformObj.setPlayerAutoMatch(who, 0)

#删除玩家状态目标
def removePlayerMatch(who):
	gTeamPlatformObj.removePlayerMatch(who)

def transPlayerTarget(who):
	gTeamPlatformObj.transPlayerTarget(who)

#获取匹配的玩家
def getMatchPlayer(who, teamObj):
	return gTeamPlatformObj.getMatchPlayer(teamObj.id)

def getAutoMatchPlayer(who, teamObj):
	matchList = gTeamPlatformObj.getMatchPlayer(teamObj.id, True)
	targetArgs = gTeamPlatformObj.getTeamTarget(teamObj.id)
	target = targetArgs.get("target", 0)
	func = gTargetMatchPlayerRule.get(target, None)
	if func:
		matchList = func(who, teamObj, matchList)
	return matchList

#获取匹配的队伍
def getMatchTeam(who, *excludeList):
	return gTeamPlatformObj.getMatchTeam(who)

def getAutoMatchTeam(who, *excludeList):
	matchList = gTeamPlatformObj.getMatchTeam(who, True, *excludeList)
	targetArgs = gTeamPlatformObj.getPlayerTarget(who)
	target = targetArgs.get("target", 0)
	func = gTargetMatchTeamRule.get(target, None)
	if func:
		matchList = func(who, matchList)
	return matchList

#获取队伍的目标
def getTeamTarget(teamId):
	return gTeamPlatformObj.getTeamTarget(teamId)

def getPlayerTarget(who):
	return gTeamPlatformObj.getPlayerTarget(who)


#================================
#便捷组队任务
DEMON_TASK_NPC = 1 	#降魔任务
INSTANCE_TASK_NPC = 101#副本NPC



def demonTaskPlayerRule(who, teamObj, matchList, start=0, end=3, *args):
	'''	优先匹配在线队员，若无则匹配离线队员
		根据队长职业，在剩余5个职业（除队长职业）外，随机匹配4个队员，每个队员职业都不一样
		若上述条件不满足（如佛门职业已经没人），则随机匹配一个非队长职业的职业,（若无则全随机）
		匹配的队员的等级，第2、3、4号位置为队长等级的±5级内，第5号位为低于队长10级的任意等级玩家
		上述条件不满足，则2、3、4号位置匹配范围扩大到±15级（若无则全随机），5号位置全随机
	'''
	resultPid = []
	teamMemSchool = []	#当前队员的职业
	for pid in teamObj.memberList:
		targetObj = getRole(pid)
		if not targetObj:
			continue
		teamMemSchool.append(targetObj.school)

	for times in xrange(start, end):
		flag = False
		for pid in matchList:
			if pid in resultPid:
				continue
			# if pid in teamObj.joinList:
			# 	continue
			if pid in teamObj.memberList:
				continue
			targetObj = getRole(pid)
			if not targetObj:
				continue
			#职业
			if times == 0 and targetObj.school in teamMemSchool:
				continue

			#匹配非队长职业
			if times < 2 and targetObj.school == who.school:
				continue

			#等级
			if teamObj.size + len(resultPid) < 5:	#第2、3、4号位置
				if times < 2 and targetObj.level > who.level+5+10*times or targetObj.level < min(0, who.level-5-10*times):
					continue
			else:	#第5号位
				if times == 0 and targetObj.level > min(0, who.level - 10):
					continue

			resultPid.append(pid)
			teamMemSchool.append(targetObj.school)
			if len(resultPid) >= len(matchList):
				flag = True
				break
			if teamObj.size + len(resultPid) >= MEMBER_LIMIT:
				break
		if flag:
			break

	return resultPid

def demonTaskTeamRule(who, matchTeamId):
	'''	降魔任务 玩家找到最优的队伍
		相当于玩家是否符合队伍的要求
	'''
	for i in xrange(3):
		for teamId in matchTeamId:
			teamObj = team.getTeam(teamId)
			if not teamObj:
				continue
			if teamObj.size >= MEMBER_LIMIT:
				continue
			# if who.id in teamObj.joinList:
			# 	continue
			if who.id in teamObj.memberList:
				continue
			# if len(teamObj.joinList) >= JOIN_LIMIT:
			# 	continue
			leaderObj = getRole(teamObj.leader)
			if not leaderObj:
				continue
			l = demonTaskPlayerRule(leaderObj, teamObj, [who.id], i, i+1)
			if l:
				return [teamId]
	return []

#具体任务匹配要求
gTargetMatchPlayerRule = {
	DEMON_TASK_NPC:demonTaskPlayerRule,
}


gTargetMatchTeamRule = {
	DEMON_TASK_NPC:demonTaskTeamRule,
}


from common import *
from team.defines import *
import team
