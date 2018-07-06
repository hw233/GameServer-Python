# -*- coding: utf-8 -*-
from collect.object import cMainCollect as customClass

#导表开始
class cMainCollect(customClass):

	eventInfo = {
		1001:{"事件类型":1,"事件图标":202043,"事件名称":"浣形丹","剩余时间":8,"守关怪物":"4007(0,1,0,0,0,0)","绑定关卡":1001,"奖励编号":1001},
		1002:{"事件类型":1,"事件图标":202044,"事件名称":"虹彩珠","剩余时间":8,"守关怪物":"4008(0,1,0,0,0,0)","绑定关卡":1002,"奖励编号":1002},
		1003:{"事件类型":1,"事件图标":202045,"事件名称":"彩云晶","剩余时间":8,"守关怪物":"4509(0,1,0,0,0,0)","绑定关卡":1003,"奖励编号":1003},
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"贼","造型":"4007(0,1,0,0,0)","能力编号":"1002","数量":"1","技能":(1111,1112,1113,),"站位":(1,)},
			{"类型":0,"名称":"帮手","造型":"4502(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(2,3,)},
			{"类型":0,"名称":"帮手","造型":"4504(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(4,5,)},
		),
		1002:(
			{"类型":1,"名称":"盗","造型":"4008(0,1,0,0,0)","能力编号":"1002","数量":"1","技能":(1512,1531,),"站位":(1,)},
			{"类型":0,"名称":"帮手","造型":"4502(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(2,3,)},
			{"类型":0,"名称":"帮手","造型":"4504(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(4,5,)},
		),
		1003:(
			{"类型":1,"名称":"偷","造型":"4509(0,1,0,0,0)","能力编号":"1002","数量":"1","技能":(1311,1312,),"站位":(1,)},
			{"类型":0,"名称":"帮手","造型":"4502(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(2,3,)},
			{"类型":0,"名称":"帮手","造型":"4504(0,1,0,0,0)","能力编号":"1001","数量":"2","站位":(4,5,)},
		),
	}

	ableInfo = {
		1001:{"等级":"LV","生命":"B*0.3","真气":"B*1","物理伤害":"B*0.3","法术伤害":"B*0.3","物理防御":"B*0.3","法术防御":"B*0.3","速度":"B*1","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"LV","生命":"B*0.4","真气":"B*1","物理伤害":"B*0.4","法术伤害":"B*0.4","物理防御":"B*0.4","法术防御":"B*0.4","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*50+2000,"宠物经验":lambda PLV:PLV*50+2000,"银币":lambda LV:LV*10+500,"物品":[1001]},
		1002:{"经验":lambda LV:LV*50+2000,"宠物经验":lambda PLV:PLV*50+2000,"银币":lambda LV:LV*10+500,"物品":[1002]},
		1003:{"经验":lambda LV:LV*50+2000,"宠物经验":lambda PLV:PLV*50+2000,"银币":lambda LV:LV*10+500,"物品":[1003]},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":100,"物品":"202043","数量":"1","绑定":1},
		),
		1002:(
			{"权重":100,"物品":"202044","数量":"1","绑定":1},
		),
		1003:(
			{"权重":100,"物品":"202045","数量":"1","绑定":1},
		),
	}
#导表结束
	
	def __init__(self):
		customClass.__init__(self)
		self.dRoleEventInfo = {}
		self.dRoleEventNo = {}

	def getEventType(self, iEventNo):
		return self.eventInfo.get(iEventNo, {}).get("事件类型", 0)

	def getEventTime(self, iEventNo):
		return self.eventInfo.get(iEventNo, {}).get("剩余时间", 0)

	def getFightIdx(self, iEventNo):
		return self.eventInfo.get(iEventNo, {}).get("绑定关卡", 0)

	def getEventName(self, iEventNo):
		return self.eventInfo.get(iEventNo, {}).get("事件名称", "")

	def getEventRewardNo(self, iEventNo):
		return self.eventInfo.get(iEventNo, {}).get("奖励编号", 0)

	def getShufferEventNoList(self):
		return shuffleList(self.eventInfo.keys())

	def setEventArgs(self, pid, iEventNo, msg):
		self.dRoleEventInfo[pid] = msg
		self.dRoleEventNo[pid] = iEventNo

	def delEventNo(self, who):
		pid = who.id
		self.dRoleEventNo.pop(who.id, None)
		iEventId = self.dRoleEventInfo.get(pid, {}).get("iEventId", 0)
		self.dRoleEventInfo.pop(pid, None)
		if iEventId:
			collect.service4terminal.sendDelEvent(who, iEventId, 1)

	def onWarWin(self, warObj, npcObj, w):
		customClass.onWarWin(self, warObj, npcObj, w)
		#给奖励
		who = getRole(w.id)
		if not who:
			return

		eventInfo = self.dRoleEventInfo.get(who.id, {})
		if not eventInfo:
			return
		#通知中心服
		collect.service4terminal.rpcB2CCollectWarWin(eventInfo)
		iEventNo = self.dRoleEventNo.get(who.id, 0)
		if not iEventNo:
			return
		who.endPoint.rpcCollectReward(iEventNo)
		rwdIdx = self.getEventRewardNo(iEventNo)
		self.reward(who, rwdIdx, npcObj)


from common import *
import log
import c
import u
import misc
import role
import launch
import props
import types
import collect.service4terminal