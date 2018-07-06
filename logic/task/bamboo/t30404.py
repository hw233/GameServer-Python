# -*- coding: utf-8 -*-
from task.defines import *
from task.bamboo.t30401 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30401
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''竹林除妖'''
	intro = '''战胜$target'''
	detail = '''找到控制僵尸们的幕后黑手，继续调查'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1007,E(1007,1006),$LND1010'''
#导表结束