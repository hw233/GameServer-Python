# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_COLLECT
	icon = 0
	title = '''第二章·放火（一）'''
	intro = '''慈云寺四周有干燥的草堆，点着它们吧'''
	detail = '''慈云寺四周有干燥的草堆，点着它们吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NPE(1521,1536),NPE(1522,1536),NPE(1523,1536)'''
#导表结束
