# -*- coding: utf-8 -*-
# 暗雷相关

def triggerWar(who):
	'''触发暗雷
	'''
	if who.inWar():
		return
	if door.isNearByDoor(who):
		return
	if not hasattr(who, "triggerWarTime"):
		who.triggerWarTime = getSecond()
		return
	if tryTaskTriggerWar(who, True):
		who.triggerWarTime = getSecond()
		return
	
	subTime = getSecond() - who.triggerWarTime
	if subTime > 0 and subTime < rand(10, 50):
		return
	if rand(100) < 95:
		return

	if tryTaskTriggerWar(who, False):
		who.triggerWarTime = getSecond()
		return
	if trySceneTriggerWar(who):
		who.triggerWarTime = getSecond()
		return

def tryTaskTriggerWar(who, customRatio):
	'''尝试触发任务暗雷
	'''
	taskList = []

	# 组队任务暗雷
	if who.inTeam() and who.getTeamObj().isLeader(who.id):
		for taskObj in who.getTeamObj().taskCtn.getAllValues():
			taskList.append(taskObj)
	
	# 单人任务暗雷
	for taskObj in who.taskCtn.getAllValues():
		taskList.append(taskObj)
		
	for taskObj in taskList:
		if customRatio: # 自定义概率的暗雷
			if not hasattr(taskObj, "customTriggerRatio"):
				continue
			if not taskObj.customTriggerRatio(who):
				continue
		if hasattr(taskObj, "onTriggerWar") and taskObj.onTriggerWar(who):
			return True
		
	return False

def trySceneTriggerWar(who):
	'''尝试触发场景暗雷战斗
	'''
	sceneId = who.sceneId
	if not sceneId in anleiData.sceneFight:
		return False
	fightList = anleiData.sceneFight[sceneId]["战斗"]
	fightIdx = shuffleList(fightList)[0]
	warObj = war.warctrl.createCommonWar(who, fightIdx, anleiData.fightInfo[fightIdx], anleiData.ableInfo)
	warObj.onWarEnd = onWarEnd
	warObj.sceneId = sceneId
	return True

def onWarEnd(warObj):
	'''战斗结束时
	'''
	if warObj.winner != TEAM_SIDE_1:
		return
	sceneId = warObj.sceneId
	rewardIdx = anleiData.sceneFight[sceneId]["奖励"]
	rewardInfo = anleiData.rewardInfo[rewardIdx]
	monsterCnt = warObj.monsterCnt
	for w in warObj.teamList[TEAM_SIDE_1].values():
		if not w.isRole():
			continue
		who = getRole(w.id)
		if not who:
			continue

		for _type in rewardInfo.iterkeys():
	# 		if _type in ("传闻",):
	# 			continue
			val = rewardInfo.get(_type)
			if not val:
				continue
			val = transCodeForReward(val, _type, who)
			rewardByType(who, val, _type)
			
		task.monstercnt.addHasMonsterCnt(who, monsterCnt) # 除妖卫道
			
			
def transCodeForReward(code, _type, who):
	if who:
		if "PLV" in code:
			petObj = who.getLastFightPet()
			if petObj:
				petLv = petObj.level
			else:
				petLv = 0
			code = code.replace("PLV", str(petLv))
		if "LV" in code:
			code = code.replace("LV", str(who.level))
		
	return code

def rewardByType(who, val, _type):
	'''根据类型奖励
	'''
	if _type == "经验":
		val = int(eval(val))
		who.rewardExp(val, "暗雷")
	elif _type == "宠物经验":
		val = int(eval(val))
		petObj = who.getLastFightPet()
		if petObj:
			petObj.rewardExp(val, "暗雷")
	elif _type == "银币":
		val = int(eval(val))
		who.rewardCash(val, "暗雷")
	elif _type == "物品":
		for rwdIdx in val.split(","):
			rewardProps(who, int(rwdIdx))

def rewardProps(who, rwdIdx):
	'''奖励物品
	'''
	info = anleiData.rewardPropsInfo[rwdIdx]
	idx = chooseKey(info, key="权重")
	if not idx:
		return

	info = info[idx]
	propsNo, args, kwargs = misc.parseItemInfo(info["物品"])
	if not propsNo:
		return
	amount = int(transCodeForReward(info["数量"], "数量", who))
	binded = info.get("绑定", 0)
	launch.launchBySpecify(who, int(propsNo), amount, binded, "暗雷")
	
	if info.get("传闻"):
		# toDo 传闻  message.annouce(self.getText(info["传闻"]))
		pass

from common import *
import anleiData
import war.warctrl
from war.defines import *
import pet
import misc
import launch
import task.monstercnt
import door
