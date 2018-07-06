#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#ctn -> container

#抽象类
#包裹装备,任务,技能,称号,成就,坐骑,宠物....等等容器的基类
import pst
class cContainerBase(pst.cEasyPersist):
	def __init__(self,iOwnerId):
		pst.cEasyPersist.__init__(self,self._dirtyEventHandler)
		self.iOwnerId=iOwnerId
		self.dKeyMapItem={} #collections.OrderedDict() #使用有序字典,后来发现有序字典会造成循环引用,是标准库实现得不理想

	@property
	def ownerId(self):#拥有者id
		return self.iOwnerId

	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId
		
	def getOwnerObj(self):
		return getRole(self.ownerId)

	def itemCount(self):#子项总数
		return len(self.dKeyMapItem)

	def getItem(self,iKey):#根据键值获取子项
		return self.dKeyMapItem.get(iKey,None)

	#返回所有子项
	def getAllItems(self):
		return self.dKeyMapItem.iteritems()

	#返回全部键
	def getAllKeys(self):
		return self.dKeyMapItem.iterkeys()

	#返回全部值
	def getAllValues(self):
		return self.dKeyMapItem.itervalues()

	def __repr__(self):
		l=[]
		for k,v in self.dKeyMapItem.iteritems():
			l.append('key={},name={}'.format(v.key,v.name))
		return '\n'.join(l) if l else pst.cEasyPersist.__repr__(self)

	def _dirtyEventHandler(self):
		raise NotImplementedError,'请在子类实现,把本对象加入到存盘调度队列'
	
	@property
	def endPoint(self):
		raise NotImplementedError,'请在子类实现'

	def _rpcAddItem(self,obj):
		raise NotImplementedError,'请在子类实现,调用rpc方法发包给客户端'

	def _rpcRemoveItem(self,obj):
		raise NotImplementedError,'请在子类实现,调用rpc方法发包给客户端'

	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		for obj in self.getAllValues():			
			self._rpcAddItem(obj)			

	def callSetup4allItem(self):#对全部成员对象调用setup,在角色实例加载成功后调用.
		ownerObj = self.getOwnerObj()
		if not ownerObj:
			return
		for obj in self.dKeyMapItem.values():
			self.setup(obj)

	def _initItem4container(self,obj,uData=None):#从数据库中load回来,新增进来都会走这里
		uKey=obj.key
		if uKey in self.dKeyMapItem:
			raise Exception,'key为{}的子项已经存在:{}'.format(uKey, getattr(self, "sChineseName", ""))
		self.dKeyMapItem[uKey]=obj
		obj.eDirtyEvent+=self._dirtyEventHandler
		obj.ownerId = self.ownerId
		return True

	def addItem(self,obj):#新增子项
		if not self._initItem4container(obj,None):#也要走数据库load回来的流程.
			return False

		self.markDirty()
		self._rpcAddItem(obj)
		self.setup(obj)
		return True
	
	def setup(self, obj, isLogin=False):
		pass

	def removeItem(self,obj):#移除子项
		iKey=obj.key
		return self.removeItemByKey(iKey)
	
	def removeItemByKey(self, iKey):
		'''根据key移除子项
		'''
		if iKey not in self.dKeyMapItem:
			return False

		obj = self.dKeyMapItem.pop(iKey)
		obj.eDirtyEvent-=self._dirtyEventHandler
		obj.ownerId = 0
		self.markDirty()
		self._rpcRemoveItem(obj)
		self.cancelSetup(obj)
		return True
	
	def cancelSetup(self, obj):
		pass
	
	def clearAll(self): # 清除所有子项
		objList = self.dKeyMapItem.values()
		for obj in objList:
			self.removeItem(obj)
	
	def hasItem(self,obj):
		return obj.key in self.dKeyMapItem

	def _createAndLoadItem(self,iIndex,uData):
		raise NotImplementedError,'请在子类实现'

	def _saveItem(self,iIndex,obj):#生成子项的保存数据
		dData=obj.save()
		if dData is None:
			return None
		if dData:
			return (obj.key,dData)
		else:
			return obj.key

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		for iIndex,uData in enumerate(dData.pop('item',[])):
			obj=self._createAndLoadItem(iIndex,uData)
			if obj:
				self._initItem4container(obj,uData)
				
		# self.callSetup4allItem()

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		lItem=[]
		for iIndex,obj in enumerate(self.dKeyMapItem.itervalues()):
			uData=self._saveItem(iIndex,obj)
			if uData is not None:
				lItem.append(uData)
		if lItem:
			dData['item']=lItem
		return dData

	def refresh(self):#发送到客户端,一般是登录时调用
		self._rpcRefresh()

	def takeItem(self,iKey):#根据键值获取子项,如果没有就取公共对象(一般用于玩家还没有获得,但是又需要显示在ui上的,比如技能,成就)
		obj=self.dKeyMapItem.get(iKey,None)#先从自己的容器中找
		if not obj:#找不到,从共同对象中找
			obj=self._takePublicItem(iKey)
		return obj

	def _takePublicItem(self,iKey):
		raise NotImplementedError,'请在子类override实现,获取公共对象'
	

class LevelContainer(cContainerBase):
	'''等级对象管理器，如技能、阵法
	'''

	def setLevel(self, key, level):
		'''设置等级，如果没有该对象则创建
		'''
		obj = self.getItem(key)
		if level == 0: # 删除
			if obj:
				obj.level = 0
				self.removeItem(obj)
			return obj
		
		if obj:
			self.setItemLevel(obj, level)
		else:
			obj = self._newItem(key)
			obj.level = level
			self.addItem(obj)

		return obj
	
	def getLevel(self, key):
		'''获取等级
		'''
		obj = self.getItem(key)
		if obj:
			return obj.level
		return 0
	
	def setItemLevel(self, obj, level):
		obj.level = level
		self._rpcSetLevel(obj)
			
	def _newItem(self, key):
		raise NotImplementedError, "请在子类实现"
	
	def _rpcSetLevel(self, obj):
		raise NotImplementedError, "请在子类实现"

from common import *
