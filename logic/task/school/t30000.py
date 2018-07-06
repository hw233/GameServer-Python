# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30000
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''师门任务指引'''
	intro = '''师傅有重要的任务要交给你，请尽快找他'''
	detail = '''师傅有重要的任务要交给你，请尽快找他'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(master,3001)'''
#导表结束

	def getTitle(self, who):
		return self.transString(self.title, who.id)

	def onMissionDone(self, who, npcObj):
		'''指引任务，重载父方法，防止自动接师门
		'''
		pass
