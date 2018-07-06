# -*- coding: utf-8 -*-
import pst
from common import getSecond

#只维持n个周期后就会自动清理的数据
class cCycleData(pst.cPersist):
	#iKeepCyc	数据保留的时间周期
	#cDirtyHandler	数据变化事件响应函数.
	def __init__(self,iKeepCyc,cDirtyHandler=None):
		pst.cPersist.__init__(self,cDirtyHandler)
		if iKeepCyc<1:
			iKeepCyc=1
		self.iKeepCyc=iKeepCyc
		self.dData={}

	def save(self):#override
		return self.dData

	def load(self,dData):#override
		iCurCycNo=self.getCycleNo()
		lCycNo=dData.keys()
		lCycNo.sort()#从最早的开始检查,可以尽快地退出循环
		bIsDirty=False
		for iCycNo in lCycNo:
			if iCurCycNo>=int(iCycNo)+self.iKeepCyc:
				del dData[iCycNo]
				bIsDirty=True
			else:
				break
		if bIsDirty:
			self.markDirty()
		self.dData=dData

	def set(self,key,value):#override
		iCycNo=self.getCycleNo()
		if iCycNo not in self.dData:
			self.dData[iCycNo]={}
		self.dData[iCycNo][key]=value
		self.markDirty()

	def delete(self,key):
		iCycNo=self.getCycleNo()
		if iCycNo not in self.dData or key not in self.dData[iCycNo]:
			return
		del self.dData[iCycNo][key]
		self.markDirty()

	def add(self,key,uValue,uDefault=0):#override	#返回成功后的结果值
		iCycNo=self.getCycleNo()		
		dCurCyc=self.dData.setdefault(iCycNo,{})
		dCurCyc[key]=dCurCyc.get(key,uDefault)+int(uValue)
		self.markDirty()
		return dCurCyc[key]

	#override
	#iWhichCyc的值范围 0:当前周期,-1:上一个周期,-2:上二个周期,-3:上三个周期,以此类推
	#如果是天记录,则相应是 0:今天,-1:昨天,-2:前天,-3:大前天,以此类推
	def fetch(self,key,uDefault=0,iWhichCyc=0):
		if iWhichCyc>0:
			raise Exception,'iWhichCyc值为{},大于0是没有意义的'.format(iWhichCyc)
		iCycNo=self.getCycleNo()+iWhichCyc
		return self.dData.get(iCycNo,{}).get(key,uDefault)

	def clear(self,iWhichCyc=0)	:#清除某个周期的数据,这个很危险,基本上只是方便QC在内服做测试用的
		if iWhichCyc>0:
			raise Exception,'iWhichCyc值为{},大于0是没有意义的'.format(iWhichCyc)
		iCycNo=self.getCycleNo()+iWhichCyc
		if self.dData.pop(iCycNo,None):
			self.markDirty()

	def getCycleNo(self):
		raise NotImplementedError,'请在子类override'

#小时变量
class cCycHour(cCycleData):
	def getCycleNo(self):#override
		return common.getHourNo()

#天变量
class cCycDay(cCycleData):
	def getCycleNo(self):#override
		return common.getDayNo()

#周变量
class cCycWeek(cCycleData):
	def getCycleNo(self):#override
		return common.getWeekNo()

#月变量
class cCycMonth(cCycleData):
	def getCycleNo(self):#override
		return common.getMonthNo()
	


class ThisTemp(pst.cPersist):
	'''临时变量
	'''

	def __init__(self, cDirtyHandler=None):
		pst.cPersist.__init__(self, cDirtyHandler)
		self.dataList = {}
		self.timeList = {}
		
	def save(self):
		data = {}
		data["dataList"] = self.dataList
		data["timeList"] = self.timeList
		
	def load(self, data):
		self.dataList = data["dataList"]
		self.timeList = data["timeList"]
		self.checkTimeout()
		
	def checkTimeout(self):
		now = getSecond()
		keyList = self.dataList.keys()
		updated = False
		for key in keyList:
			if self.timeList[key] <= now:
				del self.dataList[key]
				del self.timeList[key]
				updated = True
		
		if updated:
			self.markDirty()
		
	def set(self, key, val, ti):
		self.checkTimeout()
		self.markDirty()
		self.dataList[key] = val
		self.timeList[key] = getSecond() + ti
		
	def add(self, key, val, ti):
		self.checkTimeout()
		self.markDirty()
		self.dataList[key] = self.dataList.get(key, 0) + val
		if key not in self.timeList:
			self.timeList[key] = getSecond() + ti
		return self.dataList[key]
			
	def delete(self, key, default=0):
		if key in self.dataList:
			self.markDirty()
			self.timeList.pop(key, 0)
			return self.dataList.pop(key)
		return default
	
	def fetch(self, key, default=0):
		self.checkTimeout()
		return self.dataList.get(key, default)
	
	def fetchTime(self, key, default=0):
		self.checkTimeout()
		return self.timeList.get(key, default)
	

import weakref
# import timeU
import u
import common