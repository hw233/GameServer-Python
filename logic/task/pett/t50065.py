# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 2
	title = '''傀儡熊·内情'''
	intro = '''找来$props，替巨熊治伤'''
	detail = '''巨熊虽然伤口不少，但幸好没中蛇毒，应小女孩的要求，给巨熊找来伤药。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1011,L(221103,1),E(1011,1037)'''
#导表结束