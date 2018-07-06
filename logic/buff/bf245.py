# -*- coding: utf-8 -*-
from buff.defines import *
from buff.bf225 import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "高级眩晕"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"禁止指令":True,
	}
#导表结束