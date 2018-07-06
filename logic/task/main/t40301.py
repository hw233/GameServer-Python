# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·学艺'''
	intro = '''师父找得很急，究竟是何事？'''
	detail = '''师父找得很急，究竟是何事？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1501,school)'''
#导表结束