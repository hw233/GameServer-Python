#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import product

#数据块,抽象类
class cBlock(product.cProduct):
	def __init__(self,sChineseName,*tPriKey):
		product.cProduct.__init__(self,sChineseName,*tPriKey)
		self.sSlStm=self.sUdStm=self.sIsStm=self.sDlStm='' #增删改查的SQL语句
		self.sBackup=None #检查程序员是否漏打脏标志,内服才启用,外服不能用,因为性能差
		self.bInitialized=False #是否初始化完成
		
	def getConnPool(self):#
		return db4ms.gConnectionPool

	def isInitialized(self):#是否初始化完成
		return self.bInitialized
		
	def setIsStm(self,sIsStm):#insert statement
		self.sIsStm=sIsStm
		return self #可以链式调用

	def getIsStm(self):
		return self.sIsStm

	def setDlStm(self,sDlStm):#delete statement
		self.sDlStm=sDlStm
		return self #可以链式调用

	def getDlStm(self):
		return self.sDlStm

	def setUdStm(self,sUdStm):#update statement
		self.sUdStm=sUdStm
		return self #可以链式调用

	def getUdStm(self):
		return self.sUdStm

	def setSlStm(self,sSlStm):#select statement
		self.sSlStm=sSlStm
		return self #可以链式调用

	def getSlStm(self):
		return self.sSlStm

	def getPstObj(self):
		return self

	def _insertToDB(self,*itNoRowInsertValues,**dData):#override
		oPst=self.getPstObj()
		oPst.onBorn(**dData)	#初始化新生数据
		dData=oPst.save()
		self.sBackup=ujson.dumps(dData)
		#oPst.markDirty()#(这里不打脏标记,由onBorn里面来决定是否打脏标记)
		values=[]
		values.extend(self.tPriKey)
		values.append(self.sBackup)
		self.getConnPool().query(self.sIsStm,*values)
		
		self.bInitialized=True
		self._onInitialized()

	def _deleteFromDB(self):#override
		self.getConnPool().query(self.getDlStm(),*self.tPriKey)

	def checkMarkDirty(self):#override 本次存盘数据与上一次的存盘数据对比(只在内服检查程序员的错误)
		if not config.IS_INNER_SERVER:
			return
		dData=self.getPstObj().save()
		sData=ujson.dumps(dData)
		if self.sBackup is not None and not self._equal(self.sBackup,sData):
			try:
				raise Exception,'\'{}\'数据发生了变化,但是漏打脏标志\nsBackup={},sData={}'.format(self.sChineseName,self.sBackup,sData)
			except Exception:
				misc.logException()

	def _equal(self,sBackup,sData):#判断sBackup和sData是否相同
		return sBackup==sData #or ujson.loads(sBackup)==ujson.loads(sData)

	def _saveToDB(self):#override 执行update语句
		oPst=self.getPstObj()
		dData=oPst.save()
		sData=ujson.dumps(dData)
		self.getConnPool().query(self.getUdStm(),sData,*self.tPriKey)		
		if config.IS_INNER_SERVER:
			self.sBackup=sData
		return True

	def _loadFromDB(self):#override 执行select语句
		rs=self.getConnPool().query(self.getSlStm(),*self.tPriKey)
		#print 'rs.rows==',rs.rows
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行			
			return False

		if len(rs.rows[0])!=1:
			raise Exception,'列数只能是1列'
		sData=rs.rows[0][0]
		if sData:
			try:
				dData=ujson.loads(sData)#反序列化
			except Exception:
				u.reRaise('反序列化\'{}\'数据块时出错,主键为{}'.format(self.sChineseName,self.getPriKey()))
		else:
			dData={}

		oPst=self.getPstObj()
		oPst.load(dData)
		
		if config.IS_INNER_SERVER:
			self.sBackup=ujson.dumps(oPst.save())  # save可能新加了一些标记
		
		self.bInitialized=True
		self._onInitialized()
		return True

	def _onInitialized(self):
		pass

#cCtnBlock,各个容器的基类,因为容器对象sava时由于字典访问的无序性,所以可能造成dBackup,dData里面的数据项一样,
#但数据项排列不一样,是的sBackup和sData不同
#此时若sBackup,sData里的数据项相同既可认为它们相等
class cCtnBlock(cBlock):
	def __in99999it__(self,sChineseName,*tPriKey):
		cBlock.__in99999it__(self, sChineseName, *tPriKey)
		
	def _equal999999(self,sBackup,sData):
		if sBackup==sData:
			return True
		print 'sChineseName=',u.trans(self.sChineseName)
		print 'sBackup=',sBackup
		print 'sData=',sData
		dBackup,dData=ujson.loads(sBackup),ujson.loads(sData)
		lBackItem,lCurrItem=dBackup.get('item', []), dData.get('item', [])
		if len(lBackItem)!=len(lCurrItem):
			return False
		#判断lBackItem,lCurrItem里面的数据是否相同,此处性能较差
		#只有在内网角色下线时 或者从keeper移除该ctn时,才会进入此函数
		sPos=set()
		for uData in lBackItem:	
			if uData not in lCurrItem:
				return False
			sPos.add(lBackItem.index(uData))
		return len(sPos)==len(lCurrItem)




import weakref
import copy
import sys
import ujson
#import gevent.event
import db4ms
import timer
import c
import u
import misc
import primitive
import log
import config