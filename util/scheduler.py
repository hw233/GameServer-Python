#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#调度器
#精度很差的,用于定时存盘,对象清出内存等对时间精度要求很低的工作

CYCLE_TIME=5*60.0 #全部执行一遍所需时间(秒),以此计算出平均每一个执行间隔
#真正的执行间隔受以下两个数修正
MIN_INTERVAL,MAX_INTERVAL=0.1,5 #最小间隔(秒),最大间隔(秒)

class cScheduler(object):
	def __init__(self,icycleTime=CYCLE_TIME,iMinInterval=MIN_INTERVAL,iMaxInterval=MAX_INTERVAL):#iMinInterval,iMaxInterval
		self.icycleTime=icycleTime
		self.iMinInterval,self.iMaxInterval=iMinInterval,iMaxInterval		

		self.timerMng=timer.cTimerMng()#用于
		self.deqItems=collections.deque()#双端队列
		self.dKeyMapFunc={}#主键映射函数
		self.uTimerId=0
		self.fNext=self.iMaxInterval #下一次呼叫的间隔

	def callBackAmount(self):#总共还有多少个callback有待调用
		return len(self.dKeyMapFunc)

	def prependCallLater(self,func,*tPriKey):
		self.__addCallLater(False,func,*tPriKey)

	def appendCallLater(self,func,*tPriKey):
		self.__addCallLater(True,func,*tPriKey)

	def __addCallLater(self,bAppend,func,*tPriKey):
		if not tPriKey:
			raise Exception,'必须提供主键.'
		if bAppend:
			#append到尾上就没有必要重复添加,插入到头上就允许重复
			#if tPriKey in self.deqItems:#这个可能是遍历,性能稍差
			#	return
			if tPriKey in self.dKeyMapFunc:#hash性能稳定一点
				return
			self.deqItems.append(tPriKey)
		else:#append到前面的插队动作,不检查是否已经在队里,会造成同1个key多次存在队列里
			self.deqItems.appendleft(tPriKey)			
		self.dKeyMapFunc[tPriKey],=u.makeWeakFunc(func) #存储弱引用
		#print 'scheduler .. __addCallLater..',tPriKey
		#import traceback
		#traceback.print_stack()
		if self.uTimerId==0:#定时器尚未起动
			fDelay=self.__next()
			self.uTimerId=self.timerMng.run(self.__helperFunc,fDelay,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)

	def hasCallLater(self,*tPriKey):#是否存在某个回调
		if not tPriKey:
			raise Exception,'必须提供主键.'
		return tPriKey in self.dKeyMapFunc

	def removeCallLater(self,*tPriKey):
		if not tPriKey:
			raise Exception,'必须提供主键.'
		#if tPriKey in self.deqItems:#从双端队列的中间remove元素,性能不知道如何,干脆就不做了
		#	self.deqItems.remove(tPriKey)#时间到了再找一个有效的函数,跳过无效的函数即可
		self.dKeyMapFunc.pop(tPriKey,None)

	def __helperFunc(self):
		while self.deqItems:
			tPriKey=self.deqItems.popleft()#前面弹出来
			func=self.dKeyMapFunc.pop(tPriKey,None)
			if func!=None:#有可能会None,因为会发生多个key存在deqItems里的情况,但dKeyMapFunc只能存一个相同的key
				break
		else:
			self.uTimerId=0 #标识定时器未起动
			return
		try:#确保不会因为一个调用发生异常,导致执行链中断
			func()
		except Exception:
			u.logException()
			self.deqItems.append(tPriKey)#出异常了,放回队列尾去,一会再重试
			self.dKeyMapFunc[tPriKey]=func #函数也要挂回去
		
		# else:#不要这段代码了,无法正确地检查,因为存盘过程访问了sql,有IO操作,是异步的
		# 	try:
		# 		if self.dKeyMapFunc.pop(tPriKey,None):
		# 			raise Exception,'在存档过程中又打了脏标志,这是不合理的.key为{}'.format(tPriKey)
		# 	except Exception:
		# 		u.logException()

		fDelay=self.__next()
		if fDelay!=-1:#还有元素,继续为下一次执行准备
			if fDelay<self.fNext:#越走越快
				self.fNext=fDelay
			self.uTimerId=self.timerMng.run(self.__helperFunc,self.fNext,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)
		else:
			self.uTimerId=0 #标识定时器未起动
			self.fNext=self.iMaxInterval #全部执行完了,恢复初始速度
		
	def __next(self):
		#iLen=len(self.deqItems)#这个不准确的,以self.dKeyMapFunc为准
		iLen=len(self.dKeyMapFunc)
		if iLen==0:
			return -1 #表示没有元素,不需要定时器了
		fDelay=self.icycleTime/iLen #平均间隔		
		if fDelay<self.iMinInterval: #不能太密,影响性能
			fDelay=self.iMinInterval 
		elif fDelay>self.iMaxInterval: #不能太疏,不影响性能的情况下要保证精度
			fDelay=self.iMaxInterval
		return fDelay

import collections
import timer
import timeU
import log
import u
import c
