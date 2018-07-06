# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第一章·孝敬'''
	intro = '''师父累了，寻找$props，将其奉献给$target'''
	detail = '''师父说口诀都说得口干，找点喝的给师父吧。'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1013,L(221102,1),E(1013,1008)'''
#导表结束