# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''玄武龟·魔道'''
	intro = '''与赤身教门下战斗，除掉他'''
	detail = '''果然遇到不怀好意的魔道之人，动手除掉他。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1001,E(1001,1004)'''
#导表结束