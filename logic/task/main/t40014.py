# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·醉汉'''
	intro = '''与$target战斗，赶走他们'''
	detail = '''与$target战斗，赶走他们'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1010,E(1010,1017)'''
#导表结束