# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5101
	name = "锋锐"
	performList = (5101,)
	score = 90
	applyList = {
		"phyCrit":10,
	}
#导表结束
