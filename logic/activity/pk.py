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
		1329:'''对方已下线''',
		1357:'''对方已进入战斗，无法切磋''',
		1358:'''对方当前无法接受切磋''',
		1359:'''队员无法切磋''',
		1360:'''无法与队员切磋''',
		1369:'''切磋需要到#C02天墉城#n擂台''',
		1370:'''切磋双方需要#C02等级≥20#n''',
		1371:'''挑战#C02$targetName#n成功#15''',
		1372:'''防守#C02$targetName#n失败#29''',
		1373:'''挑战#C02$targetName#n失败#60''',
		1374:'''防守#C02$targetName#n成功#42''',
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
		"场景":1130,
		"上":41,
		"下":23,
		"左":100,
		"右":137,
	}
#导表结束

	def checkCondition(self, who, target):
		'''检查条件
		'''
		if target.inWar():
			self.doScript(who, None, "TP1357")
			return
		if who.inTeam() and not who.getTeamObj().isLeader(who.id):
			self.doScript(who, None, "TP1359")
			return False
		if target.inTeam() and not target.getTeamObj().isLeader(target.id):
			self.doScript(who, None, "TP1360")
			return False
		if not self.isInPkArea(who) or not self.isInPkArea(target):
			self.doScript(who, None, "TP1369")
			return False
		if target.level < 20 or who.level < 20 :
			self.doScript(who, None, "TP1370")
			return False
		return True

	def isInPkArea(self, who):
		'''是否在pk区
		'''
		areaInfo = self.configInfo
		sceneId = areaInfo["场景"]
		areaUp = areaInfo["上"]
		areaDown = areaInfo["下"]
		areaLeft = areaInfo["左"]
		areaRight = areaInfo["右"]
		if sceneId != who.sceneId:
			return False
		if not (areaLeft < who.x < areaRight) or not (areaDown < who.y < areaUp):
			return False
		ringHighly = areaUp - areaDown
		ringWidth  = areaRight - areaLeft
		ringCenterWhoX = abs(who.x - ((ringWidth) / 2 + areaLeft))
		ringCenterWhoY = abs(who.y - ((ringHighly) / 2 + areaDown))
		if (ringCenterWhoX * ringHighly / 2) + (ringCenterWhoY * ringWidth / 2) > (ringHighly * ringWidth / 4):
			return False
		return True

	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利
		'''	
		side = warObj.winner
		leaderId = warObj.teamInfoList[side]["leaderId"]
		who = getRole(leaderId)
		if not who:
			return
		who.pkTargetId = warObj.teamInfoList[side^1]["leaderId"]
		if side == TEAM_SIDE_1:  #挑战成功
			self.doScript(who, None, "TP1371")
		else:
			self.doScript(who, None, "TP1374")
		del who.pkTargetId

	def warFail(self, warObj, npcObj, warriorList):
		'''战斗失败时
		'''
		side = warObj.winner^1
		leaderId = warObj.teamInfoList[side]["leaderId"]
		who = getRole(leaderId)
		if not who:
			return
		who.pkTargetId = warObj.teamInfoList[side^1]["leaderId"]
		if side == TEAM_SIDE_1:  #挑战失败
			self.doScript(who, None, "TP1373")
		else:
			self.doScript(who, None, "TP1372")	
		del who.pkTargetId
		
	def setupWar(self, warObj, who, npcObj):
		'''战斗设置
		'''
		warObj.noLost = True

	def transString(self, content, pid=0):
		who = None
		if pid:
			who = getRole(pid)

		if who:
			if "$targetName" in content and hasattr(who,"pkTargetId"):
				target = getRole(who.pkTargetId)
				if target:
					content = content.replace("$targetName", target.name)

		return customActivity.transString(self, content, pid)

def getActivity():
	return activity.getActivity("pk")

def rpcPk(who, reqMsg):
	'''申请pk
	'''
	if who.inEscort():
		message.tips(who, "运镖中不能切磋")
		return
	if who.inWar():
		message.tips(who,"战斗中怎么PK，是否有BUG?")
		return

	actObj = activity.getActivity("pk")
	target = getRole(reqMsg.iValue)	
	if not target:
		actObj.doScript(who, None, "TP1329")
		return
	if target.inEscort():
		message.tips(who, "对方运镖中不能切磋")
		return
	if target.inStory():
		message.tips(who, "对方播放剧情中不能切磋")
		return
	if getattr(target, "enterCollect", 0):#玩家在收集玩法内不能pk
		message.tips(who, "对方当前无法接受切磋")
		return
	if not actObj.checkCondition(who,target):
		return
	warObj = war.warctrl.createPKWar(who,target,actObj)

from common import *
from war.defines import *
import message
import activity
import war.warctrl
import message