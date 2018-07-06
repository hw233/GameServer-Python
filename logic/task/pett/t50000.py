# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50000
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''异兽任务领取'''
	intro = '''$target正在找你'''
	detail = '''$target在四处找你，似乎有什么重要事情。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束
	
	def getTargetNpc(self):
		'''目标npc
		'''
		return npc.getNpcByIdx(10208)

	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 0
		
import npc
	