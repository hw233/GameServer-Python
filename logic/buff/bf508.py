# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "蜀山弟子"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"被物理伤害结果加成":-5,
		"被法术伤害结果加成":-5,
	}
#导表结束