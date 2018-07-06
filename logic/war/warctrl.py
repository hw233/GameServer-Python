# -*- coding: utf-8 -*-

#===============================================================================
# 普通战斗(玩家打怪物)
#===============================================================================
def createCommonWar(who, fightIdx=0, fightList=None, ableData=None, lineupData=None, gameObj=None, npcObj=None):
	'''创建普通战斗
	'''
	if who.inWar():
		return None

	monsterList = {}
	if gameObj and hasattr(gameObj, "customCreateMonsterList"):
		monsterList = gameObj.customCreateMonsterList(who, fightIdx, fightList, ableData, lineupData, npcObj)
	if not monsterList:
		monsterList = createMonsterList(who, fightIdx, fightList, ableData, lineupData, gameObj, npcObj)
	
	warObj = None
	if hasattr(gameObj, "newWar"):
		warObj = gameObj.newWar(who, fightIdx)
	if not warObj:
		warObj = war.object.War(WAR_COMMON)
	
	warObj.fightIdx = fightIdx
	warObj.gameNpc = npcObj.this() if npcObj else None
	warObj.game = gameObj
	
	if hasattr(gameObj, "setupWar"):
		gameObj.setupWar(warObj, who, npcObj)
	if not warObj.onWarEnd:
		warObj.onWarEnd = onWarEnd
	
	# 玩家
	addRoleFight(warObj, who, TEAM_SIDE_1)
	
	# 处理怪物
	monsterCnt = 0
	for monsterType in (MONSTER_TYPE_BOSS, MONSTER_TYPE_NORMAL, MONSTER_TYPE_FRIEND):
		for monsterObj in monsterList.get(monsterType, []):
			side = TEAM_SIDE_2
			if monsterType == MONSTER_TYPE_FRIEND:  # 友军
				side = TEAM_SIDE_1
			elif monsterType == MONSTER_TYPE_BOSS: # 主怪
				monsterCnt += 1
				
				#阵法、阵眼
				lineupObj = monsterObj.getLineupObj()
				if lineupObj:
					warObj.setLineup(lineupObj, side)
					eyeObj = lineupObj.getEyeObj()
					if eyeObj:
						warObj.addLineupEyeFight(eyeObj, side)

			else:  # 普通怪
				monsterCnt += 1

			warObj.addMonsterFight(monsterObj, side)

	warObj.monsterCnt = monsterCnt  # 怪物数量，用于除妖卫道任务
	warObj.start()
	return warObj

def addRoleFight(warObj, who, side):
	'''玩家进入战斗
	'''
	# 阵法、阵眼
	lineupObj = who.buddyCtn.getCurrentLineup()
	if lineupObj:
		warObj.setLineup(lineupObj, side)
		eyeObj = lineupObj.getEyeObj()
		if eyeObj:
			warObj.addLineupEyeFight(eyeObj, side)
	
	buddyCount = 4 # 最大伙伴出战数
	buddyList = list(who.buddyCtn.getCurrentBuddyList())
	if who.inTeam():
		teamObj = who.getTeamObj()
		if teamObj.isLeader(who.id):
			warObj.addRoleFight(who, side)
			buddyLen = len(buddyList)
			for idx,pid in enumerate(teamObj.memberList):
				if pid in teamObj.getInTeamList():
					if pid == who.id:
						continue
					memberObj = getRole(pid)
					warObj.addRoleFight(memberObj, side)
				elif idx-1 < buddyLen:
					warObj.addBuddyFight(who.warrior, buddyList[idx-1])
			buddyCount = team.defines.MEMBER_LIMIT - len(teamObj.memberList)
		else:
			teamObj.setLeave(who)
			warObj.addRoleFight(who, side)
	else:
		warObj.addRoleFight(who, side)
		
	if buddyCount:
		for buddyObj in buddyList[4-buddyCount:]:
			warObj.addBuddyFight(who.warrior, buddyObj)

