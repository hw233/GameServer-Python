# -*-coding:utf-8-*-
'''探宝
'''
import npc.object

class cNpc(npc.object.cNpc):
	def levelCheck(self, who):
		'''等级判断
		'''
		actObj = activity.getActivity("treasure")
		if not actObj:
			return
		openLv = actObj.configInfo.get(1016, 25)
		if who.level < openLv:
			self.say(who, actObj.getText(2433))
			return False
		return True

	def doLook(self, who):
		if not self.levelCheck(who):
			return
		if who.getLeftCubeCount() < 1:
			actObj = activity.getActivity("treasure")
			self.say(who, actObj.getText(2434))
			return
		content = self.getChat()
		selList = []
		content += "\nQ前往探宝"
		selList.append(1)
		content += "\nQ探宝排行"
		selList.append(2)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.treasure(who)
		elif sel == 2:
			self.rank(who)

	def treasure(self, who):
		'''前往探宝
		'''
		pt = team.platform.getPlayerTarget(who)
		if pt and pt.get("automatch") == 1:
			message.tips(who, "自动匹配中无法进行探宝")
			return
		elif who.inTreasure():
			return
		actObj = activity.getActivity("treasure")
		if not actObj:
			return
		pid = who.id
		openLv = 20
		if who.level < openLv:
			self.say(who, actObj.getText(2433))
			return
		if who.getTeamObj():
			actObj.doScript(who, self, "TP2401")
			return
		actObj.enterScene(who)

	def rank(self, who):
		'''探宝排行
		'''
		openUIPanel.openRankUi(who, 10701)


import message
import activity
import money
from common import *
import team.platform
import openUIPanel
