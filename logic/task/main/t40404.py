# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·惨剧'''
	intro = '''去到黑河村时，发现村民们已经变成了$target'''
	detail = '''去到黑河村时，发现村民们已经变成了$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2006,NI2007,NI2008,NI2009,E(2006,2010),E(2007,2011),E(2008,2012),E(2009,2013)'''
#导表结束
	def setupWar(self, warObj, who, npcObj):
		self.createMonsterList(who, npcObj)
		warObj.addFunc("onEndRound",self.onEndRound)
		
	def createMonsterList(self, who, npcObj):
		self.monsterList = []
		
		fightIdx = 2490
		fightList = self.getFightInfo(fightIdx)
		ableData = self.getAbleInfo()
		lineupData = self.getLineupInfo()
		monsterList = war.warctrl.createMonsterList(who, fightIdx, fightList, ableData, lineupData, self, npcObj)
		for lst in monsterList.itervalues():
			for monsterObj in lst:
				self.monsterList.append(monsterObj)
	
	def onEndRound(self, warObj):
		if 0 != warObj.bout % 3:
			return
		if len(warObj.teamList[TEAM_SIDE_2]) >= len(POS_MONSTER):
			return

		monsterList = self.monsterList
		monsterObj = monsterList[rand(len(monsterList))]
		monsterW = warObj.addMonsterFight(monsterObj, TEAM_SIDE_2)
		warObj.rpcAddWarrior(monsterW, None, True)
		warObj.rpcWarAllBuff(monsterW)
		warObj.say(monsterW, self.getText(7004))

from common import *
from war.defines import *
import perform
import message
import template
import war.warctrl