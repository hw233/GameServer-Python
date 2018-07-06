#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import keeper

#product对象keeper.肚子里装的是product对象
class cProductkeeper(keeper.cKeeper):
	def __init__(self,oFactory):
		keeper.cKeeper.__init__(self)		
		self.oFactory=oFactory
		self.dLock={}#key映射锁,用于互斥访问(相同key的才互斥,不同key可以并发)
		glProductKeeper.append(self)


		'''
		对于这样的逻辑,可以避免外部使用者加锁.
		如果这里不作lock,如下代码就有bug,因为getObjFromDB里面有协程切换,且从数据库中拉出obj后才addObj.
		if not keeper.getObj():#读
			doSomething()
			keeper.getObjFromDB()#写

		改成下面这个就可以避免外部加锁
		
		if not keeper.getObjWithLock():
			doSomething()
			keeper.getObjFromDB()
		'''


	def getObjWithLock(self,*tPriKey):#
		with primitive.cLockByKey(self.dLock,tPriKey):
			return keeper.cKeeper.getObj(self,*tPriKey)

	def getObjFromDB(self,itNoRowInsertValues,*tPriKey,**dData):#从数据库加载对象,并且交给这个keeper进行管理
		with primitive.cLockByKey(self.dLock,tPriKey):
			obj=self.getObj(*tPriKey)
			if obj:#已经在内存中了.
				return obj
			obj=self.oFactory.getProductFromDB(itNoRowInsertValues,*tPriKey,**dData)#从工厂生产obj
			if not obj:
				return None
			self.addObj(obj,*tPriKey)	
			return self.getObj(*tPriKey)#返回一个代理出去.

	def addObj(self,obj,*tPriKey):#override
		if not isinstance(obj,product.cProduct):
			raise Exception,'必须是product的实例才能加入到keeper里.'
		if isinstance(obj,weakref.ProxyType):
			obj=obj.this()#从proxy取出直实的实例
		keeper.cKeeper.addObj(self,obj,*tPriKey)
		obj.addKeeper(self)		
		
	def removeObj(self,*tPriKey):#override
		with primitive.cLockByKey(self.dLock,tPriKey):
			obj=self.getObj(*tPriKey)
			if obj:
				obj.removeKeeper(self)
				if obj.keeperAmount()<=0:#没有任何keeper持有这个实例了.(事实上可能有其他地方还有强引用这个product对象,不过不是keeper.比如friend里面强引用了resume)
					#if config.IS_INNER_SERVER:
					#	print '在keeper中呆了{},即将踢出keeper,最后一次存盘.主键是{}.obj={}'.format(obj.liveTime(),tPriKey,obj)
					if self.oFactory.isWait2schedule(*tPriKey):#是否正在等待存盘调度
						self.oFactory.saveProduct2db(*tPriKey)#最后一次存盘了.(里面会从存盘队列里移除自己)
					else:
						obj.checkMarkDirty()
			keeper.cKeeper.removeObj(self,*tPriKey)
	
	def removeAllObj(self):#override,基类仅仅是置空,要改为逐个移除
		for tPriKey in self.dObjs.keys():
			self.removeObj(*tPriKey)


'''
DEFAULT_KEEP_TIME=5*60 #默认维持时间(秒)
#jit是 just in time的意思,需要时从临时数据库加载回来,用完差不多就踢回数据库
#N秒后自动从内存中移除对象
#用于玩家邮箱,玩家的宠物店,物品店,玩家的房子.玩家的仓库,等等不需要常驻内存的

class cJITproductKeeper(cProductkeeper):
	def __init__(self,oFactory,fKeepSecond=DEFAULT_KEEP_TIME):#
		cProductkeeper.__init__(self,oFactory)
		if fKeepSecond<=0:
			raise Exception,'fDelay必须大于0,不能是{}'.format(fKeepSecond)
		self.oFactory=oFactory
		self.fKeepSecond=fKeepSecond #持有对象秒数		
		self.dLastAccess={}#记录最后访问时间.
		self.oScheduler=scheduler.cScheduler()#用于一定时间后删除对象的引用#todo:不要检查得太密了
		glJitKeeper.append(self)

	def getObjFromDB(self,itNoRowInsertValues,*tPriKey):#override
		obj=cProductkeeper.getObjFromDB(self,itNoRowInsertValues,*tPriKey)
		if obj:
			self.dLastAccess[tPriKey]=timeU.getStamp()#记录最后访问时间.
		return obj

	def addObj(self,obj,*tPriKey):#override
		cProductkeeper.addObj(self,obj,*tPriKey)		
		self.dLastAccess[tPriKey]=timeU.getStamp()#最后一次访问时间
		self.oScheduler.appendCallLater(u.cFunctor(self.__removeObj,*tPriKey),*tPriKey)	
		
	def removeObj(self,*tPriKey):#override
		cProductkeeper.removeObj(self,*tPriKey)#里面存盘可能会抛异常
		self.dLastAccess.pop(tPriKey,None)#存盘成功后才pop	
		self.oScheduler.removeCallLater(*tPriKey)
		
	def __removeObj(self,*tPriKey):
		#最近还有访问,先别删,下一个周期再检查
		if self.stayAnyway(*tPriKey) or (timeU.getStamp()-self.dLastAccess.get(tPriKey,0)<self.fKeepSecond):
			self.oScheduler.appendCallLater(u.cFunctor(self.__removeObj,*tPriKey),*tPriKey)
		else:#真的删掉
			self.removeObj(*tPriKey)
			#print 'keeper......__removeObj=',tPriKey

	def stayAnyway(self,*tPriKey):#如果不希望从内存中卸载,请在子类override,并返回True值
		return False

	def getObj(self,*tPriKey):#override
		obj=cProductkeeper.getObj(self,*tPriKey)
		if obj:
			self.dLastAccess[tPriKey]=timeU.getStamp()#记录最后访问时间.
		return obj
	
if 'glJitKeeper' not in globals():#系统中全部的jit keeper实例
	glJitKeeper=[]
	
'''

if 'glProductKeeper' not in globals():#系统中全部的Product keeper实例
	glProductKeeper=[]

import weakref
import timeU
import misc
import log
import u
import scheduler
import product
import primitive
import config