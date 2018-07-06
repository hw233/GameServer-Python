# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_COLLECT
	icon = 0
	title = '''仙盟-清除杂草'''
	intro = '''清除杂草'''
	detail = '''仙盟里最近杂草丛生，清理下吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NPE(1012,1005),NPE(1013,1005),NPE(1014,1005)'''
#导表结束

