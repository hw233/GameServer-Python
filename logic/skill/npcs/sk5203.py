# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5203
	name = "高级悍勇"
	performList = (5203,)
	score = 120
	applyList = {
		"phyDam":lambda LV:LV,
	}
#导表结束
