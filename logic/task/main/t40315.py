# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·血神老人'''
	intro = '''大殿中$target跟血神教门人动起手来，快去支援'''
	detail = '''大殿中$target跟血神教门人动起手来，快去支援'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1526,NI1527,NI1528,NI1529,E(1526,1539),E(1527,1540),E(1528,1541),E(1529,1542)'''
#导表结束