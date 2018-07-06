# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''云犬·出走'''
	intro = '''$target有事找你'''
	detail = '''仙子似乎还遇到其他麻烦，听听她要说什么。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10303,1013)'''
#导表结束