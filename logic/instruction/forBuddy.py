# -*- coding: utf-8 -*-
'''宠物相关指令
'''
import instruction

def freeBuddy(ep, target=None):
	'查看周免英雄'
	lst = activity.buddy.getFreeBuddy()
	txtList = []
	for iBuddyNo in lst:
		txtList.append("%d - %s - %s" % (iBuddyNo,buddyData.getConfig(iBuddyNo,"名称"),buddyData.getConfig(iBuddyNo,"类型")))
	message.dialog(target, "\n".join(txtList))

def setBuddyTime(ep,iBuddyNo,iSecond,target=None):
	'修改伙伴时间 参数：伙伴编号 时间（秒数）'
	if iSecond == -1:
		target.buddyCtn.setTime(iBuddyNo,-1)
	else:
		target.buddyCtn.setTime(iBuddyNo,iSecond+getSecond())
	message.tips(target,"修改伙伴时间成功")

def refreshFreeBuddy(ep, target=None):
	'刷新周免伙伴'
	iWeek = getWeekNo()
	oAct = activity.getActivity("buddy")
	lst = oAct.freeBuddyList.pop(iWeek,[])
	oAct.freeBuddyList[iWeek-1] = lst
	oAct.refreshFreeBuddy()
	oAct.markDirty()
	target.buddyCtn.lTimeLimit = []
	for iBuddyNo,iTime in target.buddyCtn.dBuddyTime.iteritems():
		if iTime == -2:
			target.buddyCtn.lTimeLimit.append(iBuddyNo)
	for iBuddyNo in target.buddyCtn.lTimeLimit:
		target.buddyCtn.dBuddyTime.pop(iBuddyNo)
	target.buddyCtn.iWeekNo = 0
	target.buddyCtn.checkAndAddTimeForFreeBubby()
	message.tips(target,"刷新周免伙伴成功")

def setServerLevel(ep, iServerLevel,target=None):
	'设置服务器等级'
	activity.buddy.iServerLevel = iServerLevel
	message.tips(target,"设置服务器等级成功")

from common import *
import activity
import activity.buddy
import buddyData
import message