#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#pst -> persist

#可持久化类(抽象类)
class cPersist(object):
	def __init__(self,cDirtyHandler=None):
		self.eDirtyEvent=u.cEvent()

		if cDirtyHandler!=None:
			if not callable(cDirtyHandler):
				raise Exception,'{}不是可呼叫类型.'.format(cDirtyHandler)
			self.eDirtyEvent+=cDirtyHandler

	def markDirty(self):#标示为脏数据
		self._onDirty()

	def _onDirty(self):	
		self.eDirtyEvent()#触发事件

	def onBorn(self,*tArgs,**dArgs):
		pass

	def save(self):
		raise NotImplementedError,'请在子类override,记得返回一个dict哦'

	def load(self,dData):
		raise NotImplementedError,'请在子类override'

#非常易于使用的persist对象
class cEasyPersist(cPersist):
	def __init__(self,cDirtyHandler=None):
		cPersist. __init__(self,cDirtyHandler)
		self.dData={}

	def add(self,uKey,uValue,uDefault=0):#返回成功后的结果值
		self.dData[uKey] = self.dData.get(uKey,uDefault)+int(uValue)
		self.markDirty()
		return self.dData[uKey]

	def delete(self,uKey,uDefault=0):
		if uKey in self.dData:
			self.markDirty()
			return self.dData.pop(uKey)
		return uDefault

	def set(self,uKey,uValue):
		if uValue==None:
			raise Exception,'参数uValue不能是None'
		# elif type(uValue)==types.FloatType:
			# raise Exception,'参数uValue不能是float类型'
		elif type(uValue)==types.BooleanType:
			raise Exception,'bool类型存成0或1就行,不要存成True或False,以减少存盘数据'
		#elif self.dData.get(uKey)==uValue:#不能比,容器类型值总是同一个引用
		#	return
		self.dData[uKey]=uValue
		self.markDirty()
		return self #可以链式调用

	def fetch(self,uKey,uDefault=0):#默认值是0更合理
		return self.dData.get(uKey,uDefault)

	def hasKey(self,uKey):
		return uKey in self.dData

	def save(self):#override
		return self.dData.copy()
		#因为返回dict后子类会往里面加东西,dict是引用类型,导致永久性存在
		#返回一个浅拷贝,即使被修改也不会影响到原来的dict

	def load(self,dData):#override
		self.dData=dData
		
	#iFlag	需要处理的标志位
	#bVal	标志位取正还是取反
	def setFlag(self, iFlag,bVal):
		iKey=0
		while iFlag>=(2**32):
			iFlag>>=32
			iKey+=1
	
		dBool=self.fetch('bool',{})
		iBitMap=dBool.get(iKey,0)
		if bVal:
			iBitMap=iFlag|iBitMap
		else:
			iBitMap=~iFlag&iBitMap
		dBool[iKey]=iBitMap
		self.set('bool',dBool)
	
	#返回值是bool型
	def getFlag(self, iFlag):#没有办法实现默认值
		iKey=0
		while iFlag>=(2**32):
			iFlag>>=32
			iKey+=1
		return self.fetch('bool',{}).get(iKey,0)&iFlag		

class cMergePersist(cPersist):#把多个persist对象组合成一个persist对象
	def __init__(self,dObjList,cDirtyHandler=None):
		cPersist. __init__(self,cDirtyHandler)
		self.dObjList=dObjList

	def load(self,dData):#override
		for sKey,obj in self.dObjList.iteritems():
				obj.load(dData.get(sKey,{}))

	def save(self):#override
		dData={}
		for sKey,obj in self.dObjList.iteritems():
			dTemp=obj.save()
			if dTemp:
				dData[sKey]=dTemp
		return dData

	def onBorn(self,*tArgs,**dArgs):#override
		for sKey,obj in self.dObjList.iteritems():
			obj.onBorn(*tArgs,**dArgs)

import copy
import types
import weakref
import u
