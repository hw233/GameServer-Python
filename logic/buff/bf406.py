# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "散魂蝎毒"
	type = BUFF_TYPE_DEBUFF
	applyList = {
		"禁止复活":True,
	}
#导表结束