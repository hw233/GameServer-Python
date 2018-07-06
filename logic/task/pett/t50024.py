# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 2
	title = '''螺旋草·治伤'''
	intro = '''找到$props，把药交给$target'''
	detail = '''原来螺旋草在看护被魔道追杀的人，误以为你是敌人所以出手……出于善心还是帮它一把，找来治伤的药物吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1002,L(221101,1),E(1002,1009)'''
#导表结束