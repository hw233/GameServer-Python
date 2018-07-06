# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·真相'''
	intro = '''$target为何原地陷入沉思中？'''
	detail = '''$target为何原地陷入沉思中？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2005,E(2005,2006)'''
#导表结束