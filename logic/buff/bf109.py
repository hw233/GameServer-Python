# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "迷魂夺魄"
	type = BUFF_TYPE_SEAL
	applyList = {
		"禁止物理攻击":True,
		"禁止法术":True,
	}
#导表结束