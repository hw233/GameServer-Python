# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''50006'''
	intro = '''与$target说话'''
	detail = '''前面$target看起来是位大仙，仙缘际遇，不可错过！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1001,E(1001,1001)'''
#导表结束