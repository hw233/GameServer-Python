# -*- coding: utf-8 -*-
from task.defines import *
from task.ring.t30601 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30601
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''入世修行'''
	intro = '''回答$target提出的问题'''
	detail = '''回答$target提出的问题'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(9015,1002)'''
#导表结束

	def getHyperLink(self, who):
		iProblemNo = getattr(who, "ringProblem", None)
		if not iProblemNo:
			return None
		answerObj = answer.getAnswerRingObj()
		data = answerObj.getQuestionConfig(iProblemNo)
		sContent = data["题目内容"]
		iRing = self.getRing(who)
		sLink = "#L2<{},3,{},{}>*[{}]*08#n".format(who.id, self.getUniqueId(), self.id, sContent)
		content = "我在{}环#L1<14,20>*[入世修行]*02#n中遇到难题，题目{}，请各位大大快来帮我解答".format(iRing, sLink)
		return content

	def doneAnswer(self, who, isRight):
		'''答题结果
		'''
		npcObj = self.getTargetNpc()
		if isRight:
			self.doEventScript(who, npcObj, "成功")
			return
		else:
			self.doEventScript(who, npcObj, "失败")
		if getattr(who, "dRingAnswerHelpId", None):
			who.week.add("ringHelp", 1)
		who.dRingAnswerHelpId = {}

	def handleAnswer(self, who, npcObj, *args):
		'''答题
		'''
		answerType = rand(1, 6)
		answerObj = answer.getAnswerRingObj()
		answerObj.openAnswerRing(who, answerType)

	def offerHelp(self, who):
		'''提供帮助
		'''
		owner = self.getOwnerObj()
		answerNo = owner.ringProblem
		if not answerNo:
			message.tips(who, "此入世修行求助已完成")
			return
		answer.service.rpcRingGuildHelpHyperlink(who, owner, answerNo)


from common import *
import answer
import answer.service
import message
