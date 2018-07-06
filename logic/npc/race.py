# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q进入竞技场
Q武勋兑换'''
		
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.enterRace(who)
		elif selectNo == 2:
			self.exchange(who)
			
	def enterRace(self, who):
		'''进入竞技场
		'''
		actObj = activity.getActivity("race")
		if not actObj:
			return
		if not actObj.inReadyTime() and not actObj.inNormalTime():
			actObj.doScript(who, self, "D1001")
			return
		if who.level < 20:
			actObj.doScript(who, self, "D1002")
			return
		if who.getTeamObj():
			actObj.doScript(who, self, "D1003")
			return
		if not actObj.validBuddy(who):
			actObj.doScript(who, self, "D3007")
			return
		pt = team.platform.getPlayerTarget(who)
		if pt and pt.get("automatch") == 1:
			self.say(who, "你处于#C04队伍匹配#n中，不能进入单人竞技场")
			return
		actObj.enterScene(who)
	
	def exchange(self, who):
		'''武勋兑换
		'''
		shop.openPropsExchange(who, 200007)
		

import activity
import message
import shop
import team.platform