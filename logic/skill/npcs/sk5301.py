# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5301
	name = "灵草冥毒"
	performList = (5301,)
	score = 0
	applyList = {
		"phyDamRatio":10,
	}
#导表结束

