# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("购买珍品",)
	conditionList = (
		(1,"单价>=1000000"),
	)
	conditionScope = ""
	eventList = (
		"达成成就(10207)",
	)
#导表结束