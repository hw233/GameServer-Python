# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("获得助战",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"增加成就进度(10501,1)",
	)
#导表结束