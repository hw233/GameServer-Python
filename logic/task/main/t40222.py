# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·无辜'''
	intro = '''美人蛇东奔西走，依然突破不了诛邪刀阵，然而此时……'''
	detail = '''美人蛇东奔西走，依然突破不了诛邪刀阵，然而此时……'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1025,E(1025,1067)'''
#导表结束