# -*-coding:utf-8-*-
'''运镖
'''
import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		content = self.getChat()
		content += '''
Q我要运镖'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.escort(who)

	def escort(self, who):
		'''领取运镖任务
		'''
		pt = team.platform.getPlayerTarget(who)
		if pt and pt.get("automatch") == 1:
			message.tips(who, "自动匹配中无法接取运镖任务")
			return
		elif who.inEscort():
			return
		actObj = activity.getActivity("escort")
		if not actObj:
			return
		pid = who.id
		iCash = actObj.getDeposit()
		actPoint = actObj.getNeedActPoint()
		maxCnt = actObj.getMaxCount()
		openLv = actObj.getOpenLevel()
		if who.day.fetch("escort") >= maxCnt:
			actObj.doScript(who, self, "TP1001")
			return
		if who.level < openLv:
			actObj.doScript(who, self, "TP1002")
			return
		if who.getTeamObj():
			actObj.doScript(who, self, "TP1003")
			return
		if who.day.fetch("actPoint") < actPoint:
			actObj.doScript(who, self, "TP1004")
			return
		message.confirmBoxNew(who, self.responseGiveTask, actObj.getText(1007, who.id))
		
	def responseGiveTask(self, who, yes):
		if not yes:
			return
		
		actObj = activity.getActivity("escort")
		if not actObj:
			return
		iCash = actObj.getDeposit()
		if not money.checkCash(who, iCash):
			return

		who.addCash(-iCash, "运镖押金", None)
		message.message(who, "扣除运镖押金#R<{},3,2>#n".format(iCash))
		actObj.doEscort(who, self)


import message
import activity
import money
from common import *
import team.platform
