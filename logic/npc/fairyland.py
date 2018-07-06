# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		if who.level < 40:
			self.say(who, content)
			return
			
		content += '''
Q试炼幻境
Q规则说明'''
		
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.enterFairyland(who)
		elif selectNo == 2:
			self.detailFairyland(who)
			
	def enterFairyland(self, who):
		'''进入试炼幻境
		'''
		actObj = activity.getActivity("fairyland")
		if not actObj:
			return
		if actObj.isFailAll(who):
			actObj.doScript(who, self, "D4001")
			return
		if actObj.isPassAll(who):
			actObj.doScript(who, self, "D4002")
			return

		actObj.sendInfoMsg(who)
	
	def detailFairyland(self, who):
		'''武勋兑换
		'''
		actObj = activity.getActivity("fairyland")
		if not actObj:
			return
		actObj.doScript(who, self, "D4003")
		

import activity
import message
import shop