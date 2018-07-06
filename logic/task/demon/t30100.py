# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30100
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''降魔任务领取'''
	intro = '''$target正在找你'''
	detail = '''$target在四处找你，似乎有什么重要事情。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10401,3001)'''
#导表结束

	def getRefObj(self):
		'''关联对象
		'''
		return task.demon.t30101.Task

	def onBorn(self, who, npcObj, **kwargs):
		customTask.onBorn(self, who, npcObj, **kwargs)
		doublePoint = who.doublePoint
		if 0 < doublePoint:
			return
		fdp = who.getFrozenDoublePoint()
		if not fdp:
			return
		dp = min(fdp, 80 - doublePoint, 40)
		who.addDoublePoint(dp, "领取高倍点数", False)
		who.addFrozenDoublePoint(-dp, "领取高倍点数")
		activity.center.centerChange(who, "doublePoint", "frozenDoublePoint")
	 	

import task.demon.t30101
import activity.center
