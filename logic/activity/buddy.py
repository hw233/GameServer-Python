# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.freeBuddyList = {}

	def save(self):
		data = customActivity.save(self)
		data["freeBuddy"] = self.freeBuddyList
		return data
	
	def load(self, data):
		customActivity.load(self, data)
		self.freeBuddyList = data.pop("freeBuddy",{})

	def getFreeBuddy(self):
		iWeek = getWeekNo()
		lst = self.freeBuddyList.get(iWeek)
		if not lst:
			lst = self.refreshFreeBuddy()
		return lst

	def getLastFreeBuddy(self):
		iWeek = getWeekNo()
		return self.freeBuddyList.get(iWeek-1,[])

	def refreshFreeBuddy(self): #刷新周免伙伴 比较恶心 求优化
		iWeek = getWeekNo()
		dFreeBuddy = {}    #已选取的本周周免伙伴 {"类型"：[编号]}
		dBuddy = {}	       #符合条件的伙伴 {"类型"：[编号]}
		lBuddy = []        #符合条件的伙伴
		level = openLevel.getOpenLevel()
		for iBuddyNo,dData in buddyData.gdData.iteritems():
			if iBuddyNo in [1001,2001,3001,4001,5001]:
				continue
			if dData["开启等级"] > level:
				continue
			sType = dData["类型"]
			tTime = dData.get("必出周免")
			if tTime and iWeek == getWeekNo(getSecond(*tTime)):
				dFreeBuddy[sType] = iBuddyNo #先抽取时间符合的
			else:
				lst = dBuddy.setdefault(sType,[])
				lst.append(iBuddyNo)
		for sType,lst in dBuddy.iteritems():
			if sType not in dFreeBuddy:    #每个类型抽取一个
				dFreeBuddy[sType] = lst.pop(rand(len(lst)))
			lBuddy.extend(lst)

		if lBuddy:
			dFreeBuddy["last"] = lBuddy[rand(len(lBuddy))]  #每个类型抽完后再随机抽一个

		self.freeBuddyList.pop(iWeek-2,[])
		self.freeBuddyList[iWeek] = dFreeBuddy.values()
		self.markDirty()
		return self.freeBuddyList[iWeek]

def getFreeBuddy():
	oAct = activity.getActivity("buddy")
	return oAct.getFreeBuddy()

def getLastFreeBuddy():
	oAct = activity.getActivity("buddy")
	return oAct.getLastFreeBuddy()

from common import *
import buddyData
import activity
import openLevel