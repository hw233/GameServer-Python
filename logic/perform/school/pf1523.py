# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1523
	name = "呼幽唤灵"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = lambda self,LV,SLV:(SLV-LV+2)/10+6
	boutMax = 6
	consumeList = {
		"真气": lambda SLV:SLV*1.2+50,
		"符能": 40,
	}
	speRatio = 105
	configInfo = {
		"名称":"幽灵",
		"造型":"4006(0,1,0,0,0)",
		"染色":(0,0,0,0,0),
		"技能":(1511,),
	}
#导表结束

	def validPerform(self, att, needTips):
		'''检查施法
		'''
		count = 0
		warObj = att.war
		side = att.side
		for w in warObj.teamList[side].itervalues():
			if not hasattr(w, "performId") or w.performId != self.id:
				continue
			if not hasattr(w, "summonIdx") or w.summonIdx == att.idx:
				continue
			count += 1
		if count >= 2:
			if needTips:
				message.tips(att.getPID(), "本方战场最多只能同时存在#C022只#n幽灵")
			return False
	
		return CustomPerform.validPerform(self, att, needTips)

	def perform(self, att, vicCast):
		att.war.rpcWarPerform(att, self.getMagId(), att)
		bout = self.calBout(att)
		shape, shapeParts = template.transShapeStr(self.configInfo["造型"])

		monsterData = {
			"名称": self.configInfo["名称"],
			"造型": shape,
			"造型部位": shapeParts,
			"等级": att.level,
			"生命": max(1, att.hp * 40 / 100),
			"真气": att.mp,
			"物理伤害": att.phyDam,
			"法术伤害": att.magDam,
			"物理防御": att.phyDef,
			"法术防御": att.magDef,
			"速度": att.spe,
			"技能": self.configInfo["技能"],
		}
		
		if self.configInfo.get("染色"):
			monsterData["染色"] = self.configInfo["染色"]
		if self.configInfo.get("技能"):
			monsterData["技能"] = self.configInfo["技能"]
	
		monsterW = perform.summonMonster(att, monsterData, bout, True)
		monsterW.performId = self.id
		self.addApply(monsterW, "法术伤害结果加成", -50)
			
			
import perform
import message
import template