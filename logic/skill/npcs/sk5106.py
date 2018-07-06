# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5106
	name = "灵护"
	performList = (5106,)
	score = 60
	applyList = {
		"magDef":lambda LV:LV*0.8,
	}
#导表结束
