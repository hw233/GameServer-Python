# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''螺旋草·误会'''
	intro = '''找到螺旋草之后，反被攻击'''
	detail = '''果然在竹林旁边遇到螺旋草，但它似乎有所误会，对你发起了攻击。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1002,E(1002,1008)'''
#导表结束