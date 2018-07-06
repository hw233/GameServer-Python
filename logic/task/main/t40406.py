# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·旧相识'''
	intro = '''突然有人叫喊，循声而看，却是旧相识$target'''
	detail = '''突然有人叫喊，循声而看，却是旧相识$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2011,NI2010,E(2011,2015),E(2010,2016)'''
#导表结束