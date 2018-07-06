# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_COMMON
	id = 10105
	name = "小有名气"
	point = 10
#导表结束