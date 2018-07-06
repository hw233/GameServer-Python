# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "雪满封山"
	type = BUFF_TYPE_BUFF
	applyList = {
		"物理躲闪率加成":20,
		"法术躲闪率加成":20,
	}
#导表结束
