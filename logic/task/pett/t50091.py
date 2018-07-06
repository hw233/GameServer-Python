# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·羽毛'''
	intro = '''得知毕方羽毛消失，探查内情'''
	detail = '''仙子发现毕方的羽毛消失大半，修为也消耗了许多，请你查探其中的内情。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1050)'''
#导表结束