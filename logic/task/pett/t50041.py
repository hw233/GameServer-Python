# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''文雀·请求'''
	intro = '''$target请你去询问文雀'''
	detail = '''听闻在青螺竹林修行的文雀自从出过门后就闷闷不乐，仙子请你去问问它。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1021)'''
#导表结束