def createMonsterList(who, fightIdx, fightList, ableData, lineupData, gameObj=None, npcObj=None):
	'''创建怪物列表
	'''
	monsterList = {
		MONSTER_TYPE_NORMAL: [], # 普通怪
		MONSTER_TYPE_BOSS: [], # 主怪
		MONSTER_TYPE_FRIEND: [], # 友军怪
	}
	
	for idx, fightInfo in enumerate(fightList):
		fightInfo = copy.deepcopy(fightInfo)
		if hasattr(gameObj, "transFightInfo"):
			fightInfo = gameObj.transFightInfo(who, fightIdx, fightInfo, npcObj)
		fightInfo = transFightInfo(who, fightIdx, fightInfo, npcObj)
		
		ableInfo = copy.deepcopy(ableData[fightInfo["能力编号"]])
		if hasattr(gameObj, "transAbleInfo"):
			ableInfo = gameObj.transAbleInfo(who, fightIdx, ableInfo, npcObj)
		ableInfo = transAbleInfo(who, fightIdx, ableInfo, npcObj)
		
		monsterType = fightInfo["类型"]
		monsterObj = None
		for i in xrange(int(fightInfo["数量"])):
			monsterObj = war.monster.newMonster(fightInfo, ableInfo)
			if fightInfo.get("站位"):
				monsterObj.pos = fightInfo["站位"][i]
			monsterObj.monsterIdx = idx
			monsterObj.monsterType = monsterType

			monsterList[monsterType].append(monsterObj)
		
		if fightInfo.get("阵法编号") and monsterObj:
			lineupInfo = lineupData[fightInfo["阵法编号"]]
			lineupObj = createMonsterLineup(monsterObj, lineupInfo)
			monsterObj.setLineupObj(lineupObj)
	
	for monsterType, lst in monsterList.items():
		monsterList[monsterType] = shuffleList(lst)
	return monsterList
			
def transFightInfo(who, fightIdx, info, npcObj=None):
	'''转化怪物战斗信息
	'''
	shape, shapeParts = template.transShapeStr(info["造型"], who, npcObj)
	info["造型"] = shape
	info["造型部位"] = shapeParts
	
	if info.get("染色"):
		colors = template.transColorsStr(info["染色"], who, npcObj)
		info["染色"] = colors
		
	name = info["名称"]
# 	if "$pet" in name:
# 		name = name.replace("$pet", pet.getPetName(info["宠物"]))
	if "$npc" in name:
		name = name.replace("$npc", npcObj.name)
	info["名称"] = name
		
	ableId = info["能力编号"]
	if isinstance(ableId, str):
		info["能力编号"] = int(ableId)
	
	num = info["数量"]
	if isinstance(num, str):
		info["数量"] = int(num)
		
	import war.ai
	if info.get("AI集"):
		aiSetList = []
		for desc in info["AI集"].split(","):
			aiSetList.append(war.ai.AISetTypeDesc[desc])
		info["AI集"] = aiSetList
		
	import perform.defines
	if info.get("五行"):
		fiveEl = perform.defines.getFiveElVal(info["五行"])
		info["五行"] = fiveEl
		
	if info.get("精通技能"):
		info["精通技能"] = [info["精通技能"]]
	
	return info

def transAbleInfo(who, fightIdx, ableInfo, npcObj=None):
	'''转化怪物能力信息
	'''
	level = ableInfo["等级"]
	if isinstance(level, str):
		level = template.transLevelStr(who, level, npcObj=None)
		level = int(eval(level))
	ableInfo["等级"] = level
	
	return transByMonsterBase(level, ableInfo)

def transByMonsterBase(level, ableInfo):
	'''根据怪物基础能力数据转换数据
	'''
	baseInfo = monsterBase.getBaseAbleInfo(level)
	for attr,baseVal in baseInfo.iteritems():
		if attr in ableInfo:
			val = ableInfo[attr]
			val = val.replace("B", str(baseVal))
			ableInfo[attr] = int(eval(val))
	return ableInfo

