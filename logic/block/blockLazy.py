#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst
import block

#玩家惰性数据 (变化不频繁的数据存这里,可以减少存盘频率,比如门派,角色1级属性等等)
class cRoleLazyBlock(block.cBlock,pst.cEasyPersist):
	def __init__(self,iRoleId):#override
		self.iRoleId=iRoleId
		block.cBlock.__init__(self,'玩家基础数据块',iRoleId)
		pst.cEasyPersist.__init__(self,self._dirtyEventHandler)
		self.setIsStm(sql.LAZY_INSERT)
		self.setDlStm(sql.LAZY_DELETE)
		self.setUdStm(sql.LAZY_UPDATE)
		self.setSlStm(sql.LAZY_SELECT)
		self.schemeCtn=cSchemeCantainer(self)#方案容器
		self.alchemyCtn=cAlchemyCantainer(self)#炼丹容器
		self.fashionCtn=cFashionCantainer(self)#时装容器

	def onBorn(self):#override
		self.set("newbie",1)
		for attr in role.defines.baseAttrList:
			self.set(attr, 10)#设置系统分配的一级属性	
		
		self.schemeCtn.onBorn()

	def _dirtyEventHandler(self):#override
		factoryConcrete.lazyFtr.schedule2tail4save(self.iRoleId)

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.schemeCtn.load(dData.pop('sch',{}))
		self.alchemyCtn.load(dData.pop('alch',{}))
		self.fashionCtn.load(dData.pop('fashion',{}))

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData['sch']=self.schemeCtn.save()
		dData['alch']=self.alchemyCtn.save()
		dData['fashion']=self.fashionCtn.save()
		return dData

#角色加点方案容器
class cSchemeCantainer(pst.cEasyPersist):
	def __init__(self,shellObj):#override
		pst.cEasyPersist.__init__(self,shellObj._dirtyEventHandler)
		self.shellObj=weakref.proxy(shellObj)
		self.iScheme=1 #当前加点方案
		self.dScheme={}

	def onBorn(self):#override		
		self.dScheme[1]=cScheme(self.shellObj._dirtyEventHandler)#新生角色预给一套加点方案


	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)		
		for iScheNo,dSche in dData.pop('sche',{}).iteritems():
			obj=cScheme(self.shellObj._dirtyEventHandler)
			obj.load(dSche)
			self.dScheme[iScheNo]=obj
		self.iScheme=dData.pop('curSche',1)


	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData['curSche']=self.iScheme
		d={}
		for iScheNo,obj in self.dScheme.iteritems():
			d[iScheNo]=obj.save()
		dData['sche']=d
		return dData


	def getCurSchemeNo(self):
		return self.iScheme
		
	def getScheme(self,iScheme=0):#返回一个加点方案,默认返回当前正在使用的方案
		if iScheme==0:
			iScheme=self.iScheme
		return self.dScheme.get(iScheme,None)

	def switchScheme(self,iScheme,iLv):#切换加点方案
		if iScheme>3:			
			raise Exception,'只允许有3套方案'
		if iScheme not in self.dScheme:#刚启用新方案
			obj=cScheme(self.shellObj._dirtyEventHandler)
			obj.add('point',iLv*5) #
			self.dScheme[iScheme]=obj

		self.iScheme=iScheme
		self.markDirty()	

	def getAllScheme(self):
		return self.dScheme.itervalues()

class cScheme(pst.cEasyPersist):#起个别名
	pass

#炼丹容器
class cAlchemyCantainer(pst.cEasyPersist):
	def __init__(self,shellObj):#override
		pst.cEasyPersist.__init__(self,shellObj._dirtyEventHandler)
		self.shellObj=weakref.proxy(shellObj)
		self.iAnima=0#灵气
		self.dAlchemy={}

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)		
		for iPropsNo,d in dData.pop('alist',{}).iteritems():
			obj=cAlchemy(self.shellObj._dirtyEventHandler)
			obj.load(d)
			self.dAlchemy[iPropsNo]=obj
		self.iAnima=dData.pop('anima',0)

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData['anima']=self.iAnima
		d={}
		for iPropsNo,obj in self.dAlchemy.iteritems():
			d[iPropsNo]=obj.save()
		dData['alist']=d
		return dData

	def getAnima(self):
		return self.iAnima

	def addAnima(self,iAdd):
		self.iAnima+=iAdd
		if self.iAnima>3000:
			self.iAnima=3000
		elif self.iAnima<0:
			self.iAnima=0
		self.markDirty()
		return self.iAnima

	def addAlchemy(self,iPropsNo):
		obj=cAlchemy(self.shellObj._dirtyEventHandler)
		self.dAlchemy[iPropsNo]=obj
		self.markDirty()
		return obj

	def removeAlchemy(self,iPropsNo):
		obj=None
		if iPropsNo in self.dAlchemy:
			obj=self.dAlchemy.pop(iPropsNo)
			self.markDirty()
		return obj

	def getAlchemy(self,iPropsNo):
		return self.dAlchemy.get(iPropsNo,None)

	def getAllAlchemy(self):
		return self.dAlchemy.items()


class cAlchemy(pst.cEasyPersist):
	pass


#角色时装容器
class cFashionCantainer(pst.cEasyPersist):
	def __init__(self,shellObj):#override
		pst.cEasyPersist.__init__(self,shellObj._dirtyEventHandler)
		self.shellObj=weakref.proxy(shellObj)
		self.iFashion=1 #当前时装
		self.dFashion={}

	def onBorn(self):#override
		self.dFashion[1]=cFashion(self.shellObj._dirtyEventHandler)#新生角色默认为第0号时装

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		for iFashionNo, dFashion in dData.pop("fashion",{}).iteritems():
			obj=cFashion(self.shellObj._dirtyEventHandler)
			obj.load(dFashion)
			self.dFashion[iFashionNo]=obj
		self.iFashion=dData.pop("curFashion", 0)

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData["curFashion"]=self.iFashion
		d={}
		for iFashionNo,obj in self.dFashion.iteritems():
			d[iFashionNo]=obj.save()
		dData['fashion']=d
		return dData

	def getCurFashionNo(self):
		return self.iFashion

	def getFashion(self,iFashionNo=0):#返回一个时装
		if iFashionNo==0:
			iFashionNo=self.iFashion
		return self.dFashion.get(iFashionNo,None)

	def switchFashion(self, iFashionNo, shapeParts, colors):#切换时装
		if iFashionNo not in self.dFashion:#新方案新时装
			obj=cFashion(self.shellObj._dirtyEventHandler)
			obj.set("parts", shapeParts)
			obj.set("colors", colors)
			self.dFashion[iFashionNo]=obj
		self.iFashion=iFashionNo
		self.markDirty()

	def updateFashion(self, iFashionNo, shapeParts, colors):
		'''时装染色后更新
		'''
		if iFashionNo not in self.dFashion:
			self.switchFashion(iFashionNo, shapeParts, colors)
			return
		self.markDirty()
		obj = self.dFashion[iFashionNo]
		obj.set("parts", shapeParts)
		obj.set("colors", colors)

	def getAllFashion(self):
		return self.dFashion.itervalues()

class cFashion(pst.cEasyPersist):#时装
	pass


import weakref
import sql
import factoryConcrete
import role.defines
import u
