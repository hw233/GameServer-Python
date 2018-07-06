# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·证明'''
	intro = '''神秘人的话难以置信，与$target说话，询问真相'''
	detail = '''神秘人的话难以置信，与$target说话，询问真相'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1016)'''
#导表结束