# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·山则'''
	intro = '''$target又赶来了，而且脸上挂彩，似乎有大事发生'''
	detail = '''$target又赶来了，而且脸上挂彩，似乎有大事发生'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2048,NI2049,NI2050,E(2048,2064),E(2049,2065),E(2050,2066)'''
#导表结束