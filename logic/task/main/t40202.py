# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·询问'''
	intro = '''那道强光究竟是……与$target继续谈话'''
	detail = '''那道强光究竟是……与$target继续谈话'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1002,school)'''
#导表结束