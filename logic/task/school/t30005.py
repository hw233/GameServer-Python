# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''师门-教训恶霸'''
	intro = '''恶霸$target又在为祸乡民，是时候出手教训了。'''
	detail = '''恶霸$target心术不正，学了点微末道术就出来鱼肉百姓，要好好教训他们了。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NE(9014,1005)'''
#导表结束