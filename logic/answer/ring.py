# -*- coding: utf-8 -*-
# import answer.object
from answer.object import cAnswerBase as customActivity

class Activity(customActivity):
	'''答题-任务链
	'''

	def randQuestion(self, who, qtype):
		'''抽题
		'''
		lAllQuestion = QuestionData.gdData.keys()
		lChoose = []
		for i in lAllQuestion:
			if QuestionData.gdData[i].get("类型") == qtype:
				lChoose.append(i)
		if not lChoose:
			return 0
		return lChoose[rand(len(lChoose))]

	def openAnswerRing(self, who, qtype):
		'''打开任务链答题界面
		'''
		problemNo = getattr(who, "ringProblem", None)
		if not problemNo:
			problemNo = self.randQuestion(who, qtype)
			who.ringProblem = problemNo
		if not problemNo:
			raise Exception, "找不到类型为{}的题库".format(qtype)
		helpCnt = rand(5)
		answer.service.ringProblem(who, problemNo, helpCnt)

	def answerProblem(self, who, sResult):
		'''回答
		'''
		problemNo = who.ringProblem
		if not problemNo:
			raise Exception,"答题-任务链：{}没有生成题目就答题".format(who.id)
		bRight = self.isRightAnswer(problemNo, sResult)
		dAnswerHelpId = getattr(who, "dRingAnswerHelpId", {})
		if dAnswerHelpId:
			helpRids = dAnswerHelpId.get(sResult)
			if helpRids:
				helper = getRole(helpRids[0])
				txt = "#C01{}#n的#L1<14,20>*[入世修行]*02#n求助已被#C01{}#n完成".format(who.name, helper.name if helper else "盟友")
				message.guildMessage(who.getGuildId(), txt)
		self.answerReward(who, bRight)
		who.ringProblem = None

	def answerReward(self, who, isRightAnswer):
		'''奖励
		'''
		taskObj = task.hasTask(who, 30601)
		if taskObj and taskObj.id == 30605:
			taskObj.doneAnswer(who, isRightAnswer)


from common import *
from answer.defines import *
import answer
import answer.service
import message
import QuestionData
# import openUIPanel
import task
