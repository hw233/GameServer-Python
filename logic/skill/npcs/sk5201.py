# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5201
	name = "高级锋锐"
	performList = (5201,)
	score = 150
	applyList = {
		"phyCrit":20,
	}
#导表结束