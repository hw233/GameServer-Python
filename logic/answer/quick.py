# -*- coding: utf-8 -*-
# import block.singleton
# import answer.object
from answer.object import cAnswerBase as customActivity

HOUR_MAX_COUNT = 3	#每小时触发抢答题最大数量
TRIGGER_TIME = 10*60	#每10分钟检查触发
ANSWER_TIME = 31	#回答时间，30s,1秒延迟

class Activity(customActivity):
	'''答题-抢答
	'''
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.hour=cycleData.cCycHour(2, self.markDirty)#小时变量
		self.reset()
		# self.lOptions = [1,2,3,4]	#分别代表【正确答案，错误答案1，错误答案2，错误答案13】

	def reset(self):
		'''重置
		'''
		self.bStartAnswer = False #可以回答
		self.lAnswerResult = [] 		#参与本次回答的所有角色ID
		self.lAnswerRoleId = []
		self.iTriggerTime = 0 	#当前触发时间
		self.iProblemNo = 0
		# self.iRightOption = 0 	#正确答案

	def load(self,dData):#override
		customActivity.load(self, dData)
		self.hour.load(dData.pop('h',{}))

	def save(self):#override
		dData = customActivity.save(self)
		dHour=self.hour.save()
		if dHour:
			dData['h']=dHour
		return dData

	def init(self):
		self.autoTimer(False)

	# def shufferOptions(self):
	# 	shuffleList(self.lOptions)

	def nextAutoTimer(self):
		'''计算定时器下一次触发时间
		'''
		curTime = getSecond()
		nextTime = curTime + TRIGGER_TIME

		curtm = time.localtime(curTime)
		nexttm = time.localtime(nextTime)

		nextMin = nexttm[4] - nexttm[4]%10	#每个小时的00、10、20、30、40、50分触发
		nextTime = int(time.mktime((nexttm[0],nexttm[1],nexttm[2],nexttm[3],nextMin,0,0,0,nexttm[8])))
		tmnext = time.localtime(nextTime)

		return nextTime - curTime

	def autoTimer(self, trigger=True):
		'''
		'''
		self.timerMgr.run(self.autoTimer, self.nextAutoTimer(), 0, "cAnswerQuick")
		if trigger:#启服不触发
			self.trigger()

	def checkTrigger(self):
		'''判断能不能触发
		'''
		#每天10:00开始（开服第一天为14:00）
		date = getDatePart()
		startHour = 10
		if date["wday"] == 3:
			startHour = 14
		if date["hour"] < startHour or date["hour"] >= 22:
			return False
		#每个小时最多触发三次抢答题
		if self.hour.fetch("count") >= HOUR_MAX_COUNT:
			return False
		return True

	def triggerRatio(self):
		'''计算是否触发
			30%+15%*N，N等于当前小时内公式判断后未触发抢答题的次数
			当公式判断后触发抢答题，则N的数值重置为0
			在未触发过抢答题的假设下，N的数值为：00分时为0、10分时为1、20分时为2、30分时为3、40分时为4、50分时为5
		'''
		iTriggerCnt = self.hour.fetch("count")
		date = getDatePart()
		iTimes = date["minute"] / 10

		if not iTimes or (iTimes-1) == self.hour.fetch("lastTrigger", -1):
			#0分或者当前小时十分钟前触发了
			n = 0
		else:
			n = max(0, iTimes - self.hour.fetch("count"))

		ratio = min(100, 30+15*n)
		dRatio = {
			1:ratio,
			0:100-ratio,
		}
		result = chooseKey(dRatio, 100)
		if result:	#触发
			self.hour.set("lastTrigger", iTimes)
		return result

	def trigger(self, check=True):
		'''触发刷新题目
		'''
		if check:
			if not self.checkTrigger():
				return
			if not self.triggerRatio():
				return

		self.reset()
		self.iTriggerTime = getSecond()
		self.hour.add("count", 1)

		#随机题目
		# content,lOptionContent = self.getRandQuestion()
		self.randQuestion()
		#广播给客户端
		answer.service.broadcastQuickProblem(self.iProblemNo, 30)
		content = self.getQuestionConfig(self.iProblemNo, "题目内容")
		message.worldMessage("抢答：#C02{}#n".format(content))
		self.timerMgr.run(self.answerEnd, ANSWER_TIME, 0, "trigger_end")
		self.bStartAnswer = True

		sLog = "trigger {}|{}".format(self.hour.fetch("count"), self.iProblemNo)
		self.answerLog("answerQuick", sLog)

	def answerEnd(self):
		'''回答结束
		'''
		sLog = "answerEnd {}|{}".format(self.hour.fetch("count"), self.iProblemNo)
		self.answerLog("answerQuick", sLog)

		self.bStartAnswer = False

		#todo 广播tips
		#广播给客户端
		# answer.service.broadcastQuickResult(self.iRightOption)
		#系统传闻
		sRightResult = self.rightAnswer(self.iProblemNo)
		message.worldMessage('本次抢答题正确的答案是#C02{}#n'.format(sRightResult))

		lRightId = []
		firstRole = None
		for pid,sResult in self.lAnswerResult:
			who = getRole(pid)
			if not who:
				continue
			#正确
			if sResult == sRightResult:
				if not firstRole:
					firstRole = who
					
				lRightId.append(who.id)
				message.tips(who, '恭喜你回答正确，拿好奖励再接再厉！')
				self.answerReward(who, 1002)#抢答答题正确
			else:#错误
				message.tips(who, '回答错误，请拿好安慰奖下次继续努力')
				self.answerReward(who, 1001)#抢答答题错误

		if not lRightId:
			#系统传闻
			message.sysMessageRoll('本次抢答没有人答题正确，请大家下次继续努力')
		if len(lRightId) == 1:
			who = getRole(lRightId[0])
			if who:
				message.sysMessageRoll('本次抢答仅有#C01{}#n答题正确，请大家下次继续努力'.format(who.name))
		elif firstRole:
			message.tips(firstRole, '你取得了本次抢答第一名的宝座')
			self.answerReward(firstRole, 1004)#抢答第一奖
			message.sysMessageRoll('#C01{}#n在本次抢答中夺取了第一名的宝座，大家快来膜拜他！'.format(firstRole.name))

		lRightId = shuffleList(lRightId) 
		iLuckCnt = 0
		# roleNameList = []
		for pid in lRightId:
			who = getRole(pid)
			if not who:
				continue
			# message.tips(who, '你被选为本次抢答的幸运玩家，将获得幸运大奖一份')
			message.tips(who, self.getText(2307))
			# roleNameList.append(who.name)
			self.answerReward(who, 1003)#抢答幸运奖
			iLuckCnt += 1
			if iLuckCnt >= 10:
				break
		# if roleNameList:
			# message.worldMessage('本次抢答获得了幸运大奖的玩家有：#C01{}#n'.format(",".join(roleNameList)))
		self.reset()

	def answerProblem(self, who, sResult):
		'''回答
		'''
		if not self.bStartAnswer:
			message.tips(who, '本次限时抢答已结束，请等待下一次限时抢答')
			return
		if who.id in self.lAnswerRoleId:
			return

		self.lAnswerResult.append((who.id, sResult))
		self.lAnswerRoleId.append(who.id)
		# message.tips(who, '答案提交成功，倒计时结束后将公布正确答案')
		message.tips(who, self.getText(2302))
		#todo 世界频道广播
		content = self.getQuestionConfig(self.iProblemNo, "题目内容")
		message.worldRoleMessage(who.id, sResult)

	def answerReward(self, who, index):
		# sLog = "answerReward {}|{}".format(who.id, index)
		# self.answerLog("answerQuick", sLog)
		self.doScript(who, None, "R{}".format(index))


	def randQuestion(self, uIgnoreNo=()):
		lAllQuestion = QuestionData.gdData.keys()
		for i in uIgnoreNo:
			if i in lAllQuestion:
				lAllQuestion.remove(i)
		self.iProblemNo = lAllQuestion[rand(len(lAllQuestion))]

	def onLogin(self, who, bRelogin):
		'''登录下发抢答
		'''
		if not self.bStartAnswer:
			return
		if who.level < 15:
			return
		duration = max(0, 30 - (getSecond() - self.iTriggerTime))
		if duration > 0:
			msg = {}
			msg["iProblemNo"] = self.iProblemNo
			msg["duration"] = duration
			who.endPoint.rpcAnswerQuickProblem(**msg)


	# def getRandQuestion(self, uIgnoreNo=()):
	# 	lAllQuestion = QuestionData.gdData.keys()
	# 	for i in uIgnoreNo:
	# 		if i in lAllQuestion:
	# 			lAllQuestion.remove(i)

	# 	lAllQuestion = shuffleList(lAllQuestion)
	# 	if not lAllQuestion:
	# 		raise Exception,"没有可用的答题题库数据"

	# 	self.iProblemNo = lAllQuestion[0]
	# 	data = QuestionData.gdData[self.iProblemNo]
	# 	content = data["题目内容"]

	# 	self.shufferOptions()
	# 	self.iRightOption = self.lOptions.index(giRightValue) + 1

	# 	lOptionContent = []
	# 	for option in self.lOptions:
	# 		lOptionContent.append(data[gdOptionTitle[option]])

	# 	return content,lOptionContent


from common import *
from answer.defines import *
import timer
import cycleData
import time
import answer
import answer.service
import message
import answer.service
import QuestionData