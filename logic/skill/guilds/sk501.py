# -*- coding: utf-8 -*-
from skill.object import GuildSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 501
	name = "强身术"
	applyList = {
		"hpMax":lambda SLV:SLV*10,
	}
#导表结束

