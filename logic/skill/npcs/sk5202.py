# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5202
	name = "高级灵犀"
	performList = (5202,)
	score = 150
	applyList = {
		"magCrit":20,
	}
#导表结束
