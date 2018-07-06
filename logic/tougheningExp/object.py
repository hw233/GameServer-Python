# -*- coding: utf-8 -*-
'''历练经验
'''

class TougheningExp(object):
	'''历练经验数据对象
	'''

	def __init__(self, iNo):
		self.iNo = iNo

	@property
	def id(self):
		return self.iNo

	def getConfig(self, key, default=0):
		return tougheningExpData.gdData.get(self.iNo, {}).get(key, default)

	@property
	def name(self):
		return self.getConfig("活动名称", "")

	def ring(self):
		return self.getConfig("轮数")

	def ringCnt(self):
		return self.getConfig("每轮次数")

	def cntMax(self):
		return self.getConfig("次数")

	def rate(self):
		return self.getConfig("转化率")

	def calculateExp(self, who, iDayNo, comCnt):
		'''计算历练经验,comCnt:已完成次数
		'''
		if not self.checkMiss(who, iDayNo):
			#当天不开放
			return 0
		func = self.getConfig("经验公式", None)
		if not func:
			return 0

		rate = self.rate()
		iMaxCnt = self.cntMax()
		if iMaxCnt:	#每次的历练经验相同
			if comCnt >= iMaxCnt:
				return 0
			params=[]
			for varName in func.func_code.co_varnames:
				varVal = self.getValueByVarName(varName, who)
				params.append(varVal)
			iExp = func(*params)
			#每次经验*剩余*转化率
			return int(iExp*(iMaxCnt-comCnt)*rate)

		else:	#每轮的经验不一样
			iRingCnt = self.ringCnt()
			iRing = self.ring()
			iMaxCnt = iRing*iRingCnt
			if comCnt >= iMaxCnt:
				return 0
			iTotalExp = 0

			for ring in xrange(comCnt+1, iMaxCnt+1):
				params=[]
				for varName in func.func_code.co_varnames:
					_ring = ring%iRingCnt if 0 != ring%iRingCnt else iRingCnt
					varVal = self.getValueByVarName(varName, who, _ring)
					params.append(varVal)
				iExp = func(*params)
				iTotalExp += iExp
			return int(iTotalExp*rate)

	def getValueByVarName(self, varName, who, ring=0):
		if varName == "LV":
			return who.level
		elif varName == "R":
			return ring
		elif varName == "N":
			if self.name == '天问初试':
				dActProgress = who.fetch("actProgress", {})
				return dActProgress.get("firstExmaRightN", 0)
			return 0
			
		raise Exception,'历练经验策划填的变量{}无法解析.'.format(varName)

	def checkMiss(self, who, iDayNo):
		'''检查当天有没开放、等级
		'''
		centerObj = activity.center.getActivityCenter()
		info = centerObj.activityData.get(self.id, {})
		if not info:
			return False
		if who.level < info.get("活动等级", 0):
			return False

		timetype = info.get("活动日期类型", 0)
		actDateList = info.get("活动日期")

		datePart,weekNo = dayNoToDatePart(iDayNo)
		
		year = datePart["year"]  # 年
		month = datePart["month"]  # 月
		day = datePart["day"]  # 日
		wday = datePart["wday"]  # 星期几
		curTime = (year, month, day)  # 年,月,日
		
		if timetype == 1:  # 每天活动
			pass
		elif timetype == 2:  # 每周活动
			if isinstance(actDateList, int):
				if wday != actDateList:
					return False
			elif wday not in actDateList:
				return False
		elif timetype == 3:  # 具体日子
			if len(actDateList) == 4:
				startTime = [year] + list(actDateList[:2])
				endTime = [year] + list(actDateList[2:])
			else:
				startTime = actDateList[:3]
				endTime = actDateList[3:]
			if curTime < startTime:
				return False
			if curTime > endTime:
				return False
		elif timetype == 4:  # 单周活动
			if weekNo % 2 == 0:
				return False
			if wday not in actDateList:
				return False
		elif timetype == 5:  # 双周活动 
			if weekNo % 2 == 1:
				return False
			if wday not in actDateList:
				return False
		elif timetype == 6:  # 每月活动
			if month not in actDateList:
				return False
		else:
			return False
		return True

def dayNoToDatePart(iDayNo):
	'''根据天编号计算出日期
	'''
	lTime = list(timeU.gtStandardTime)
	lTime[2] += (iDayNo-1)
	ti = getSecond(*lTime)
	weekNo = getWeekNo(ti)
	return getDatePart(ti),weekNo

from common import *
import tougheningExpData
import types
import activity.center
import timeU
