# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·调查'''
	intro = '''下山后还惦记着上次袭击难民们的妖物，决定去调查一番'''
	detail = '''下山后还惦记着上次袭击难民们的妖物，决定去调查一番'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1011,E(1011,1046)'''
#导表结束