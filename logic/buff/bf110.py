# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "破血噬魂"
	type = BUFF_TYPE_SEAL
	applyList = {
		"禁止物理攻击":True,
		"禁止法术":True,
		"被物理伤害结果加成":15,
		"被法术伤害结果加成":15,
	}
#导表结束