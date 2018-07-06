# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "百足疾走"
	type = BUFF_TYPE_BUFF
	applyList = {
		"速度加成":10,
	}
#导表结束