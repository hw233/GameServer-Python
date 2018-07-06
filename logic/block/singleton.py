#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst
import block

#单件对象,存储在singleton表
class cSingleton(block.cBlock,pst.cEasyPersist):
	def __init__(self,sChineseName,sName):#override
		glSingleton.append(self)
		self.sName=sName
		block.cBlock.__init__(self,sChineseName,sName)
		pst.cEasyPersist.__init__(self)
		self.setIsStm(sql.SINGLETON_INSERT)
		self.setDlStm(sql.SINGLETON_DELETE)
		self.setUdStm(sql.SINGLETON_UPDATE)
		self.setSlStm(sql.SINGLETON_SELECT)
		self.eDirtyEvent+=self._dirtyEventHandler

		# self.hour=cycleData.cCycHour(2,self._dirtyEventHandler)#小时变量
		# self.day=cycleData.cCycDay(2,self._dirtyEventHandler)#天变量
		# self.week=cycleData.cCycWeek(2,self._dirtyEventHandler)#周变量
		# self.month=cycleData.cCycMonth(2,self._dirtyEventHandler)#月变量

	def _dirtyEventHandler(self):#数据发生变化,加入到存盘调度队列
		factory.storageScheduler.appendCallLater(self._saveToDB,'singleton',self.sName)#u.cFunctor(,False)

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		# self.hour.load(dData.pop('h',{}))
		# self.day.load(dData.pop('d',{}))
		# self.week.load(dData.pop('w',{}))
		# self.month.load(dData.pop('m',{}))

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		
		# dHour=self.hour.save()
		# if dHour:
		# 	dData['h']=dHour
		# dDay=self.day.save()
		# if dDay:
		# 	dData['d']=dDay
		# dWeek=self.week.save()
		# if dWeek:
		# 	dData['w']=dWeek
		# dMonth=self.month.save()
		# if dMonth:
		# 	dData['m']=dMonth

		return dData

if 'glSingleton' not in globals():#系统中全部的singleton实例
	glSingleton=[]

import u
import c
import misc
import log
import sql
import cycleData
import factory