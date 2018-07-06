# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "雪映破踪"
	type = BUFF_TYPE_BUFF
	applyList = {
		"抵抗封印":10,
		"破隐":True,
	}
#导表结束