# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·突变'''
	intro = '''苍茫山路上，$target匆匆跑过，发生什么事？'''
	detail = '''苍茫山路上，$target匆匆跑过，发生什么事？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2001,E(2001,2001)'''
#导表结束