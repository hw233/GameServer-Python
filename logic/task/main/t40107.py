# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·决心'''
	intro = '''依旧与$target说话'''
	detail = '''依旧与$target说话'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2006,E(2006,2008)'''
#导表结束