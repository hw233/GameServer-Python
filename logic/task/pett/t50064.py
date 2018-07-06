# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·经过'''
	intro = '''询问小女孩，理清事情经过'''
	detail = '''杀死巨蛇后，小女孩和一只巨熊现身了，巨熊身上都是伤，看起来很严重。问问小女孩，这到底是怎么回事？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1011,E(1011,1036)'''
#导表结束