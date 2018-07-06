# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "妖莲幻术状态"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"禁止指令":True,
	}
	removable = False
#导表结束