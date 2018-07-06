# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·试炼'''
	intro = '''与$target战斗'''
	detail = '''击败$target，证明你的根基'''
	rewardDesc = '''200001,221102'''
	goAheadScript = ''''''
	initScript = '''N1002,NI1012,E(1002,1003),E(1012,1026)'''
#导表结束