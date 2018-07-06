# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("重铸装备",)
	conditionList = (
		(1,"重铸后珍品==0"),
	)
	conditionScope = ""
	eventList = (
		"增加成就进度(10602,1)",
	)
#导表结束