# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第一章·修复'''
	intro = '''$target工作时受伤了，急需$props，请马上找来'''
	detail = '''$target工作时受伤了，急需$props，请马上找来'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,L(221101,1),E(1004,1026)'''
#导表结束