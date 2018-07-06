# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·等待'''
	intro = '''返回碧筠庵，$target等一干人还在会议中'''
	detail = '''返回碧筠庵，$target等一干人还在会议中'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1514,NI1515,,NI1516,NI1517,E(1514,1529),E(1515,1530),E(1516,1531),E(1517,1532)'''
#导表结束