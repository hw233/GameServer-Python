# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·离开'''
	intro = '''与$target说话'''
	detail = '''与$target说话'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1015,E(1015,1023)'''
#导表结束