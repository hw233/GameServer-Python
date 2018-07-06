# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·寻找'''
	intro = '''$target请你寻找灵猴'''
	detail = '''淘气的灵猴逃出了禹鼎，仙子请你去城西查看有没有灵猴的踪迹。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1015)'''
#导表结束