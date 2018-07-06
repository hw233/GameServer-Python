# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·朱文'''
	intro = '''$target飞剑传书，约定大家于妖蛇洞窟前相聚'''
	detail = '''$target飞剑传书，约定大家于妖蛇洞窟前相聚'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1018,NI1019,NI1020,NI1021,E(1018,1059),E(1019,1060),E(1020,1061),E(1021,1062)'''
#导表结束