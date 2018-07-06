# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30301
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''运镖'''
	intro = '''运镖给$target'''
	detail = '''运镖给$target，切莫耽误'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(9001,1001)'''

	npcInfo = {
	}

	eventInfo = {
		1001:{"点击":"DONE,DEFF,R1001,$BACK"},
	}

	rewardInfo = {
		1001:{"物品":[1002]},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":100,"物品":"200001","数量":lambda :250000,"绑定":0},
		),
		1002:(
			{"权重":100,"物品":"200002","数量":lambda F:1500*F,"绑定":0},
		),
	}

	groupInfo = {
		9001:(20301,20302,20303,20304,20401,20402,20501,10601,20601,20602,20603,20701,20702,20901,20902,20903,),
		9002:(1001,1002,),
		9003:(1001,1002,),
	}

	chatInfo = {
		1001:'''嗯，辛苦$SEX1了。''',
		1002:'''总算来了，劳累$SEX1护送了！''',
	}

	branchInfo = {
		1001:(
			{"条件":0,"脚本":"L(9007,1)"},
			{"条件":10,"脚本":"L(9008,1)"},
			{"条件":20,"脚本":"L(9009,1)"},
			{"条件":30,"脚本":"L(9010,1)"},
			{"条件":40,"脚本":"L(9011,1)"},
		),
		1002:(
			{"条件":0,"脚本":"L(9006,1)"},
		),
		1003:(
			{"条件":11,"脚本":"E(10101,1012)"},
			{"条件":12,"脚本":"E(10102,1013)"},
			{"条件":13,"脚本":"E(10103,1014)"},
			{"条件":14,"脚本":"E(10104,1015)"},
			{"条件":15,"脚本":"E(10105,1016)"},
			{"条件":16,"脚本":"E(10106,1017)"},
		),
		1004:(
			{"条件":11,"脚本":"NE(2001,2001)"},
			{"条件":12,"脚本":"NE(2006,2006)"},
			{"条件":13,"脚本":"NE(2011,2011)"},
			{"条件":14,"脚本":"NE(2016,2016)"},
			{"条件":15,"脚本":"NE(2021,2021)"},
			{"条件":16,"脚本":"NE(2026,2026)"},
		),
		1005:(
			{"条件":11,"脚本":"NE(2002,2002)"},
			{"条件":12,"脚本":"NE(2007,2007)"},
			{"条件":13,"脚本":"NE(2012,2012)"},
			{"条件":14,"脚本":"NE(2017,2017)"},
			{"条件":15,"脚本":"NE(2022,2022)"},
			{"条件":16,"脚本":"NE(2027,2027)"},
		),
		1006:(
			{"条件":11,"脚本":"NE(2003,2003)"},
			{"条件":12,"脚本":"NE(2008,2008)"},
			{"条件":13,"脚本":"NE(2013,2013)"},
			{"条件":14,"脚本":"NE(2018,2018)"},
			{"条件":15,"脚本":"NE(2023,2023)"},
			{"条件":16,"脚本":"NE(2028,2028)"},
		),
		1007:(
			{"条件":11,"脚本":"NE(2004,2004)"},
			{"条件":12,"脚本":"NE(2009,2009)"},
			{"条件":13,"脚本":"NE(2014,2014)"},
			{"条件":14,"脚本":"NE(2019,2019)"},
			{"条件":15,"脚本":"NE(2024,2024)"},
			{"条件":16,"脚本":"NE(2030,2030)"},
		),
		1008:(
			{"条件":11,"脚本":"NE(2005,2005)"},
			{"条件":12,"脚本":"NE(2010,2010)"},
			{"条件":13,"脚本":"NE(2015,2015)"},
			{"条件":14,"脚本":"NE(2020,2020)"},
			{"条件":15,"脚本":"NE(2025,2025)"},
			{"条件":16,"脚本":"NE(2030,2030)"},
		),
	}

	fightInfo = {
		1001:(
			{"类型":0,"名称":"强盗","造型":"5002(0,1,0,0,0)","能力编号":"1002","数量":"2","技能":(5401,5406,),"站位":(8,3,)},
			{"类型":0,"名称":"绑匪","造型":"4001(0,1,0,0,0)","能力编号":"1002","数量":"2","技能":(5402,5407,),"站位":(6,1,)},
			{"类型":0,"名称":"杀手","造型":"4007(0,1,0,0,0)","能力编号":"1001","数量":"2","技能":(5413,5418,),"站位":(7,2,)},
		),
		1002:(
			{"类型":0,"名称":"猛兽","造型":"3005(0,1,0,0,0)","能力编号":"1002","数量":"1","技能":(5403,5408,),"站位":(6,)},
			{"类型":0,"名称":"野兽","造型":"3004(0,1,0,0,0)","能力编号":"1002","数量":"1","技能":(5404,5409,),"站位":(1,)},
			{"类型":0,"名称":"恶兽","造型":"3008(0,1,0,0,0)","能力编号":"1001","数量":"2","技能":(5415,5420,),"站位":(7,8,)},
			{"类型":0,"名称":"邪兽","造型":"3007(0,1,0,0,0)","能力编号":"1001","数量":"2","技能":(5411,5416,),"站位":(3,2,)},
		),
	}

	ableInfo = {
		1001:{"等级":"LV","生命":"B*0.6","真气":"B*1","物理伤害":"B*0.49","法术伤害":"B*0.34","物理防御":"B*0.42","法术防御":"B*0.29","速度":"B*0.72","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"LV","生命":"B*0.6","真气":"B*1","物理伤害":"B*0.34","法术伤害":"B*0.49","物理防御":"B*0.29","法术防御":"B*0.42","速度":"B*0.72","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	configInfo = {
		"生成路径":"escort",
	}
#导表结束


	def onMissionDone(self, who, npcObj):
		actObj = activity.getActivity("escort")
		if actObj:
			actObj.doneEscort(who)
			perPoint = activity.center.getPerActPoint(13)
			who.addActPoint(perPoint)
		who.day.add("escort", 1)
		cash = actObj.getDeposit()
		who.addCash(cash, "运镖押金退还", None)
		message.message(who, "返还运镖押金#R<{},3,2>#n".format(cash))

	def customRewardProps(self, who, propsNo, amount, binded, *args, **kwargs):
		launch.launchBySpecify(who, int(propsNo), amount, binded)
		return True

	def customEvent(self, who, npcObj, eventName, *args):
		if eventName == "BACK":
			self.backToEscortNpc(who, npcObj)

	def backToEscortNpc(self, who, npcObj):
		'''回到运镖任务领取npc
		'''
		roleId = who.id
		chatIdx = self.transIdxByGroup(9002)
		text = self.getText(chatIdx, roleId)
		actObj = activity.getActivity("escort")
		maxCnt = actObj.getMaxCount()
		if who.day.fetch("escort") >= maxCnt:
			npcObj.say(who, text)
			return
		message.confirmBoxNew(who, responseBackToEscortNpc, actObj.getText(1009, roleId))

	def setup(self, who):#override
		self.checkCnt = 0
		# self.timerMgr.run(self.checkFight, 20, 10, "checkFight")
		
	def customTriggerRatio(self, who):
		'''自定义暗雷概率
		'''
		self.checkCnt += 1
		if self.checkCnt < 10:
			return False
		if self.checkCnt % 5:
			return False
		n = (self.checkCnt - 10) / 5
		if rand(100) > 20 + 20 * n:
			return False
		return True

	def onTriggerWar(self, who):
		'''触发暗雷
		'''
		# 从开始第20s后，每10s判定一次，概率 = 20% + 20% * N，战斗完之后会有20s冷却时间，在此期概率 = 0
		# 应客户端要求改成移动包来判断，两秒一次移动包
		
		who = self.getOwnerObj()
		fightIdx = self.transIdxByGroup(9003)
		self.fight(who, None, fightIdx)
		# self.timerMgr.cancel("checkFight")
		return True

	@property
	def canTransfer(self):
		return False

	def warEnd(self, warObj, npcObj):
		'''战斗结束
		'''
		self.checkCnt = 0
		# self.timerMgr.run(self.checkFight, 20, 10, "checkFight")
		who = self.getOwnerObj()
		if who:
			self.goAhead(who)

	def onWarFail(self, warObj, npcObj, w):
		'''战斗失败时
		'''
		who = getRole(w.id)
		if who:
			# 扣除运镖奖励10%元宝
			actObj = activity.getActivity("escort")
			if actObj:
				actObj.doScript(who, npcObj, "TP1005")
			self.add("warFail", 1)
			pass

	def getValueByVarName(self, varName, who):
		if varName == "F":
			if who:
				res = 1 - self.fetch("warFail") * 0.1
				return max(0, res)
			return 1
		return customTask.getValueByVarName(self, varName, who)

	def isValid(self):
		'''是否有效
		'''
		return 0

def responseBackToEscortNpc(who, yes):
	'''传送到运镖任务领取NPC
	'''
	if not yes:
		return
	npcObj = npc.getNpcByIdx(10209)
	if not npcObj:
		return
	if not scene.tryTransfer(who.id, npcObj.sceneId, 52, 47):
		return
	npcObj.doLook(who)


from common import *
import activity
import launch
import scene
import myGreenlet
import message
import npc
import activity.center
