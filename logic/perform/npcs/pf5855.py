# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5815 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5855
	name = "高级指挥强力"
	configInfo = {
		"物理伤害结果加成":5,
		"法术伤害结果加成":5,
	}
#导表结束