# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	type = 200
	parentId = 10301
	targetType = TASK_TARGET_TYPE_FIGHT
	title = '''除妖卫道'''
	intro = '''在任意战斗中击杀($hasCnt/$needCnt)个怪物'''
	detail = '''近有贼寇，远有妖族侵犯我大唐国土，唐皇特召骁勇之士，驱除娇害，安抚民众。'''
	initScript = ''''''

	npcInfo = {
	}

	eventInfo = {
		1001:{"成功":"R1001,DONE"},
	}

	rewardInfo = {
		1001:{"经验":"LV*5+100","宠物经验":"PLV*2+100","银币":"999","物品":"1001"},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":100,"物品":"202006","数量":"1","绑定":0},
		),
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

	monsterData = {
		(0,49):{"怪物数量":100},
		(50,69):{"怪物数量":200},
		(70,0):{"怪物数量":300},
	}
#导表结束

	def onBorn(self, who, npcObj, **kwargs):
		customTask.onBorn(self, who, npcObj, **kwargs)
		self.set("needCnt", self.calNeedMonsterCnt(who.level))
		self.set("dayNo", getDayNo())
		
	def calNeedMonsterCnt(self, level):
		for k, v in self.monsterData.iteritems():
			minLv, maxLv = k
			if minLv <= level <= maxLv:
				return v["怪物数量"]
			if minLv == 0 and level <= maxLv:
				return v["怪物数量"]
			if maxLv == 0 and level >= minLv:
				return v["怪物数量"]
			
		return 999
	
	def getNeedMonsterCnt(self):
		'''所需杀妖数
		'''
		return self.fetch("needCnt")
	
	def getHasMonsterCnt(self):
		'''已杀妖数
		'''
		return self.fetch("hasCnt")
	
	def addHasMonsterCnt(self, monsterCnt):
		'''增加杀妖数
		'''
		self.add("hasCnt", monsterCnt)
		
		if self.getHasMonsterCnt() >= self.getNeedMonsterCnt():
			self.doDone()
		else: # 刷新杀妖数
			self.refresh()
	
	def doDone(self):
		'''完成
		'''
		eventInfo = self.getEventInfo(1001)
		who = getRole(self.ownerId)
		self.doScript(who, None, eventInfo["成功"])
	
	def transString(self, content, pid=0):
		if "$needCnt" in content:
			needCnt = self.getNeedMonsterCnt()
			content = content.replace("$needCnt", str(needCnt))
		if "$hasCnt" in content:
			hasCnt = self.getHasMonsterCnt()
			content = content.replace("$hasCnt", str(hasCnt))
		return customTask.transString(self, content, pid)
	
	def isValid(self):
		'''是否有效
		'''
		return self.fetch("dayNo") == getDayNo()
	
	def onNewDay(self):
		'''刷天时
		'''
		who = getRole(self.ownerId)
		task.removeTask(who, self.id)
				

from common import *
import task.monstercnt
		