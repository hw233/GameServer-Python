# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"无名游侠","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0,0","位置":"1130,56,91,4","称谓":"门派试炼"},
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		1001:'''六大门派弟子广布天下，其中不乏武力高强深藏不露者。你们要去和他们切磋下吗？\nQ以武会友\nQ快捷组队\nQ规则说明''',
		1002:'''对方人多势众，活动需要#C04队伍人数≥3#n''',
		1003:'''请先召回暂离队员''',
		1004:'''刀剑无眼，不要带上小朋友。玩家#C04等级需≥40级#n''',
		1005:'''你已经有任务，快去完成吧''',
		1006:'''#C03$map#n的#C02$target#n集合了一群众门派弟子在等待你们去挑战，快去证明自己吧！''',
		1007:'''少侠们好武功，青出于蓝而胜于蓝。你们的成绩是#C02$time#n''',
		1008:'''你们一共闯过了#C02$number#n关，功力还是稍欠火候，准备一下再来继续挑战吧。''',
		1009:'''蜀山弟子''',
		1010:'''唐门弟子''',
		1011:'''武林盟弟子''',
		1012:'''魔宫弟子''',
		1013:'''苗疆弟子''',
		1014:'''佛门弟子''',
		1015:'''该我出手了，你们注意啦''',
		1016:'''1.玩家等级≥#C0240级#n，队伍人数≥#C023#n\n2.试炼战斗为各大门派弟子#C02车轮战#n，通过每轮战斗恢复一定的#C02生命和真气#n\n3.每人只能获取#C021次#n通关奖励，可通过继续挑战改变自己的#C02成绩#n\n4.成绩最好的#C02前3名#n队伍可获得#C02特殊称谓#n''',
		6001:'''$rolename在#L1<14,25>*[门派试炼]*02#n中表现出色，获得了$lnkProps''',
		6002:'''#L1<14,25>*[门派试炼]*02#n将在#C0220:00#n准时开始，请各位仙友做好准备，前往等待活动开始''',
		6003:'''#L1<14,25>*[门派试炼]*02#n已经开始，已经准备好的仙友快前往领取任务，挑战诸大门派''',
		6004:'''本次#L1<14,25>*[门派试炼]*02#n已经结束，表现最好的队伍为：#C01$team1#n（#C02$time1#n）获得第一名''',
		6005:'''本次#L1<14,25>*[门派试炼]*02#n已经结束，表现最好的队伍为：#C01$team1#n（#C02$time1#n）获得第一名;#C01$team2#n（#C02$time2#n）获得第二名''',
		6006:'''本次#L1<14,25>*[门派试炼]*02#n已经结束，表现最好的队伍为：#C01$team1#n（#C02$time1#n）获得第一名;#C01$team2#n（#C02$time2#n）获得第二名;#C01$team3#n（#C02$time3#n）获得第三名''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.teamInfoList = {} # 活动队伍信息列表

	def inNormalTime(self):
		'''是否活动正式时间
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		if wday not in (1, 3):
			return False
		if hour not in (20, 21,):
			return False
		return True

	def init(self):
		if self.inNormalTime():
			self.begin()

	def begin(self):
		'''开始活动
		'''
		self.state = 1
		self.teamInfoList = {}
		self.timerMgr.run(self.actNotify, 0, 1800, "actNotify")
		self.npcObj = self.addNpc(1001, "npc")

	def end(self):
		'''结束活动
		'''
		if self.timerMgr.hasTimerId("actNotify"):
			self.timerMgr.cancel("actNotify")
		self.recordRank()
		self.state = 0
		self.removeNpc(self.npcObj)

	def beginNotify(self, nextTime):
		'''开启通知
		'''
		if nextTime == 300:
			self.timerMgr.run(functor(self.beginNotify, 240), nextTime, 0, "beginNotify")
		elif nextTime == 240:
			self.timerMgr.run(functor(self.beginNotify, None), nextTime, 0, "beginNotify")
		txt = self.getText(6002)
		message.sysMessageRoll(txt)

	def actNotify(self):
		'''活动通知
		'''
		if 22 == getDatePart(partName="hour"):
			return
		txt = self.getText(6003)
		message.sysMessageRoll(txt)

	def onNewHour(self, day, hour, wday):
		if wday not in (1, 3):
			return
		if self.inNormalTime():
			if self.state == 0:
				self.begin()
		else:
			if self.state != 0:
				self.end()
		if hour == 19:
			self.timerMgr.run(functor(self.beginNotify, 300), 3000, 0, "beginNotify")

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		return Npc(self)

	def getSurplusTime(self):
		if self.state == 0:
			return 0
		i = getSecond()
		t=time.localtime(i)
		#直接对hour加1,即使当前是23点,也不会有问题
		return int(time.mktime((t[0],t[1],t[2],22,0,0,0,0,t[8])))-i #t[8]是否是夏令时之类的

	def recordTime(self, roleIdList, warTime):
		if not self.state:
			return
		roleIdList = tuple(roleIdList)
		oldTime = self.teamInfoList.get(roleIdList)
		if not oldTime or oldTime > warTime:
			self.teamInfoList.update({roleIdList:warTime})

	def recordRank(self):
		'''记录排名
		'''
		if not self.teamInfoList:
			return
		orderList = [(k, v) for k, v in self.teamInfoList.iteritems()]
		orderList.sort(cmp=lambda e1, e2: cmp(e1[1], e2[1]))
		top3TimeList = orderList[:3] if len(orderList) > 3 else orderList[:]
		top3Teams = []
		for k, v in self.teamInfoList.iteritems():
			if (k, v) in top3TimeList:
				top3Teams.append((k, v))
		txt = self.getText(6004 + len(top3TimeList) - 1)
		for idx, teamRecord in enumerate(top3TimeList):
			txt = txt.replace("$team{}".format(idx+1), self.transTeamNames(teamRecord[0]))
			txt = txt.replace("$time{}".format(idx+1), formatTime(teamRecord[1]))
		message.sysMessageRoll(txt)
		tmpIdList = []
		for idx, (roleIdList, warTime) in enumerate(top3Teams):
			titleNo = 40303 - idx
			for roleId in roleIdList:
				if roleId in tmpIdList:
					continue
				who = getRole(roleId)
				if not who:
					offlineHandler.addHandler(roleId, "schoolFightTile", titleNo=titleNo)
					continue
				title.newTitle(who, titleNo)
				tmpIdList.append(roleId)

	def transTeamNames(self, roleIdList):
		nameList = []
		for roleId in roleIdList:
			resumeObj = resume.getResume(roleId)
			nameList.append(resumeObj.fetch("name"))
		return "、".join(nameList)

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 101:
			if self.state != 1:
				self.begin()
		elif cmdIdx == 102:
			if self.state != 0:
				self.end()
		elif cmdIdx == 103:
			self.recordRank()


