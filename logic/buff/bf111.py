# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "禁绝百骸"
	type = BUFF_TYPE_SEAL
	applyList = {
		"禁止物理攻击":True,
		"禁止法术":True,
		"禁止特技":True,
		"禁止物品":True,
	}
#导表结束