# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·闲谈'''
	intro = '''$target突然叫住了你，过去与他说话'''
	detail = '''突然之间，二师兄叫住你了，看看是什么事？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1014,E(1014,1010)'''
#导表结束