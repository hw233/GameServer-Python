# -*- coding: utf-8 -*-
from task.defines import *
from task.bamboo.t30401 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30401
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''竹林除妖'''
	intro = '''让#C02村民们#n平静下来'''
	detail = '''村民们被愤怒冲晕了头脑，先让他们冷静下来吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,NI1003,E(1004,1010),NIE(1005,1012),$LND1005'''
#导表结束