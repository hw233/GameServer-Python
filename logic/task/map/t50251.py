# -*- coding: utf-8 -*-
from task.defines import *
from task.map.t50201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50251
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''月儿岛取宝任务'''
	intro = '''找$target获赠宝物'''
	detail = '''前往$scene找$target获赠宝物'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2001,E(1,2001)'''
#导表结束

	def onBorn(self, who, npcObj, **kwargs):
		customTask.onBorn(self, who, npcObj, **kwargs)
		self.setTime(12*3600)
		
	def getBranchCondition(self, who, npcObj, branchIdx, flag):
		if flag == "lv":
			lst = [info["条件"] for info in self.getBranchInfo(branchIdx)]
			lst.sort(reverse=True)
			for lv in lst:
				if who.level >= lv:
					return lv
			
		return customTask.getBranchCondition(self, who, npcObj, branchIdx, flag)	
		
		