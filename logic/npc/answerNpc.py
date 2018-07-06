# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		answerDayObj = answer.getAnswerDayObj()
		sReason = answerDayObj.canDayAnswer(who)
		if sReason:
			self.say(who, sReason)
			return

		content = "每日答题已经开始，快来答题吧"#self.getChat()
		content += "\nQ每日答题"
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			answerDayObj = answer.getAnswerDayObj()
			answerDayObj.openAnswerDay(who)

from common import *
import answer
import message
