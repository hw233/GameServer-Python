#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import u
import c
import keeper
import gevent.event

#SEE_AMOUNT=10 #每个人所能看到玩家的个数

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'sceneService' in SYS_ARGV:		
		gSceneKeeper=keeper.cKeeper()#场景实例存放处
		# gSceneProxy = u.cKeyMapProxy()#用主服务器的场景id关联场景对象
		gEnginerSceneProxy = u.cKeyMapProxy()#用引擎层的实体id关联实体对象

#场景
class cScene(object):#场景基类
	def __init__(self, iScriptSceneId, iWidth, iHeight, iRes, iBroadcastRole):
		self.iWidth,self.iHeight = iWidth, iHeight	#场景可行走区域的宽与高
		self.iRes = iRes
		self.iBroadcastRole = iBroadcastRole #特殊处理是否能看到其它玩家（0:可以 1：不可以）
		#iPhone 6 Plus:1242*2208 -->49.68*88.32
		#iPad Retina:1546*2048 -->61.84*81.92
		#宽高都取最大-->61.84*88.32 各除以3-->20.6133*29.4399
		# iGridWidth,iGridHeight=30,21
		iGridWidth,iGridHeight=45,31 #底层用9宫格iGridWidth,iGridHeight=宽高都取最大-->61.84*88.32 各除以2
		#客户端的位置从1开始计算，所以传入底层的场景iWidth iHeight要加1
		if iGridWidth > self.iWidth+1:
			iGridWidth = self.iWidth+1
		if iGridHeight > self.iHeight+1:
			iGridHeight = self.iHeight+1
		self.handle = zfmPyEx.createScene(self.iWidth+1,self.iHeight+1,iGridWidth,iGridHeight)
		if not self.handle:
			raise Exception,'场景创建失败'

		self.iScriptSceneId = iScriptSceneId #脚本层id
		self.dEttByType = {}		#用实体的类型分类存放obj的id
		self.dEttById = {}			#实体id映射obj
		self.iEngineSceneId = self.handle.iSceneId 	#引擎层的场景id
		gEnginerSceneProxy.addObj(self, self.iEngineSceneId)

		# gSceneProxy.addObj(self,iScriptSceneId)
		#u.regDestructor(self,lambda:zfmPyEx.delScene(self.iScriptSceneId))

	@property
	def scriptSceneId(self):
		return self.iScriptSceneId

	@property
	def engineSceneId(self):
		return self.iEngineSceneId

	@property
	def res(self):
		return self.iRes

	def BroadcastRole(self):
		return self.iBroadcastRole

	def isBroadcastRole(self):
		if self.iBroadcastRole == 0:
			return True
		return False

	def getEntityIdsByType(self,iEttType):#获得某一类的实体全部id
		for iScriptEttId in self.dEttByType.get(iEttType,set()):
			yield iScriptEttId

	def removeEntityByType(self, iEttType):#仅仅是从场景上移除此实体.
		if iEttType not in self.dEttByType:
			return
		s=self.dEttByType[iEttType]	
		for iScriptEttId in set(s):
			self.removeEntity(iScriptEttId,self.dEttById[iScriptEttId])
		self.dEttByType.pop(iEttType,None)


	def isNotifyToC(self, oEtt):
		'''增加/删除/移动/实体 等是否需要通知C层
		'''
		if oEtt.isRole():#
			if not self.isBroadcastRole():
				return False
		return True

	def addEntity(self,oEtt,x,y):
		'''场景加入实体
		'''
		iScriptEttId,iEttType=oEtt.scriptEttId,oEtt.ettType
		iOldSceneId = oEtt.sceneId
		if iOldSceneId:# and iOldSceneId != self.iScriptSceneId:
			#先从旧场景移除处
			# zfmPyEx.removeEttFromScene(oEtt.iEngineEttId)
			oOldScene = gSceneKeeper.getObj(iOldSceneId)
			if oOldScene:
				oOldScene.removeEntity(iScriptEttId)
		if x > self.iWidth or y > self.iHeight:
			sceneService.sceneServerLog("service4main", "addEntity error:iScriptSceneId={},self.iWidth={},self.iHeight={},oEtt.scriptEttId={},x={},y={},".format(self.iScriptSceneId,self.iWidth, self.iHeight, oEtt.scriptEttId, x, y))
			return
		
		oEtt.setXY(x, y)
		oEtt.setSceneId(self.iScriptSceneId)
		if iScriptEttId not in self.dEttById:#实体已经在场景里
			self.dEttById[iScriptEttId]=oEtt
			self.dEttByType.setdefault(iEttType,set()).add(iScriptEttId)
		zfmPyEx.addEntity(oEtt.iEngineEttId,self.engineSceneId,x,y)

	def removeEntity(self,iScriptEttId,iEttType=None):
		'''从场景上移除ett		
		'''
		oEtt=entity4ss.getEttByScriptId(iScriptEttId)
		if not oEtt:
			return
		zfmPyEx.removeEttFromScene(oEtt.iEngineEttId)#不需提供场景id

		oEtt=self.dEttById.pop(iScriptEttId,None) #pop出来的是强引用,覆盖掉oEtt这个proxy,避免下面的oEtt是no longer exist
		if oEtt and not iEttType:
			iEttType = oEtt.ettType
		if iEttType in self.dEttByType:
			self.dEttByType[iEttType].discard(iScriptEttId)
		
	def removeAllEntity(self):
		'''移除掉全部场景实体
		'''
		for iScriptEttId,iType in self.dEttById.items():
			self.removeEntity(iScriptEttId,iType)
				
	def height(self):
		return self.iHeight

	def width(self):
		return self.iWidth

	def getRoleIds(self):
		return self.dEttById.keys()

	def broadcastByXY(self,x,y,sPacket,uIgnoreId=()):
		'''根据座标进行场景广播
		'''
		if not self.isBroadcastRole():
			return
		lIds=zfmPyEx.getSurroundIdByXY(self.iEngineSceneId,x,y) #todo 仅拿玩家就好了
		for iEngineEttId in lIds:
			oEntity = entity4ss.getEttByEngineId(iEngineEttId)
			if not oEntity or oEntity.ettType != entity.ETT_TYPE_ROLE:
				continue
			if uIgnoreId and oEntity.scriptEttId in uIgnoreId:
				continue
			oEntity.send(sPacket)

#=======================================================
#=======================================================			

#生成场景实例
def new(iScriptSceneId, iWidth, iHeight, iRes, iBroadcastRole):
	obj=cScene(iScriptSceneId, iWidth, iHeight, iRes, iBroadcastRole)
	gSceneKeeper.addObj(obj,iScriptSceneId)
	return obj

def getSceneByScriptId(iScriptSceneId):
	return gSceneKeeper.getObj(iScriptSceneId)

def getSceneByEngineId(iEngineSceneId):
	return gEnginerSceneProxy.getProxy(iEngineSceneId)
	
import entity4ss
import entity
import sceneService
import zfmPyEx
import gevent.timeout
import gevent
