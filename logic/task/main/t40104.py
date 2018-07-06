# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''第二章·训练'''
	intro = '''阅读锦书大受裨益，四处巡逻寻些野兽练招'''
	detail = '''阅读锦书大受裨益，四处巡逻寻些野兽练招'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''ANLEI(2003,2005,1040)'''
#导表结束