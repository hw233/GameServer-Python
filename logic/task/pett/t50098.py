# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·遭遇'''
	intro = '''回去找毕方时，遭遇鸠盘婆'''
	detail = '''回去告知毕方时，竟然遇到赤身教主鸠盘婆？！她似乎是来找晦气的，看来一战不可避免了。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1019,E(1019,1057)'''
#导表结束