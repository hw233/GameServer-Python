# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("完成任务",)
	conditionList = (
		(1,"任务类型==30101"),
		(2,"任务类型==30102"),
		(3,"任务类型==30103"),
	)
	conditionScope = "1 or 2 or 3"
	eventList = (
		"增加成就进度(20201,1)",
	)
#导表结束