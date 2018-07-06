# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·弑师'''
	intro = '''$target与一众师兄姐已经严阵以待'''
	detail = '''$target与一众师兄姐已经严阵以待'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2011,NI2012,NI2013,NI2014,E(2011,2014),E(2012,2015),E(2013,2016),E(2014,2017)'''
#导表结束