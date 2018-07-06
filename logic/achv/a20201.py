# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 20201
	name = "雷厉风行"
	point = 15
	totalProgress = 60
	timeLimit = 3600
#导表结束
