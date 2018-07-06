# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·四师兄'''
	intro = '''$target挡在路上，战胜他吧'''
	detail = '''$target挡在路上，战胜他吧'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2008,NI2009,E(2008,2010),E(2009,2011)'''
#导表结束