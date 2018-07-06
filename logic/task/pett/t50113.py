# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·头目'''
	intro = '''前往莽苍山，找到蝎子来源'''
	detail = '''从小虎儿那得知蝎子从莽苍山来的，前往莽苍山找到蝎子头目。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1025,E(1025,1070)'''
#导表结束