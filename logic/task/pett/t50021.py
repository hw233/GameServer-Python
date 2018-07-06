# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''螺旋草·灵药'''
	intro = '''$target有事拜托'''
	detail = '''给异兽治病的灵药所剩无几，仙子让你去找隐居在青螺竹林的螺旋草，讨要一些灵药。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1006)'''
#导表结束