def createMonsterLineup(monsterObj, info):
	'''创建怪物的阵法
	'''
	lineupObj = lineup.createLineup(info["阵法"])
	lineupObj.level = info["等级"]
	
	if info.get("阵眼"):
		eyeObj = lineup.createEyeByNo(info["阵眼"])
		eyeObj.level = monsterObj.level
		lineupObj.eyeObj = eyeObj

		if info.get("被动技能"):
			skillList = eyeObj.fetch("skillList", [])
			skillList = skillList[:1]
			skillList.extend(info["被动技能"])
			eyeObj.set("skillList", skillList)

	return lineupObj

# def createLineupEyeMonster(level, lineupObj):
# 	'''创建阵眼怪
# 	'''
# 	data = lineupData.getLineupEyeData(lineupObj.id)
# 	data = transByMonsterBase(level, copy.deepcopy(data))
# 	data["等级"]= level
# 	data["造型"]= int(data["造型"])
# 	monsterObj = war.monster.newMonster(data)
# 	return monsterObj

def onWarEnd(warObj):
	'''战斗结束时
	'''
	gameObj = warObj.game
	warObj.game = None

	npcObj = warObj.gameNpc
	warObj.gameNpc = None
	if npcObj and hasattr(npcObj, "onWarEnd"):
		npcObj.onWarEnd(warObj)
	
	if not gameObj:
		return
	
	gameObj.beforeWarEnd(warObj, npcObj)
	
	if warObj.type == WAR_PK:
		side = warObj.winner
		warWin(gameObj, warObj, npcObj, warObj.teamList[side].values())# 胜利
		warFail(gameObj, warObj, npcObj, warObj.teamList[side^1].values()) # 失败
	else:
		if warObj.winner == TEAM_SIDE_1:  # 玩家胜利
			warWin(gameObj, warObj, npcObj, warObj.teamList[TEAM_SIDE_1].values())
		else:  # 玩家失败
			warFail(gameObj, warObj, npcObj, warObj.teamList[TEAM_SIDE_1].values())
			
	gameObj.warEnd(warObj, npcObj)
	
def warWin(gameObj, warObj, npcObj, warriorList):
	gameObj.warWin(warObj, npcObj, warriorList)
	
	if hasattr(warObj,"monsterCnt"):
		monsterCnt = warObj.monsterCnt
		for w in warriorList:
			if not w.isRole():
				continue
			who = getRole(w.id)
			if not who:
				continue
			task.monstercnt.addHasMonsterCnt(who, monsterCnt)  # 除妖卫道
	
def warFail(gameObj, warObj, npcObj, warriorList):
	gameObj.warFail(warObj, npcObj, warriorList)



#===============================================================================
# PK
#===============================================================================
def createPKWar(who, targetObj, gameObj=None, npcObj=None):
	'''创建玩家PK
	'''
	if who.inWar() or targetObj.inWar():
		return None

	warObj = None
	if hasattr(gameObj, "newWar"):
		warObj = gameObj.newWar(who)
	if not warObj:
		warObj = war.object.War(WAR_PK)

	warObj.setAutoFight(False)
	warObj.gameNpc = npcObj.this() if npcObj else None
	warObj.game = gameObj
	
	if hasattr(gameObj, "setupWar"):
		gameObj.setupWar(warObj, who, npcObj)
	if not warObj.onWarEnd:
		warObj.onWarEnd = onWarEnd
	
	# 玩家
	addRoleFight(warObj, who, TEAM_SIDE_1)
	addRoleFight(warObj, targetObj, TEAM_SIDE_2)

	warObj.start()
	return warObj

import weakref
import copy
from common import *
from war.defines import *
import war
import war.warrior
import war.monster
import monsterBase
import war.object
import template
import task.monstercnt
import team.defines
import lineup