#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import productKeeper

#jit是 just in time的意思,需要时从临时数据库加载回来,用完差不多就踢回数据库
#N秒后自动从内存中移除对象
#用于玩家邮箱,玩家的宠物店,物品店,玩家的房子.玩家的仓库,等等不需要常驻内存的

class cJITproductKeeper(productKeeper.cProductkeeper):
	def __init__(self,oFactory,iKeepCycle=30,iSecondPerCycle=10):#1  5
		productKeeper.cProductkeeper.__init__(self,oFactory)
		if iKeepCycle<=0:
			raise Exception,'维持周期数必须大于0,不能是{}'.format(iKeepCycle)
		self.oFactory=oFactory
		self.iKeepCycle=iKeepCycle #持有对象周期数
		self.iSecondPerCycle=iSecondPerCycle #每周期秒数

		self.dLink={} #用来实现链表
		self.tFirstKey,self.tLastKey=None,None
		
		self.dAddSeq={} #各对象加载进来的时间戳
		self.oTimerMng=timer.cTimerMng()#定时器
		self.uTimerId=0
		glJitKeeper.append(self)

	def getCycleSequene(self):#取得当前周期序号
		return int(gevent.core.time())/self.iSecondPerCycle

	def getObjFromDB(self,itNoRowInsertValues,*tPriKey,**dData):#override
		self.__check()
		obj=productKeeper.cProductkeeper.getObjFromDB(self,itNoRowInsertValues,*tPriKey,**dData)
		if obj:
			self.__adjust(tPriKey)			
		return obj

	def __updateTimer(self):#更新定时器
		self.__check()
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.dLink:#没有对象了,不需要定时器来踢对象
			return
		iNowSeq=self.getCycleSequene()
		iAddSeq=self.dAddSeq[self.tFirstKey]#最早应该踢除对象的key
		if iNowSeq-iAddSeq>self.iKeepCycle:#已经超时,立马kick
			self.__kickObj()
		else:
			fDelay=(iAddSeq+self.iKeepCycle)*self.iSecondPerCycle-int(gevent.core.time())#转为秒	
			self.uTimerId=self.oTimerMng.run(self.__kickObj,fDelay)#起一个更早的定时器

	def __kickObj(self):#时间到,定时器触发
		self.__check()
		self.uTimerId=0 #标志没有定时器了
		if self.tFirstKey is None:
			return		
		iCurCycSeq=self.getCycleSequene()
		tTempKey=self.tFirstKey
		while tTempKey:
			if iCurCycSeq-self.dAddSeq[tTempKey]<self.iKeepCycle:#没有超时,不用踢
				break 
			#print 'tTempKey===',tTempKey
			productKeeper.cProductkeeper.removeObj(self,*tTempKey)#踢,里面存盘可能会抛异常(刻意调用父类的方法来踢)
			self.dAddSeq.pop(tTempKey)
			tTempKey=self.dLink.pop(tTempKey)[1]
		else:#全部对象踢完了
			self.tFirstKey,self.tLastKey=None,None
			self.__check()
			return
		self.tFirstKey=tTempKey
		if tTempKey:#还有元素
			self.dLink[tTempKey][0]=None #首元素的前趋节点改为None		
		if self.dLink:
			self.__updateTimer()#启动下一次定时器
		self.__check()

	def addObj(self,obj,*tPriKey):#override
		self.__check()
		productKeeper.cProductkeeper.addObj(self,obj,*tPriKey)
		self._addLinkInfo(tPriKey)
		self.__check()

	def _addLinkInfo(self,tPriKey):
		if tPriKey in self.dAddSeq:
			raise Exception,'{}已在管理器中'.format(tPriKey)
		if tPriKey in self.dLink:
			raise Exception,'{}已在管理器中'.format(tPriKey)

		self.dAddSeq[tPriKey]=self.getCycleSequene()

		if self.tLastKey is not None:#不是第1个obj
			self.dLink[self.tLastKey][1]=tPriKey
			self.dLink[tPriKey]=[self.tLastKey,None]
			self.tLastKey=tPriKey
		else:#是第1个obj
			self.tLastKey=self.tFirstKey=tPriKey
			self.dLink[tPriKey]=[None,None]
			self.__updateTimer()#是第1个元素,要启动定时器
		
	def removeObj(self,*tPriKey):#override
		self.__check()
		self._removeLinkInfo(tPriKey)#这句特意放在前面的,怕下面会引起add操作
		self.__check()
		productKeeper.cProductkeeper.removeObj(self,*tPriKey)#里面存盘可能会抛异常
		
		self.__check()

	def _removeLinkInfo(self,tPriKey):
		self.dAddSeq.pop(tPriKey,None)
		tPrevKey,tNextKey=self.dLink.pop(tPriKey,(None,None))
		if tPrevKey is not None:#被remove的不是首元素,需要修改前趋元素的next指针
			self.dLink[tPrevKey][1]=tNextKey
		
		if tNextKey is not None:#被remove的不是尾元素,需要修改后继元素的prev指针
			self.dLink[tNextKey][0]=tPrevKey

		if tPriKey==self.tLastKey:
			self.tLastKey=tPrevKey

		if tPriKey==self.tFirstKey:
			self.tFirstKey=tNextKey
			self.__updateTimer()#如果没有元素了就是取消定时器,还有元素就是更新定时器

	def __check(self):#临时性的代码,上线前删掉相应代码
		if not config.IS_INNER_SERVER:
			return
		if self.tLastKey is not None:#管理器中有元素
			tPrevKey,tNextKey=self.dLink[self.tLastKey]
			if tNextKey is not None:
				raise Exception,'最后节点的后继竟然不是None'
		else:
			if len(self.dLink):
				raise Exception,'数据不一致,self.dLink竟然还有数据'
			if len(self.dAddSeq):
				raise Exception,'数据不一致,self.dAddSeq竟然还有数据'

		if self.tFirstKey is not None:#管理器中有元素
			tPrevKey,tNextKey=self.dLink[self.tFirstKey]
			if tPrevKey is not None:
				raise Exception,'首节点的前驱竟然不是None'
		else:
			if len(self.dLink):
				raise Exception,'数据不一致,self.dLink竟然还有数据'
			if len(self.dAddSeq):
				raise Exception,'数据不一致,self.dAddSeq竟然还有数据'

		if [self.tFirstKey,self.tLastKey].count(None) not in (0,2):
			raise Exception,'self.tFirstKey,self.tLastKey中为None的个数要么是0个,要么是2个,不能其1个是None'

		if len(self.dLink)!=len(self.dAddSeq):
			raise Exception,'self.dLink与self.dAddSeq的长度不一致'

		iNextCnt,iPreCnt=0,0
		for iPre,iNext in self.dLink.values():
			if iNext is None:
				iNextCnt+=1
				if iNextCnt>=2:
					raise Exception,'wth,有2个后继节点为None'
			if iPre is None:
				iPreCnt+=1
				if iPreCnt>=2:
					raise Exception,'wth,有2个前趋节点为None'

	def __adjust(self,tPriKey):#调整链表
		self.__check()
		if self.tLastKey is None:
			raise Exception,'self.tLastKey不能是None'

		if tPriKey!=self.tLastKey:#当前不是最后一个元素,要调整双向链表(只有一个元素时,肯定是最后一个)
			tPrevKey,tNextKey=self.dLink[tPriKey]

			if tNextKey is None:#不是最后一个元素,怎么后继是None??				
				raise Exception,'不是最后一个元素,怎么后继是None'

			if tPrevKey is not None:#当前元素不是首元素
				if tPriKey==self.tFirstKey:
					raise Exception,'矛盾了,你都有前趋元素,首元素怎么会是你'

				self.dLink[tPrevKey][1]=tNextKey #修改前趋元素的next指针
			

			#if tNextKey is not None:#当前元素不是尾元素(上面已经判断过了)
			self.dLink[tNextKey][0]=tPrevKey #修改后继元素的prev指针

			if self.dLink[tNextKey][1] is None:#后继元素是最后一个元素
				if tNextKey!=self.tLastKey:
					raise Exception,'说了后继元素是最后一个元素,怎么又不是了'
					
				self.dLink[tNextKey][1]=tPriKey

			if self.tFirstKey==tPriKey:
				self.tFirstKey=tNextKey
	
			self.dLink[tPriKey]=[self.tLastKey,None]

			self.dLink[self.tLastKey][1]=tPriKey #原本最后的元素的后趋指向当前元素
			self.tLastKey=tPriKey

			self.dAddSeq[tPriKey]=self.getCycleSequene()

		elif tPriKey==self.tFirstKey:#当前元素是最后一个元素,并且也是第一个元素(就是只有一个元素)
			#应该重设定时器,并修改加入时间
			self.dAddSeq[tPriKey]=self.getCycleSequene()
			self.__updateTimer()
		else:#当前元素是最后一个元素,但不是第一个元素
			#不用调整链表,不动定时器,但要修改加入的时间戳
			self.dAddSeq[tPriKey]=self.getCycleSequene()

		self.__check()

if 'glJitKeeper' not in globals():#系统中全部的jit keeper实例
	glJitKeeper=[]

import gevent
import gevent.core
import misc
import log
import u
import timer
import config