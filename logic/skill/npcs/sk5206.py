# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5206
	name = "高级灵护"
	performList = (5206,)
	score = 120
	applyList = {
		"magDef":lambda LV:LV*1.2,
	}
#导表结束
