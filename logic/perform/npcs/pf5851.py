# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5811 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5851
	name = "高级强力"
	configInfo = {
		"物理伤害结果加成":5,
		"法术伤害结果加成":5,
	}
#导表结束