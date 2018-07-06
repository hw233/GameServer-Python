# -*- coding: utf-8 -*-
# import answer.object
# import block.singleton
from answer.object import cAnswerBase as customActivity
from activity.object import Npc as customNpc

giStartHour = 12
giEndHour = 21

class Activity(customActivity):
	'''答题-天问初试
	'''
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.week=cycleData.cCycWeek(2, self.markDirty)
		self.reset()
		#每道题目有一个排行榜
		self.dFirstExamRank = {}

	def init(self):
		if self.isInAnswerTime():#起服在答题期间，创建NPC
			self.createFirstExamNpc()
		#放到最后import死循环了
		import rank.firstExam
		iMaxAnswerCnt = self.maxAnswerCnt()
		#这里的排行榜不会显示给玩家看
		for iExamNo in xrange(1, iMaxAnswerCnt):
			rankObj = rank.firstExam.cRanking(0, 0, "乡试-{}".format(iExamNo), "rank_firstExam_{}".format(iExamNo), 200)
			if not rankObj._loadFromDB():
				rankObj._insertToDB(*rankObj.getPriKey())
			# rankObj.startTimer()	#即时刷新不走定时器
			self.dFirstExamRank[iExamNo] = rankObj
		#最后一个排行榜在这里，会显示给玩家看
		self.dFirstExamRank[iMaxAnswerCnt] = rank.getRankObjByName("rank_firstExam_{}".format(iMaxAnswerCnt))

	def reset(self):
		'''重置
		'''
		self.dExamNpc = {}
		self.dExamNpcIdx = {}

	def load(self,dData):#override
		customActivity.load(self, dData)
		self.week.load(dData.pop('w',{}))

	def save(self):#override
		dData = customActivity.save(self)
		dHour=self.week.save()
		if dHour:
			dData['w']=dHour
		return dData

	def maxAnswerCnt(self):
		'''最多答题数量
		'''
		return self.getConfigInfo(2001)

	def isInGetTaskTime(self):
		'''周六12:00-21:00期间玩家可以在“天问初试NPC1”处领取“初试答题任务1”
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour >= 12 and curHour < 21:
			return True
		return False

	def isInAnswerTime(self):
		'''周六12:00-22:00期间 身上接有任一“初试答题任务”的玩家可与对应“天问初试NPC”对话进行答题
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour >= 12 and curHour < 22:
			return True
		return False

	def isInFirstExamTime(self):
		'''周六12:00-20:00期间
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour >= 12 and curHour < 20:
			return True
		return False

	def isInSeconExamTime(self):
		'''周六21:00-22:00期间
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour >= 21 and curHour < 22:
			return True
		return False

	def onNewHour(self, day, hour, wday):
		'''系统刷小时
		'''
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return
		curHour = date["hour"]
		if curHour == 12:
			#清空排行榜
			self.resetRank()
			#显示固定NPC
			self.createFirstExamNpc()
		elif curHour == 20:#发放金章之试参与资格
			self.timerHandFinalExam()
		elif curHour == 22:#删除NPC
			self.deleteFirstExamNpc()

	def createFirstExamNpc(self):
		'''创建NPC放入场景
		'''
		self.answerLog("firstExam", "createFirstExamNpc")
		self.deleteFirstExamNpc()
		# iMaxAnswerCnt = self.maxAnswerCnt()
		for idx,npcIdx in enumerate(xrange(1001, 1021)):
			npcObj = self.addNpc(npcIdx, "firstExam")
			# npcObj = self.addWeekAnswerNpc(npcIdx)
			npcObj.iExamNo = idx+1

			self.dExamNpc[idx+1] = npcObj
			self.dExamNpcIdx[npcIdx] = npcObj.id

	# def addWeekAnswerNpc(self, npcIdx):
	# 	'''npc需要加入场景
	# 	'''
	# 	npcObj = self.newWeekAnswerNpcByIdx(npcIdx)
	# 	scene.switchSceneForNpc(npcObj, npcObj.sceneId, npcObj.x, npcObj.y, npcObj.d)
	# 	npc.gdCacheNpc[npcIdx] = npcObj
	# 	return npcObj

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		if npcIdx == 1001:
			return NpcFirst(self)
		elif npcIdx in xrange(1002, 1021):
			return NpcOther(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def deleteFirstExamNpc(self):
		'''删除NPC
		'''
		self.answerLog("firstExam", "deleteFirstExamNpc")
		# for _,npcObj in self.dExamNpc.iteritems():
		# 	self.onRemoveAnswerNpc(npcObj)
		self.removeNpcByTypeFlag("firstExam")
		self.dExamNpc = {}
		self.dExamNpcIdx = {}

	# def onRemoveAnswerNpc(self, npcObj):
	# 	'''移除npc时
	# 	'''
	# 	npc.gdCacheNpc.pop(npcObj.idx, None)
	# 	if hasattr(npcObj, "remove"):
	# 		npcObj.remove()

	def getExamNpcObjByIdx(self, npcIdx):
		return self.dExamNpcIdx.get(npcIdx, 0)

	def getNpcObjByExamNo(self, iExamNo):
		'''根据题目编号获取NPC
		'''
		return self.dExamNpc.get(iExamNo, None)

	def transString(self, content, pid=0):
		'''转化字符串
		'''
		content = customActivity.transString(self, content, pid)
		who = None
		if pid:
			who = getRole(pid)
		if who:
			if "$kemu" in content:
				tmp = self.questionTypeInfo.get(who.week.fetch("firstExamSelect", 0), "未知")
				content = content.replace("$kemu", tmp)
		return content

	def errAddTime(self):
		'''回答错误增加秒数
		'''
		return self.getConfigInfo(3001)

	def randQuestionNo(self, who):
		'''随机问题
		'''
		firstExamSelect = who.week.fetch("firstExamSelect", 1)
		if not firstExamSelect:
			if config.IS_INNER_SERVER:
				message.tips(who, "没有选择答题类型就开始答题")
			raise Exception,'没有选择答题类型就开始答题：{}'.format(firstExamSelect)
		lQuestionNo = answer.getQuestionClassify(firstExamSelect)
		lAnswerRight = who.week.fetch("FEAnswerRight", [])
		for iQuesNo in lAnswerRight:	#去除回答正确的题目
			if iQuesNo in lQuestionNo:
				lQuestionNo.remove(iQuesNo)

		iLastQuesNo = who.week.fetch("FEErrorNo", 0)
		if iLastQuesNo in lQuestionNo:	#去除上一回答错误题目
			lQuestionNo.remove(iLastQuesNo)

		if not lQuestionNo:
			if config.IS_INNER_SERVER:
				message.tips(who, "周答题没有合适的题目")
			raise Exception,'周答题没有合适的题目：{}|{}|{}'.format(firstExamSelect, lQuestionNo, lAnswerRight)

		iQuestionNo = lQuestionNo[rand(len(lQuestionNo))]
		return iQuestionNo

	def openFirstExamUI(self, who, rand=False):
		'''打开答题界面
		'''
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if not taskObj:
			return
		dFirstExamNo =  who.week.fetch("firstExamNo", {})
		iQuestionNo = dFirstExamNo.get(taskObj.iExamNo, 0)
		if not iQuestionNo or rand:
			iQuestionNo = self.randQuestionNo(who)
			dFirstExamNo[taskObj.iExamNo] = iQuestionNo
			who.week.set("firstExamNo", dFirstExamNo)
		answer.service.rpcFirstExamQuestion(who, iQuestionNo, taskObj.iExamNo, self.getFirstAnswerTime(who, taskObj.iExamNo))
		self.setStartAnswer(who)	#为了不能被队伍匹配、邀请

	def answerWarWin(self, who, taskObj):
		'''战斗胜利时
		'''
		message.tips(who, self.getText(2332))
		self.answerFirstExam(who, None, True)

	def answerWarFail(self, who, taskObj):
		'''战斗失败时
		'''
		message.tips(who, self.getText(2333))
		self.answerFirstExam(who, None, False)

	def answerFirstExam(self, who, sResult, bFightWin=None):
		'''回答
		'''
		self.setEndAnswer(who)
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if not taskObj:
			return
		iExamNo = taskObj.iExamNo
		dFirstExamNo =  who.week.fetch("firstExamNo", {})
		iQuestionNo = dFirstExamNo.get(iExamNo, 0)
		if not iQuestionNo:
			raise Exception,'没有生成题目就答题'
			# return
		#记录完成时间
		dFirstExamComTime = who.week.fetch("FEComTime", {})
		dFirstExamComTime[iExamNo] = getSecond()
		who.week.set("FEComTime", dFirstExamComTime)
		if bFightWin or self.isRightAnswer(iQuestionNo, sResult):
			#记录回答正解编号
			lAnswerRight = who.week.fetch("FEAnswerRight", [])
			lAnswerRight.append(iQuestionNo)
			who.week.set("FEAnswerRight", lAnswerRight)
			if sResult:	#战斗不用提示
				message.tips(who, self.getText(2331))
			self.doScript(who, None, "R{}".format(3001))
			self.answerRewardProps(who, iExamNo)
			who.week.add("firstExmaRightN", 1)#连续正确题数
		else:	
			who.week.set("FEErrorNo", iQuestionNo)
			#记录错误次数，时间加20秒
			dAnswerError = who.week.fetch("FEError", {})
			dAnswerError[iExamNo] = dAnswerError.get(iExamNo, 0) + 1
			who.week.set("FEError", dAnswerError)
			# who.week.add("firstExamErr", 1)
			who.week.set("firstExmaRightN", 0)#连续正确题数
			if sResult:
				message.tips(who, self.getText(2330))
			self.doScript(who, None, "R{}".format(3004))
			#重新抽取一题作为题目
			# self.openFirstExamUI(who, True)

		#加活跃
		perPoint = activity.center.getPerActPoint(17)
		who.addActPoint(perPoint)

		#更新排行榜
		self.updateRank(who, iExamNo)
		iUseTime = self.getFirstAnswerTime(who, iExamNo)	#耗时
		who.endPoint.rpcFirstExamComplete(iUseTime)
		if not self.isInAnswerTime():	#时间已结束
			message.tips(who, self.getText(2326))
			return

		#给下个题目
		taskObj.doEventScript(who, taskObj.getTargetNpc(), "成功")
		rankObj = self.dFirstExamRank.get(iExamNo, None)
		sTime = formatTime(iUseTime)
		iRank = rankObj.getRank(who.id)
		iMaxCnt = self.maxAnswerCnt()
		if iExamNo == iMaxCnt:
			if self.isInFirstExamTime():
				message.tips(who, "你已完成本周天问初试的所有答题，目前共耗时#C02{}#n，排名为#C02{}#n，请关注#C0220:00#n的#C02金章之试#n名单公布！".format(sTime, iRank))#2328
			else:
				message.tips(who, self.getText(2329, who.id))
		else:
			# print "self.isInFirstExamTime()=",self.isInFirstExamTime()
			if self.isInFirstExamTime():
				message.tips(who, "你已经完成#C02第{}题#n的初试答题，目前共耗时#C02{}#n，排名为#C02{}#n，请前往下一名考官处继续答题吧！".format(iExamNo, sTime, iRank))#2327
			else:
				message.tips(who, "你已经完成#C02第{}题#n的初试答题，请前往下一名考官处继续答题吧".format(iExamNo))

		#前往下一任务NPC
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj:
			if bFightWin!=None:
				taskObj.delayGoAhead(who)
			else:
				taskObj.goAhead(who)

	def answerRewardProps(self, who, iExamNo):
		'''	连续答对五道可获得一个203031
			连续答对十道可获得一个203032
		'''
		dAnswerError = who.week.fetch("FEError", {})
		iLastFive = who.week.fetch("FE_FRight", 0)
		iLastTen = who.week.fetch("FE_TRight", 0)
		#连续正确的题数
		iFiveRightCnt = 0
		iTenRightCnt = 0
		for index in xrange(iExamNo, 0, -1):
			if dAnswerError.get(index, 0):
				break
			if index > iLastFive:
				iFiveRightCnt += 1
			if index > iLastTen:
				iTenRightCnt += 1

		if iFiveRightCnt >= 5:
			self.doScript(who, None, "R{}".format(3002))
			message.tips(who, "你已连续答对五道题目，获得了一个#C02{}#n".format(props.getPropsName(self.getConfigInfo(2003))))
			who.week.set("FE_FRight", iExamNo)#记录最后一次连续对5题

		if iTenRightCnt >= 10:
			self.doScript(who, None, "R{}".format(3003))
			message.tips(who, "你已连续答对十道题目，获得了一个#C02{}#n".format(props.getPropsName(self.getConfigInfo(2004))))
			who.week.set("FE_TRight", iExamNo)#记录最后一次连续对10题

	def useProps(self, who, propsNo):
		'''使用道具
		'''
		if not self.isInAnswerTime():
			message.tips(who, self.getText(2326))
			return
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if not taskObj:
			# message.tips(who, "只能在天问初试中使用")
			return
		if propsNo == self.getConfigInfo(2004):#随机去除一个错误答案
			dUseProps = who.week.fetch("FEProps", {})
			if taskObj.iExamNo in dUseProps:
				message.tips(who, "#C02{}#n每题只能使用一次".format(props.getPropsName(propsNo)))
				return

			if sum(who.propsCtn.getPropsAmountByNos(propsNo)) <= 0:
				return
			who.propsCtn.subPropsByNo(propsNo, 1, "周答题")

			dUseProps[taskObj.iExamNo] = 1
			who.week.set("FEProps", dUseProps)

			who.endPoint.rpcFirstExamRemoveOption()
			message.tips(who, "使用#C02{}#n成功，已随机去掉一个错误选项".format(props.getPropsName(propsNo)))

		elif propsNo == self.getConfigInfo(2003):#战斗
			if sum(who.propsCtn.getPropsAmountByNos(propsNo)) <= 0:
				return
			who.propsCtn.subPropsByNo(propsNo, 1, "周答题")
			message.tips(who, "使用#C02{}#n成功，战斗胜利将通过该题目".format(props.getPropsName(propsNo)))
			taskObj.customFight(who)

	def getValueByVarName(self, varName, who):
		if varName == "N":#连续答对的题数
			return who.week.fetch("firstExmaRightN", 0)
			# dFirstExamComTime = who.week.fetch("FEComTime", {})
			# dAnswerError = who.week.fetch("FEError", {})
			# iRightCnt = 0
			# iExamNo = max(dFirstExamComTime.keys())
			# for index in xrange(iExamNo, 0, -1):
			# 	if dAnswerError.get(index, 0):
			# 		break
			# 	iRightCnt+=1
			# return iRightCnt
		return customActivity.getValueByVarName(self, varName, who)

	#===========================
	#排行榜
	def resetRank(self):
		'''重置排行榜
		'''
		self.answerLog("firstExam", "firstExam resetRank")
		for _,rankObj in self.dFirstExamRank.iteritems():
			rankObj.clearRank()

	def getFinalRank(self):
		'''完成20道题目的排行榜
		'''
		iMaxAnswerCnt = self.maxAnswerCnt()
		rankObj = self.dFirstExamRank.get(iMaxAnswerCnt, None)
		if not rankObj:
			raise Exception,"找不到资格排行榜"
		return rankObj

	def updateRank(self, who, iExamNo):
		'''更新排行榜
		'''
		if not self.isInFirstExamTime():
			return
		rankObj = self.dFirstExamRank.get(iExamNo, None)
		if not rankObj:
			return

		#统计完成20道题目的人数
		self.week.add("completeAllCnt", 1)

		dFirstExamComTime = who.week.fetch("FEComTime", {})
		iStartTime = who.week.fetch("firstExamStart", 0)	#开始计时时间
		iCurrentTime = dFirstExamComTime.get(iExamNo, getSecond())#当前题目完成时间

		dAnswerError = who.week.fetch("FEError", {})#错误次数
		iErrorCnt = sum(dAnswerError.values())

		#使用时间
		useTime = iCurrentTime - iStartTime + iErrorCnt*self.errAddTime()
		rankObj.updateScore(who.id, who.name, useTime, who.level, who.school, gender=who.gender)
		#需要马上排序
		rankObj.timerUpdateRanking()

	def getFirstAnswerTime(self, who, iExamNo=20):
		'''完成N道题目时间
		'''
		dAnswerError = who.week.fetch("FEError", {})#错误次数
		iErrorCnt = 0
		for i,iCnt in dAnswerError.iteritems():
			if i > iExamNo:
				break
			iErrorCnt += iCnt

		dFirstExamComTime = who.week.fetch("FEComTime", {})
		iStartTime = who.week.fetch("firstExamStart", 0)#开始计时时间
		iEndTime = dFirstExamComTime.get(iExamNo, getSecond())#20题目完成时间
		return iEndTime - iStartTime + iErrorCnt * self.errAddTime()

	def timerHandFinalExam(self):
		'''20:00系统将对12:00至20:00中所有答完天问初试20道题的玩家答题总耗时进行排行，并选择其中耗时最短的3%玩家发放金章之试参与资格
		'''
		self.answerLog("firstExam", "timerHandFinalExam start")

		#若3%的玩家大于100人，则只选取前100名玩家参与金章之试；
		#若3%的玩家少于50人，则自动向后补充玩家直至有50名玩家参与金章之试；
		iCompleteCnt = self.week.fetch("completeAllCnt", 0)

		iQualifyNumber = int(iCompleteCnt * 0.03)
		if iQualifyNumber > 100:
			iQualifyNumber = 100
		elif iQualifyNumber < 50:
			iQualifyNumber = 50

		#回答完20题排行榜
		iMaxAnswerCnt = self.maxAnswerCnt()
		lastRankObj = self.dFirstExamRank.get(iMaxAnswerCnt, None)
		if not lastRankObj:
			raise Exception,"乡试-排行榜不存在"
		lFinalExamId = lastRankObj.lRanking[:iQualifyNumber]

		self.answerLog("firstExam", "timerHandFinalExam lastRankObj|{}|{}|{}".format(iCompleteCnt, iQualifyNumber, lFinalExamId))
		self.week.set("finalExamId", lFinalExamId)

		#保存金章之试名单
		finalExamObj = answer.getAnswerFinalExamObj()
		finalExamObj.setFinalExamRoleId(lFinalExamId)

		#名单出炉时，系统传闻+滚屏公告：金章之试名单已出炉，请火速前往邮箱查看金章之试名单邮件！
		content = self.getText(2350)#"金章之试名单已出炉，请火速前往邮箱查看金章之试名单邮件！"
		message.sysMessage(content)
		message.sysRoll(content)

		#名单出炉时，将发放一封邮件给所有获得了金章之试资格的玩家
		title = "金章之试资格发放"
		npcName = self.npcInfo.get(100021, {}).get("称谓", "")
		content = "恭喜你获得了本周金章之试的参与资格，请于今晚21:00至22:00在{}处进行金章之试答题。".format(npcName)
		for iRoleId in lFinalExamId:
			mail.sendSysMail(iRoleId, title, content)

	def onLogin(self, who, bRelogin):#override
		customActivity.onLogin(self, who, bRelogin)

		#删除过期的物品
		iNo1 = self.getConfigInfo(2003)
		iNo2 = self.getConfigInfo(2004)
		propsObjList = list(who.propsCtn.getPropsGroupByNo(iNo1, iNo2))
		for obj in propsObjList:
			if obj.isInvalid():
				who.propsCtn.removeItem(obj)


class NpcFirst(customNpc):
	'''周答题npc1
	'''
	
	# def __init__(self, gameObj):
	# 	npc.object.NpcBase.__init__(self)
	# 	self.game = weakref.proxy(gameObj)
	# 	self.iExamNo = 0

	# def remove(self):
	# 	sceneObj = scene.getScene(self.sceneId)
	# 	if sceneObj:
	# 		sceneObj.removeEntity(self)

	def checkCanExam(self, who):
		#除周六12:00-22:00以外的所有时间显示
		#周六21:00-22:00玩家当天未接取过“初试答题任务1”时显示
		if gbNotLimitTime:
			return ''
		if not self.game.isInAnswerTime() or (self.game.isInSeconExamTime() and not who.week.fetch("firstExamSelect", 0)):
			return '天问初试于 #C04每周六12点#n 开始，现在不是初试任务的领取时间'
		if who.level < 20:
			return '少侠等级太低，请升到#C04 20级#n后再来'
		return ''

	def doLook(self, who):
		reason = self.checkCanExam(who)
		if reason:
			self.say(who, reason)
			return

		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj and taskObj.iExamNo == self.iExamNo:
			if who.getTeamObj():
				message.tips(who, self.game.getText(2321, who.id))
				return
			#打开答题界面
			self.game.openFirstExamUI(who)
			return

		txtList= []
		selList = []
		##未接取过“初试答题任务1” 周六12:00-21:00期间
		if not who.week.fetch("firstExamSelect", 0) and self.game.isInGetTaskTime():
			if self.game.isInFirstExamTime():#周六12:00-20:00，玩家等级大于等于20级且当天未接取过“初试答题任务1”
				txtList.append('天问初试已开始，少侠是否开始答题？')
			else:							#周六20:00-21:00，玩家等级大于等于20级且当天未接取过“初试答题任务1”
				txtList.append('金章之试资格发放已结束，当前任可参与天问初试，少侠是否开始答题？')

			txtList.append('Q开始答题')
			selList.append(100)
		else:
			if self.iExamNo in who.week.fetch("FEComTime", {}):#已完成
				txtList.append('你已完成了此处的天问初试答题。')
			else:
				txtList.append('天问初试于 #C04每周六12点#n 开始，现在不是初试任务的领取时间')

		# 一直显示，点击弹出规则描述框
		txtList.append('Q初试规则')
		selList.append(101)

		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return

		reason = self.checkCanExam(who)
		if reason:
			return
		
		sel = selList[selectNo-1]
		if sel == 100:	#开始答题
			if who.getTeamObj():
				message.tips(who, self.game.getText(2321, who.id))
				return

			#弹出科目类型选择界面
			who.endPoint.rpcOpenSelectFirstExam()
			message.tips(who, "请选择你擅长的科目类别")
		elif sel == 101:#初试规则
			#弹出初试规则界面
			openUIPanel.openCommonTips(who, 3017)
			# who.endPoint.rpcOpenFirstExamRule()

	def canSelectFirstExam(self, who, iSelect):
		'''判断能不能选择科目类型
		'''
		reason = self.checkCanExam(who)
		if reason:
			message.tips(who, reason)
			return False
		if who.getTeamObj():
			message.tips(who, self.game.getText(2321))
			return False
		if who.week.fetch("firstExamSelect", 0):
			return False
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj:
			message.tips(who, "您已领取答题任务")
			return False
		#题目类型
		if iSelect not in self.game.questionTypeInfo:
			message.tips(who, "领取类型不存在")
			return False
		return True

	def selectFirstExam(self, who, iSelect):
		'''科目类型选择
		'''
		if not self.canSelectFirstExam(who, iSelect):
			return
		who.week.set("firstExamSelect", iSelect)
		who.week.set("firstExamStart", getSecond())	#开始计时时间
		message.tips(who, self.game.getText(2325, who.id))
		if task.weekAnswer.giveWeekAnswerTask(who):
			#给道具
			launch.launchBySpecify(who, self.game.getConfigInfo(2003), 3, False, "领取周答题")
			launch.launchBySpecify(who, self.game.getConfigInfo(2004), 3, False, "领取周答题")
		self.game.openFirstExamUI(who)



class NpcOther(customNpc):
	'''周答题npc2-20
	'''
	# def __init__(self, gameObj):
	# 	npc.object.NpcBase.__init__(self)
	# 	self.game = weakref.proxy(gameObj)
	# 	self.iExamNo = 0

	# def remove(self):
	# 	sceneObj = scene.getScene(self.sceneId)
	# 	if sceneObj:
	# 		sceneObj.removeEntity(self)

	def getExamChat(self, who):
		firstExamSelect = who.week.fetch("firstExamSelect", 0)
		#除周六12:00-22:00以外的所有时间显示
		#周六21:00-22:00玩家当天未接取过“初试答题任务1”时显示
		if not self.game.isInAnswerTime() or (self.game.isInSeconExamTime() and not firstExamSelect):
			return '天问初试于 #C04每周六12点#n 开始，现在不是初试任务的领取时间'
		
		#周六12:00-21:00，玩家当天未接取过“初试答题任务1”时显示
		if not firstExamSelect and self.game.isInGetTaskTime():
			info = self.game.getNpcInfo(1001)
			return '你还未领取天问初试任务，请前往 #C04{}#n 处领取。'.format(info.get("名称", ""))

		dComExamNo = who.week.fetch("FEComTime", {})
		#周六12:00-22:00，玩家完成了对应NPC的“初试答题任务”
		if self.iExamNo in dComExamNo:
			return '你已完成了此处的天问初试答题。'

		#玩家身上接有非当前NPC对应的“初试答题任务”，且当天未完成过当前“天问初试NPC”对应的任务
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj and taskObj.iExamNo != self.iExamNo and self.iExamNo not in dComExamNo:
			# npcObj = self.game.getNpcObjByExamNo(taskObj.iExamNo)
			# name = npcObj.name if npcObj else ""
			info = self.game.getNpcInfo(1000+taskObj.iExamNo)
			return '我不是这道题的考官，请少侠前往 #C04{}#n 处进行答题。'.format(info.get("名称", ""))

		return '天问初试于 #C04每周六12点#n 开始，现在不是初试任务的领取时间'

	def doLook(self, who):
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj and taskObj.iExamNo == self.iExamNo:
			if who.getTeamObj():
				message.tips(who, self.game.getText(2321, who.id))
				return
			#todo 打开答题界面
			self.game.openFirstExamUI(who)
			return

		txtList= []
		selList = []
		txtList.append(self.getExamChat(who))

		firstExamSelect = who.week.fetch("firstExamSelect", 0)
		#周六12:00-21:00，玩家当天未接取过“初试答题任务1”时显示，点击自动引路至“天问初试NPC1”
		#周六12:00-22:00，玩家身上接有非当前NPC对应的“初试答题任务”，且当天未完成过当前“天问初试NPC”对应的任务，点击自动引路至身上”初试答题任务“对应的”天问初试NPC“
		if (not firstExamSelect and self.game.isInGetTaskTime()) or \
			(taskObj and self.game.isInAnswerTime() and self.iExamNo not in who.week.fetch("FEComTime", {})):
			txtList.append('Q前往')
			selList.append(100)
		
		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return

		sel = selList[selectNo-1]
		if sel == 100:	#开始答题
			self.goToOtherNpc(who)

	def goToOtherNpc(self, who):
		'''前往其它NPC
		'''
		taskObj = task.weekAnswer.hasWeekAnswerTask(who)
		if taskObj:
			taskObj.goAhead(who)
		else:
			firstExamSelect = who.week.fetch("firstExamSelect", 0)
			#还没接到任务到NPC1片
			if not firstExamSelect and self.game.isInGetTaskTime():
				npcObj = self.game.getNpcObjByExamNo(1)
				if npcObj:
					scene.walkToEtt(who,npcObj)

#============================================
#选择题目类型
def rpcSelectFirstExam(who, reqMsg):
	firstExamObj = answer.getAnswerFirstExamObj()
	npcObj = firstExamObj.getNpcObjByExamNo(1)
	if not npcObj:
		return
	iSelect = reqMsg.iSelect
	npcObj.selectFirstExam(who, iSelect)


def rpcAnswerFirstExam(who, reqMsg):
	firstExamObj = answer.getAnswerFirstExamObj()
	sValue = reqMsg.sValue
	firstExamObj.answerFirstExam(who, sValue)


def rpcFirstExamClose(who, reqMsg):
	firstExamObj = answer.getAnswerFirstExamObj()
	firstExamObj.setEndAnswer(who)


from common import *
from answer.defines import *
import time
import answer
import answer.service
import log
import message
import QuestionData
import openUIPanel
import activity.center
import scene
import weakref
import task.weekAnswer
import cycleData
import props
import launch
import mail
import npc
import team.platform
import config
import rank