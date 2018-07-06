# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5128 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5228
	name = "高级隐匿"
	bout = lambda self,RND:RND(3,5)
	buffId = 243
#导表结束