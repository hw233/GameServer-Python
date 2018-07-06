# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''文雀·遇敌'''
	intro = '''回到青螺竹林，发现文雀被抓'''
	detail = '''听仙子的话后回到青螺竹林，发现文雀被魔修士抓住，将要变成下酒菜。救下文雀。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1007,E(1007,1025)'''
#导表结束