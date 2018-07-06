# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·嫌疑'''
	intro = '''解决完野兽后，发现$target在前面向我们招手'''
	detail = '''解决完野兽后，发现$target在前面向我们招手'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1513,E(1513,1524)'''
#导表结束