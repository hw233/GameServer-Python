# -*- coding: utf-8 -*-
from task.defines import *
from task.map.t50201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''秘册任务指引'''
	intro = '''少侠已经足够强，可以去接去秘册任务了'''
	detail = '''少侠已经足够强，可以去接去秘册任务了'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10402,3001)'''
#导表结束

	def onMissionDone(self, who, npcObj):
		pass
