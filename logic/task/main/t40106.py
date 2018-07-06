# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第二章·小孩子'''
	intro = '''路上有个$target受伤了，快买药给他涂抹'''
	detail = '''路上有个$target受伤了，快买药给他涂抹'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2006,L(221101,1),E(2006,2007)'''
#导表结束