# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_COMMON
	id = 10301
	name = "学有所成"
	point = 5
#导表结束