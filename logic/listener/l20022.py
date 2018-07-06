# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("完成任务",)
	conditionList = (
		(1,"任务类型==30001"),
	)
	conditionScope = ""
	eventList = (
		"增加成就进度(20101,1)",
	)
#导表结束