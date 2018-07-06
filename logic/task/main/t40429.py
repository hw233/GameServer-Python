# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·祭天雷'''
	intro = '''$target刀枪不入，快把先天玄雷符祭出来！'''
	detail = '''$target刀枪不入，快把先天玄雷符祭出来！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2058,NI2038,NI2039,E(2058,2079),E(2038,2076),E(2039,2076)'''
#导表结束