# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_COLLECT
	icon = 0
	title = '''第三章·搜索'''
	intro = '''搜索莽苍山一带，看看能不能找到#C04朱果#n'''
	detail = '''搜索莽苍山一带，看看能不能找到#C04朱果#n'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NPE(2020,2027),NPE(2021,2027),NPE(2022,2027)'''
#导表结束
