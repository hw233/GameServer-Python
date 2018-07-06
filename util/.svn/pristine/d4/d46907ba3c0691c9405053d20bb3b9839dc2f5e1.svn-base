#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

#时间轮盘
#每n分钟给角色回复一定体力
#角色断线n分钟后踢出内存
#对时间要求不是非常精准的

class cTimingWheel(object):
	def __init__(self,iScaleAmount=8,iInterval=3):
		if iScaleAmount<=0:
			raise Exception,'iScaleAmount至少是1.'
		self.iScaleAmount=iScaleAmount #刻度数量(bucket数量,桶数量)
		self.iInterval=iInterval #每刻度停留秒数(可以理解成是定时器的误差值.)
		self.dBucket={}
		self.iScale=0
		
		self.timerMng=timer.cTimerMng()#
		self.uTimerId=0
		self.dKeyMapScale={}

		self.oLock=gevent.lock.RLock()

	def callbackAmount(self):
		return len(self.dKeyMapScale)

	def addCallback(self,cCallback,*tPriKey):#增加一个回调函数(重复添加会覆盖)
		if self.uTimerId==0:#尚未启动定时器
			self.uTimerId=self.timerMng.run(self._helperFunc,self.iInterval,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)

		self.removeCallback(*tPriKey)
		cCallback,=u.makeWeakFunc(cCallback)#建立弱引用
		self.dKeyMapScale[tPriKey]=self.iScale
		self.dBucket.setdefault(self.iScale,{})[tPriKey]=cCallback	
		
	def hasCallback(self,*tPriKey):#是否有一个回调函数	
		return tPriKey in self.dKeyMapScale

	def removeCallback(self,*tPriKey):#移除一个回调函数		
		iScale=self.dKeyMapScale.pop(tPriKey,None)
		if iScale in self.dBucket:
			self.dBucket[iScale].pop(tPriKey,None)

	def _helperFunc(self):
		with self.oLock:
			self.uTimerId=0 #标志尚未启动定时器
			#print 'timingWheel.__helperFunc..',timeU.stamp2str()
			self.iScale+=1
			if self.iScale>=self.iScaleAmount:
				self.iScale=0

			dFuncs=self.dBucket.get(self.iScale, {})
			if dFuncs:
				for tPriKey,func in dFuncs.items(): #iter RuntimeError: dictionary changed size during iteration
					try:
						if func():#踢
							self.dKeyMapScale.pop(tPriKey,None)
							dFuncs.pop(tPriKey,None)
						
					except Exception:
						u.logException()

			if len(self.dBucket) and self.uTimerId==0:#启动下一次定时器
				self.uTimerId=self.timerMng.run(self._helperFunc,self.iInterval,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)

import weakref
import gevent.event
import gevent.lock
import u
import log
import timer
import timeU