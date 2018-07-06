# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "高级冲锋"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"速度加成":25,
	}
#导表结束