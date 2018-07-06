# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·真相'''
	intro = '''是否要告诉$target他父亲的真相？'''
	detail = '''是否要告诉$target他父亲的真相？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''STORY40033,N1525,E(1525,1538)'''
#导表结束