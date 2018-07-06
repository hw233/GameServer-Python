# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·隐忧'''
	intro = '''告知仙子后，仙子很是担忧'''
	detail = '''把巨蛇之事告诉仙子后，仙子却显得十分担忧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1039)'''
#导表结束