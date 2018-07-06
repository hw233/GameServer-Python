# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·碧筠庵'''
	intro = '''来到碧筠庵，白谷逸正与各路正道商议要事，过去听一下？'''
	detail = '''来到碧筠庵，白谷逸正与各路正道商议要事，过去听一下？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1507,NI1508,NI1509,E(1507,1514),E(1508,1515),E(1509,1516)'''
#导表结束