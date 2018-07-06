#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import product

#多字段类,抽象类
#一个属性占数据表一列(对于需要统计的列)
class cMultiField(product.cProduct):
	def __init__(self,sChineseName,*tPriKey):
		product.cProduct.__init__(self,sChineseName,*tPriKey)
		self.sSlStm=self.sUdStm=self.sIsStm=self.sDlStm='' #增删改查的SQL语句
		#self.tBackup=None
		self.eDirtyEvent=u.cEvent()#数据发生变化的事件.
		self.eDirtyEvent+=self._dirtyEventHandler

	def _dirtyEventHandler(self):
		raise Exception,'请在子类实现,把本对象加入到存盘调度队列.'

	def setIsStm(self,sIsStm):#insert statement
		self.sIsStm=sIsStm
		return self

	def getIsStm(self):
		return self.sIsStm

	def setDlStm(self,sDlStm):#delete statement
		self.sDlStm=sDlStm
		return self

	def getDlStm(self):
		return self.sDlStm

	def setUdStm(self,sUdStm):#update statement
		self.sUdStm=sUdStm
		return self

	def getUdStm(self):
		return self.sUdStm

	def setSlStm(self,sSlStm):#select statement
		self.sSlStm=sSlStm
		return self

	def getSlStm(self):
		return self.sSlStm

	def _getWatchNames(self):
		raise NotImplementedError,'请把要观察的变量名提供上来'

	def __setattr__(self,sName,uNewValue):#override 检查数据是否发生变化,为了触发一下事件.
		uOldValue=getattr(self,sName,None)
		object.__setattr__(self,sName,uNewValue)

		if uOldValue is None:#原来没有这个属性,本次是第一次设值,一般第一次是指def __init__()里面的赋值.
			return
		if sName not in self._getWatchNames():#不在观察列表里.
			return
		if uNewValue==uOldValue:#新旧值是相同的,没有发生变化
			return		
		if getattr(self,'eDirtyEvent',None) is not None:#
			self._onDirty(sName,uNewValue)			

	def _onDirty(self,sName,uNewValue):
		self.eDirtyEvent()#触发事件.

	#select语句返回结果集的列数,对着sql.py里的语句数就行了
	def _getSelectRecordsetFieldCount(self):
		raise NotImplementedError,'请在子类实现'

	#返回tuple,update语句各字段的值,不包括主键,要与sql语句的参数顺序相同
	def _getValuesTuple4Update(self):
		raise NotImplementedError,'请在子类实现'

	#select返回0行时,设置各内存中的成员变量值
	def _setSelectNoRecordsetDefaultValues(self,*itNoRowInsertValues):
		raise NotImplementedError,'请在子类实现'

	def _setValuesAfterSelect(self,*tValues):#select成功返回1行数据时,设置内存变量
		raise NotImplementedError,'请在子类实现'

	def _insertToDB(self,*itNoRowInsertValues,**dData):#override
		db4ms.gConnectionPool.query(self.getIsStm(),*itNoRowInsertValues)
		self._setSelectNoRecordsetDefaultValues(*itNoRowInsertValues)

	def _deleteFromDB(self):#override
		db4ms.gConnectionPool.query(self.getDlStm(),*self.tPriKey)

	def _saveToDB(self):#override,执行update语句
		tValues=self._getValuesTuple4Update()
		db4ms.gConnectionPool.query(self.getUdStm(),*(tValues+self.tPriKey))
		#self.tBackup=tValues
		return True

	def _loadFromDB(self):#override,执行select语句
		rs=db4ms.gConnectionPool.query(self.getSlStm(),*self.tPriKey)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return False

		iFieldCount=self._getSelectRecordsetFieldCount()
		if len(rs.rows[0])!=iFieldCount:
			raise Exception,'列数不足{}列'.format(iFieldCount)
		self._setValuesAfterSelect(*rs.rows[0])
		#self.tBackup=rs.rows[0]
		return True
		
import db4ms
import u
