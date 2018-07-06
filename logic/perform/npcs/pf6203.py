# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6203
	name = "护卫何在"
	targetType = PERFORM_TARGET_FRIEND
	configInfo = {
		"战斗编号":2001,
	}
#导表结束

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		warObj = att.war
		gameObj = warObj.game
		if not hasattr(gameObj, "getMonsterListByFightIdx"): # 不能直接使用，需要在玩法中使用
			return
		monsterList = gameObj.getMonsterListByFightIdx(self.configInfo["战斗编号"])
		if not monsterList:
			return
		
		posList = []
		side = att.side
		for pos in xrange(1, 11):
			if pos not in warObj.teamList[side]:
				posList.append(pos)
				
		if not posList:
			return
		
		posList.sort()
		for pos in posList:
			monsterObj = monsterList[rand(len(monsterList))]
			monsterObj.pos = pos
			monsterW = warObj.addMonsterFight(monsterObj, side)
			warObj.rpcAddWarrior(monsterW, None, True)
			warObj.rpcWarAllBuff(monsterW)
	
# 	def getMonsterList(self, gameObj):
# 		if not hasattr(self, "monsterList"):
# 			fightIdx = self.configInfo["战斗编号"]
# 			fightList = gameObj.fightInfo[fightIdx]
# 			ableInfo = gameObj.ableInfo
# 			monsterList = war.warctrl.createMonsterList(who, fightIdx, fightList, ableData, lineupData, gameObj, npcObj)
	
	
from common import *
import war.warctrl
