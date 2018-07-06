# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·遇袭'''
	intro = '''$target脸色有点奇怪'''
	detail = '''$target脸色有点奇怪，似乎有不详的预感'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1009,E(1009,1014)'''
#导表结束