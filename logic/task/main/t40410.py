# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·温玉'''
	intro = '''击退野兽后，去看看$target，他情况不太妙'''
	detail = '''击退野兽后，去看看$target，他情况不太妙'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2019,E(2019,2026)'''
#导表结束