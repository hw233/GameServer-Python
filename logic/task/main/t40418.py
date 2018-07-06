# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·妖尸'''
	intro = '''向$target等发起攻击吧'''
	detail = '''向$target等发起攻击吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2033,NI2034,E(2033,2042),E(2034,2043)'''
#导表结束