# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·魔教'''
	intro = '''与小女孩交谈，询问经过'''
	detail = '''询问小女孩是怎么回事，那条巨蛇和巨熊的伤又是怎么来的。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1011,E(1011,1038)'''
#导表结束