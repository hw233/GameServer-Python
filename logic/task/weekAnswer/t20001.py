# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 20001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''天问初试-第1题'''
	intro = '''前往$target处答题'''
	detail = '''前往$target处完成天问初试的第1题答题'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''$EXAM1001'''

	npcInfo = {
	}

	eventInfo = {
		1001:{"点击":"LOOK","成功":"DONE，T20002"},
		1002:{"点击":"LOOK","成功":"DONE，T20003"},
		1003:{"点击":"LOOK","成功":"DONE，T20004"},
		1004:{"点击":"LOOK","成功":"DONE，T20005"},
		1005:{"点击":"LOOK","成功":"DONE，T20006"},
		1006:{"点击":"LOOK","成功":"DONE，T20007"},
		1007:{"点击":"LOOK","成功":"DONE，T20008"},
		1008:{"点击":"LOOK","成功":"DONE，T20009"},
		1009:{"点击":"LOOK","成功":"DONE，T20010"},
		1010:{"点击":"LOOK","成功":"DONE，T20011"},
		1011:{"点击":"LOOK","成功":"DONE，T20012"},
		1012:{"点击":"LOOK","成功":"DONE，T20013"},
		1013:{"点击":"LOOK","成功":"DONE，T20014"},
		1014:{"点击":"LOOK","成功":"DONE，T20015"},
		1015:{"点击":"LOOK","成功":"DONE，T20016"},
		1016:{"点击":"LOOK","成功":"DONE，T20017"},
		1017:{"点击":"LOOK","成功":"DONE，T20018"},
		1018:{"点击":"LOOK","成功":"DONE，T20019"},
		1019:{"点击":"LOOK","成功":"DONE，T20020"},
		1020:{"点击":"LOOK","成功":"DONE"},
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		100001:'''你若自认有几分学识，就来接受天问吧！''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"$npc","造型":"$npc","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(5409,5408,5407,),"站位":(1,)},
			{"类型":0,"名称":"保镖","造型":"3008(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"1","技能":(5401,),"站位":(6,)},
			{"类型":0,"名称":"护卫","造型":"4506(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"2","技能":(5401,5410,),"站位":(7,8,)},
		),
		1002:(
			{"类型":1,"名称":"$npc","造型":"$npc","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(5409,5408,5407,),"站位":(1,)},
			{"类型":0,"名称":"保镖","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"1","技能":(5401,),"站位":(6,)},
			{"类型":0,"名称":"护卫","造型":"4508(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"2","技能":(5401,5410,),"站位":(7,8,)},
		),
		1003:(
			{"类型":1,"名称":"$npc","造型":"$npc","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(5409,5408,5407,),"站位":(1,)},
			{"类型":0,"名称":"保镖","造型":"3015(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"1","技能":(5401,),"站位":(6,)},
			{"类型":0,"名称":"护卫","造型":"4506(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2002","数量":"2","技能":(5401,5410,),"站位":(7,8,)},
		),
	}

	ableInfo = {
		2001:{"等级":"LV+1","生命":"B*0.1","真气":"B*0.1","物理伤害":"B*0.1","法术伤害":"B*0.1","物理防御":"B*0.1","法术防御":"B*0.1","速度":"B*0.1","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2002:{"等级":"LV","生命":"B*0.1","真气":"B*0.1","物理伤害":"B*0.1","法术伤害":"B*0.1","物理防御":"B*0.1","法术防御":"B*0.1","速度":"B*0.1","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	configInfo = {
		"生成路径":"weekAnswer",
	}
#导表结束
	def __init__(self, _id):
		customTask.__init__(self, _id)
		self.iExamNo = self.id%20000

	def onBorn(self, who, npcObj, **kwargs):#override
		'''
		'''
		customTask.onBorn(self, who, npcObj, **kwargs)
		#定时
		datePart = getDatePart()
		lEndTime = []
		lEndTime.append(datePart["year"])
		lEndTime.append(datePart["month"])
		lEndTime.append(datePart["day"])
		lEndTime.append(22)
		lEndTime.append(0)
		lEndTime.append(0)

		iEndTime = getSecond(*lEndTime)
		leftTime = iEndTime - getSecond()
		self.setTime(leftTime) # 计时任务

	def canAbort(self):#override
		'''是否可以放弃任务
		'''
		return 0

	def isValid(self):
		'''是否有效
		'''
		firstExamObj = answer.getAnswerFirstExamObj()
		if firstExamObj:
			if firstExamObj.isInAnswerTime():
				return 1
			else:
				return 0
		return customTask.isValid(self)

	def delayGoAhead(self, who):
		self.timerMgr.run(functor(self.autoGoAhead, who.id), 1, 0, "firstExamTask_%s%s"%(self.id, who.id))

	def autoGoAhead(self, pid):
		who = getRole(pid)
		if who:
			self.goAhead(who)

	def goAhead(self, who):#override
		'''前往
		'''
		firstExamObj = answer.getAnswerFirstExamObj()
		if not firstExamObj.isInAnswerTime():
			message.tips(who, firstExamObj.getText(2326))
			task.removeTask(who, self.id)
			return
		if who.inTeam():
			message.tips(who, firstExamObj.getText(2321, who.id))
			return
		customTask.goAhead(self, who)

	def getTargetNpc(self):#override
		'''目标npc
		'''
		firstExamObj = answer.getAnswerFirstExamObj()
		npcObj = firstExamObj.getNpcObjByExamNo(self.iExamNo)
		return npcObj

	def onWarWin(self, warObj, npcObj, w):
		'''战斗胜利时
		'''
		# customTask.onWarWin(self, warObj, npcObj, w)
		who = getRole(w.id)
		if who:
			firstExamObj = answer.getAnswerFirstExamObj()
			firstExamObj.answerWarWin(who, self)
		
	
	def onWarFail(self, warObj, npcObj, w):
		'''战斗失败时
		'''
		customTask.onWarFail(self, warObj, npcObj, w)
		who = getRole(w.id)
		if who:
			firstExamObj = answer.getAnswerFirstExamObj()
			firstExamObj.answerWarFail(who, self)

	def customFight(self, who):
		fightKeys = self.fightInfo.keys()
		iRandFightIdx = fightKeys[rand(len(fightKeys))]
		self.doScript(who, self.getTargetNpc(), "F{}".format(iRandFightIdx))

	def customEvent(self, who, npcObj, eventName, *args):
		m = re.match("EXAM(\d+)", eventName)
		if m:
			eventIdx = int(m.group(1))
			npcObj = self.getTargetNpc()
			self.bindEvent(npcObj.idx, eventIdx)

	def getNpcByIdx(self, npcIdx):
		if npcIdx in xrange(1001,1021):
			return self.getTargetNpc()
		return customTask.getNpcByIdx(self, npcIdx)

import copy
from common import *
import answer
import answer.firstExam
import message
import task
