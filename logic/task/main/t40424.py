# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·雪窟双魔'''
	intro = '''$target果然往火云洞方向走去，快去拦住它们'''
	detail = '''$target果然往火云洞方向走去，快去拦住它们'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2046,NI2047,E(2046,2061),E(2047,2062)'''
#导表结束