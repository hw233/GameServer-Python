# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·族长'''
	intro = '''与鸠盘婆对话，询问原因'''
	detail = '''与鸠盘婆对话，询问春天不来的原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10104,1060)'''
#导表结束