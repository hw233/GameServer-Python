# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("竞技场排名",)
	conditionList = (
		(1,"名次==1"),
	)
	conditionScope = ""
	eventList = (
		"达成成就(60101)",
	)
#导表结束