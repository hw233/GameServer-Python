#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#产品,抽象类
class cProduct(object):
	def __init__(self,sChineseName,*tPriKey):
		self.oFactory=None
		self.sChineseName=sChineseName #有个中文名,方便调试查找错误
		self.tPriKey=tPriKey
		self.iBirthStamp=0 #从数据库中加载回来的时间戳
		self.lKeepers=[] #本来用set的,但是set不能存proxy.(TypeError: unhashable type: 'weakproxy')

	def addKeeper(self,oKeeper):
		oPrx=weakref.proxy(oKeeper) #避免keeper与product互相循环引用
		self.lKeepers.append(oPrx)

	def removeKeeper(self,oKeeper):
		oPrx=weakref.proxy(oKeeper) #避免keeper与product互相循环引用
		if oPrx in self.lKeepers:
			self.lKeepers.remove(oPrx)

	def keeperAmount(self):
		return len(self.lKeepers)

	def this(self):
		return self

	def getPriKey(self):#返回主键,类型是tuple
		return self.tPriKey

	def chineseName(self):
		return self.sChineseName

	def setFactory(self,oFactory):
		self.oFactory=weakref.proxy(oFactory)
		return self #可以链式调用

	def getFactory(self):
		return self.oFactory

	@property
	def factoryObj(self):
	    return self.oFactory	

	def birthStamp(self):
		return self.iBirthStamp

	def setBirthStamp(self,iBirthStamp):
		self.iBirthStamp=iBirthStamp

	def liveTime(self):#至今存活时间(进入内存总共多长时间),返回如 94天21时56分5秒 字符串
		return timeU.getTimeStr(timeU.getStamp()-self.iBirthStamp)

	def _insertToDB(self,*itNoRowInsertValues,**dData):
		raise NotImplementedError,'请在子类实现'

	def _deleteFromDB(self):
		raise NotImplementedError,'请在子类实现'

	def _saveToDB(self):#执行update语句,bForce为真时不管内存数据有没有发生变化都强行存盘,bForce=False
		raise NotImplementedError,'请在子类实现'

	def _loadFromDB(self):#执行select语句,bNotExistInsert表示数据库中查不到时是否当场insert
		raise NotImplementedError,'请在子类实现'

	def checkMarkDirty(self):
		pass
import weakref
import copy
import sys
import ujson
import gevent.event
import mysqlCnt
import timer
import c
import u
import primitive
import timeU