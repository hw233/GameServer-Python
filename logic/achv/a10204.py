# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 10204
	name = "摆摊小贩"
	point = 5
	totalProgress = 100000
#导表结束