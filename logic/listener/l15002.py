# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("使用物品",)
	conditionList = (
		(1,"拥有称谓(2)==0"),
		(2,"物品编号==221202"),
	)
	conditionScope = ""
	eventList = (
		"给予称谓(2)",
	)
#导表结束