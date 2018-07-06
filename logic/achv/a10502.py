# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_COND
	id = 10502
	name = "笑哈哈"
	point = 5
	conditionList = {
		1:2002,
		2:3002,
	}
#导表结束