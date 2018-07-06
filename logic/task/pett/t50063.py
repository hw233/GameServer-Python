# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·巨蛇'''
	intro = '''发现血迹源头，击杀巨蛇'''
	detail = '''跟随带毒血迹一路寻找，果然发现一条带伤的巨蛇！它在疯狂地攻击附近所有生物，还是先收拾了它吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1010,E(1010,1035)'''
#导表结束