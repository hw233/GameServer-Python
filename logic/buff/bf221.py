# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "冲锋"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"速度加成":15,
	}
#导表结束