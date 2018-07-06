# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("使用物品",)
	conditionList = (
		(1,"性别==男"),
		(2,"拥有称谓(6)==0"),
		(3,"物品编号==221104"),
	)
	conditionScope = ""
	eventList = (
		"给予称谓(6)",
	)
#导表结束