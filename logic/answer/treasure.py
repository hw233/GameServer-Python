# -*- coding: utf-8 -*-
# import answer.object
from answer.object import cAnswerBase as customActivity

class Activity(customActivity):
	'''答题-探宝
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

	def openAnswerTreasure(self, who, qtype):
		'''打开探宝答题界面
		'''
		problemNo = self.randQuestion(who, qtype)
		if not problemNo:
			raise Exception, "找不到类型为{}的题库".format(qtype)
		who.treasureProblem = problemNo
		# openUIPanel.openAnswerProblem(who)#是否需要通知打开
		answer.service.treasureProblem(who, problemNo)

	def answerProblem(self, who, sResult):
		'''回答
		'''
		problemNo = who.treasureProblem
		if not problemNo:
			raise Exception,"答题-探宝：{}没有生成题目就答题".format(who.id)
		bRight = self.isRightAnswer(problemNo, sResult)
		self.answerReward(who, bRight)

	def answerReward(self, who, isRightAnswer):
		'''奖励
		'''
		actObj = activity.treasure.getActivity()
		if isRightAnswer:
			content = actObj.getText(2417)
			activity.treasure.tipsAndMessage(who, content)
			actObj.doScript(who, None, "R2002")
		else:
			content = actObj.getText(2418)
			activity.treasure.tipsAndMessage(who, content)
		actObj.doneEvent(who, isRightAnswer)



from common import *
from answer.defines import *
import answer
import answer.service
import message
import QuestionData
# import openUIPanel
import activity.treasure
