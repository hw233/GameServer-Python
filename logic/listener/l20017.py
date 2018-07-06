# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("获得助战",)
	conditionList = (
		(1,"助战编号==2002"),
		(2,"助战编号==3002"),
	)
	conditionScope = "1 or 2"
	eventList = (
		"达成成就条件(10502,助战编号)",
	)
#导表结束