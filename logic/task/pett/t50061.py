# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·求助'''
	intro = '''面见$target，询问发生何事'''
	detail = '''仙子看上去非常着急，不知道发生了什么事？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1033)'''
#导表结束