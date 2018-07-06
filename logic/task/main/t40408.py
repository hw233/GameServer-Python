# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·冰窟'''
	intro = '''还是不放心，先偷偷跟过去，看看$target的情况'''
	detail = '''还是不放心，先偷偷跟过去，看看$target的情况'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2015,NI2016,E(2015,2020),E(2016,2022)'''
#导表结束