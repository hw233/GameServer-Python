# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·丁引'''
	intro = '''那边似有吵闹，过去看一下'''
	detail = '''那边似有吵闹，过去看一下'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1503,NI1504,NI1505,NI1506,E(1503,1509),E(1504,1510),E(1505,1511),E(1506,1512)'''
#导表结束