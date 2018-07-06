# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("使用物品",)
	conditionList = (
		(1,"拥有称谓(5)==0"),
		(2,"人物等级>30"),
		(3,"物品编号==221103"),
	)
	conditionScope = ""
	eventList = (
		"给予称谓(5)",
	)
#导表结束