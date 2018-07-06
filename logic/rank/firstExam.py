# -*- coding: utf-8 -*-
import rank.object

class cRanking(rank.object.cRanking):
	'''周答题-初试排行榜
	'''
	#override
	def _valueComparer(self, iUid1, iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return -1
		elif iValue1>iValue2:
			return 1
		return 0

	def startTimer(self):#启动定时器,用于定时刷新排行榜
		'''不用自动排行
		'''
		pass

	def getRoleGender(self, iUid):
		return self.getRoleArgs(iUid).get("gender", 0)

	def title4(self, iUid):
		iValue = self.getValue(iUid)
		return formatTime(iValue)

	def getAnswerUseTime(self, who):
		iValue = self.getValue(who.id)
		if iValue:
			return formatTime(iValue)
		firstExamObj = answer.getAnswerFirstExamObj()
		iStartTime = who.week.fetch("firstExamStart", 0)	#开始计时时间
		if not iStartTime:
			return '—'
		dFirstExamComTime = who.week.fetch("FEComTime", {})	#结束时间
		iEndTime = dFirstExamComTime.get(firstExamObj.maxAnswerCnt(), 0)#当前题目完成时间
		if not iEndTime:
			return '—'
		dAnswerError = who.week.fetch("FEError", {})#错误次数
		iErrorCnt = sum(dAnswerError.values())
		#使用时间
		useTime = iEndTime - iStartTime + iErrorCnt*firstExamObj.errAddTime()
		return formatTime(useTime)

	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(self.getAnswerUseTime(who))
		return tMyInfo

from common import *
import role.defines
import answer