import activity.object

class Npc(activity.object.Npc):
	'''活动npc
	'''
	def doLook(self, who):
		content = getActivity().getText(1001)
		selList = [1, 2, 3]
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.takeTask(who)
		elif sel == 2:
			self.speedyTeam(who)
		elif sel == 3:
			self.taskDesc(who)

	def takeTask(self, who):
		'''门派试炼任务
		'''
		actObj = getActivity()
		if task.hasTask(who, 20101):
			self.say(who, actObj.getText(1005))
			return
		taskObj = task.getTask(20101)
		if not taskObj:
			return
		if not taskObj.taskAddCheck(who, self):
			return
		taskObj = task.newTask(who, self, 20101)
		if not taskObj:
			return
		npcObj = taskObj.getTargetNpc()
		mapName = scene.getScene(npcObj.sceneId).name
		content = getActivity().getText(1006)
		content = content.replace("$map", mapName)
		content = content.replace("$target", npcObj.name)
		self.say(who, content)

	def speedyTeam(self, who):
		'''打开便捷组队界面
		'''
		team.platformservice.quickMakeTeam(who, 6)

	def taskDesc(self, who):
		actObj = getActivity()
		self.say(who, actObj.getText(1016))


def getActivity():
	return activity.getActivity("schoolFight")


import time
from common import *
import activity
import message
import task
import team
import resume
import title
import scene
import offlineHandler
