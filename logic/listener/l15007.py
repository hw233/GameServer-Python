# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("使用物品",)
	conditionList = (
		(1,"性别==女"),
		(2,"拥有称谓(7)==0"),
		(3,"物品编号==221201"),
	)
	conditionScope = ""
	eventList = (
		"给予称谓(7)",
	)
#导表结束