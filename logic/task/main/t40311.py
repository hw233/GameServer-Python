# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·法元'''
	intro = '''火速来到慈云寺中，正见敌魁$target等在大殿谈话，靠近一点偷听吧'''
	detail = '''火速来到慈云寺中，正见敌魁$target等在大殿谈话，靠近一点偷听吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1518,NI1519,NI1520,E(1518,1533),E(1519,1534),E(1520,1535)'''
#导表结束