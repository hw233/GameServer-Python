# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·秘册'''
	intro = '''$target追过来了，看看发生什么事'''
	detail = '''$target追过来了，看看发生什么事'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2002,E(2002,2002)'''
#导表结束