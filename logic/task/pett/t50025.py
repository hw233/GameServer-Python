# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''螺旋草·挟持'''
	intro = '''击败心术不正之人，救出螺旋草'''
	detail = '''这人受伤是假的！他为了得到能够治愈病痛的灵药，反过来抓住了螺旋草，得赶紧把它救下！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1003,E(1003,1010)'''
#导表结束