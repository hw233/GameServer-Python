# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·路人'''
	intro = '''迎面有一$target走过来'''
	detail = '''迎面有一$target走过来'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2001,E(2001,2001)'''
#导表结束