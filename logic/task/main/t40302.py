# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·芝仙'''
	intro = '''刚到天墉，便发现熟悉的面孔，$target旁边似乎是？'''
	detail = '''刚到天墉，便发现熟悉的面孔，$target旁边似乎是？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1501,NI1502,E(1501,1507),E(1502,1508)'''
#导表结束