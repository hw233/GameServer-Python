# -*- coding: utf-8 -*-
from task.defines import *
from task.test.t00001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 1
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''试炼'''
	intro = '''与$target战斗'''
	detail = '''击败$target，证明你的根基'''
	rewardDesc = '''200001,221102'''
	goAheadScript = ''''''
	initScript = '''NE(5001,5001),NIE(5002,5002),E(10102,5003)'''
#导表结束
