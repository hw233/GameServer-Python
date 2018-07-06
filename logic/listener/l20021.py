# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("穿装备",)
	conditionList = (
		(1,"身上装备特技数>=6"),
	)
	conditionScope = ""
	eventList = (
		"达成成就(10603)",
	)
#导表结束