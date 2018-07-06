# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 20301
	targetType = TASK_TARGET_TYPE_NPC_MULTI
	icon = 1
	title = '''五岳帝君'''
	intro = '''依次通过$BOSS共五位帝君的测试'''
	detail = '''山川林泽皆有神灵，五岳则为其中之首。每逢良辰吉日，则五岳帝君分别化成人形，于人间观赏游玩。修行者若能找到泰山君、衡山君、华山君、嵩山君、恒山君这五位帝君的踪迹，并通过他们给予的测试，则能获得丰厚奖赏！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''

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

	configInfo = {
		"生成路径":"fiveBoss",
	}

	bossDescInfo = {
		1002:{"完成":"#C04泰山君#n","未完成":"#C02泰山君#n"},
		1003:{"完成":"#C04衡山君#n","未完成":"#C02衡山君#n"},
		1004:{"完成":"#C04华山君#n","未完成":"#C02华山君#n"},
		1005:{"完成":"#C04嵩山君#n","未完成":"#C02嵩山君#n"},
		1006:{"完成":"#C04恒山君#n","未完成":"#C02恒山君#n"},
	}
#导表结束

	def getTargetNpc(self):
		'''目标npc
		'''
		who = getRole(self.ownerId)
		if who:
			actObj = activity.fiveBoss.getActivity()
			doneList = who.week.fetch("fiveBoss",[])
			for bossIdx in xrange(1002,1007):
				if bossIdx not in doneList:
					npcObj = actObj.getNpcByIdx(bossIdx)
					if npcObj:
						return npcObj
		return None

	def goAhead(self, who):
		'''前往
		'''
		wday = getDatePart()["wday"]
		if wday != 7:
			message.tips(who,"活动时间已过，自动删除任务")
			task.removeTask(who,self.id)
			return

		customTask.goAhead(self, who)

	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 0

	def isValid(self):
		'''是否有效
		'''
		wday = getDatePart()["wday"]
		if wday != 7:
			return 0

		return customTask.isValid(self)

	def transString(self, content, pid=0):
		who = None
		if pid:
			who = getRole(pid)
			
		if who:
			if "$BOSS" in content:
				content = content.replace("$BOSS",self.getBossDesc(who))

		return customTask.transString(self, content, pid)

	def getBossDesc(self, who):
		lst = []
		doneList = who.week.fetch("fiveBoss",[])
		for bossIdx in xrange(1002,1007):
			if bossIdx in doneList:
				desc = self.bossDescInfo[bossIdx]["完成"]
			else:
				desc = self.bossDescInfo[bossIdx]["未完成"]
			lst.append(desc)
		return "，".join(lst)

from common import *
import activity.fiveBoss
import task
import message