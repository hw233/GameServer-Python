#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#
import timer
#外部不断地往轮盘里加obj,内部定时器不断地踢obj
#目的是利用obj对象的析构做一些事
class cTimingWheel(object):
	def makeWrObj(self,deleter):
		obj=cBar()
		self.addObj(obj)
		func,=u.makeWeakFunc(deleter)#防止循环引用
		return weakref.ref(obj,func)

	def __init__(self,iScaleAmount=8,iDelay=3):
		if iScaleAmount<=0:
			raise Exception,'iScaleAmount至少是1.'
		self.iScaleAmount=iScaleAmount #刻度数量(bucket数量,桶数量)
		self.iDelay=iDelay #每刻度停留秒数(可以理解成是定时器的误差值.)
		self.dBucket={}
		self.iIndex=0

		self.timerMng=timer.cTimerMng()#		
		self.uTimerId=0

	def addObj(self,obj):#增加一个
		if self.uTimerId==0:#尚未启动定时器
			self.uTimerId=self.timerMng.run(self.__helperFunc,self.iDelay,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)
	
		sScale=self.dBucket.setdefault(self.iIndex,set())
		sScale.add(obj)

	def __helperFunc(self):
		self.uTimerId=0 #标志尚未启动定时器
		self.iIndex+=1
		if self.iIndex>=self.iScaleAmount:
			self.iIndex=0

		#要保证"self.uTimerId置0" 和 "再启一个定时器"是一个原子操作.
		#dBucket.pop行为会导致ep的shutdown,进而引起协程切换.
		
		#timerid在上面已经置0了,pop引起协程切换,执行addObj,发现uTimerId是0,产生一个新的定时器,pop结束往下执行,又产生了一个定时器
		#结果就有2个定时器存在,要保证任何时候定时器,不能超过1个,可以0个


		#解决这个问题,1.对整一个函数加锁 2.spawn一个协程来pop,3.用临时变量延迟对象的析构到函数结束
		#这里用临时变量把对象析构延迟到函数结尾

		sTemp=self.dBucket.pop(self.iIndex,None)#sTemp变量不能删

		if len(self.dBucket)>0:#还有刻度槽,启动下一次定时器
			self.uTimerId=self.timerMng.run(self.__helperFunc,self.iDelay,timer.NOT_REPEAT,timer.NO_NAME,None,timer.LOWEST)
		

class cBar(object):#无法创建object对象的弱引用,就随便弄了一个类.
	pass
	
import weakref
import u
import c
import misc
import log