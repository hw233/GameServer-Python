#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import u
import c
import keeper
import gevent.event

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'sceneService' in SYS_ARGV:		
		gEntityKeeper=keeper.cKeeper()#实体实例存放处
		# gEntityProxy = u.cKeyMapProxy()#用主服务器的实体id关联实体对象
		gEnginerEntityProxy = u.cKeyMapProxy()#用引擎层的实体id关联实体对象

#实体基类
class cEntity(object):
	def __init__(self, iScriptEttId, iEttType, sBaseSerialized):
		self.handle = zfmPyEx.createEntity(iEttType)
		if not self.handle:
			raise Exception,'实体创建失败'
		self.iScriptEttId=iScriptEttId #脚本层id	
		self.iEngineEttId=self.handle.iEttId #引擎层的实体id
		self.iEttType=iEttType
		self.sBaseSerialized = sBaseSerialized	#序列化好的外观数据
		self.sEnterSerialized = ""
		self.sLeaveSerialized = ""
		gEnginerEntityProxy.addObj(self, self.iEngineEttId)
		self.iSceneId = 0
		self.x,self.y=0,0
		# self.iSceneIncreaseId = 0	#每切换一次场景加1
			
	@property
	def scriptEttId(self):
		return self.iScriptEttId

	@property
	def engineEttId(self):
		return self.iEngineEttId		

	@property
	def ettType(self):#获得实体类型
		return self.iEttType

	@property
	def sceneId(self):
		return self.iSceneId

	@property
	def sceneObj(self):
		return sceneService.scene4ss.gSceneKeeper.getObj(self.iSceneId)

	@property
	def sceneIncreaseId(self):	#暂时没用
		return self.iSceneIncreaseId

	@property
	def endPoint(self):
		raise NotImplementedError,'请在子类实现.'

	def setSceneId(self, iSceneId):
		self.iSceneId = iSceneId
		self.sEnterSerialized = ''

	def setXY(self,x,y):
		self.x,self.y=x,y
		self.sEnterSerialized = ''

	def setBaseSerialized(self, sBaseSerialized):
		self.sBaseSerialized = sBaseSerialized
		self.sEnterSerialized = ''

	def isRole(self):
		return False

	def getEntityEnter(self, x, y):  # 实体进入视野
		if not self.sEnterSerialized:
			entityEnter = scene_pb2.entityEnter()
			entityEnter.iEttId = self.iScriptEttId
			entityEnter.iEttType = self.iEttType
			entityEnter.sSerializedEtt = self.sBaseSerialized
			entityEnter.iX = x
			entityEnter.iY = y
			entityEnter.iSceneId = self.iSceneId
			self.sEnterSerialized = endPoint.makePacket('rpcEttEnter', entityEnter)
		return self.sEnterSerialized

	def getSerializedGroup(self, x, y):
		yield self.getEntityEnter(x, y)

	def getLeaveMsgSerialized(self):
		'''序列化后的离开消息(离开场景时广播给周围的玩家)
		'''
		if not self.sLeaveSerialized:#防止重复序列化
			oLeaveMsg=scene_pb2.entityLeave()
			oLeaveMsg.iEttId = self.iScriptEttId
			#oLeaveMsg.iEttType=self.ettType
			self.sLeaveMsgSerialized = endPoint.makePacket('rpcEttLeave',oLeaveMsg)
		return self.sLeaveMsgSerialized

	def onEntityEnter(self, oEtt, x, y):#将oEtt的信息发给自己
		raise NotImplementedError,'请在子类实现.'

	def onEntityMove(self, oEtt, x, y):#将oEtt的信息发给自己
		raise NotImplementedError,'请在子类实现.'

	def onEntityLeave(self, oEtt):#将oEtt离开的信息发给自己
		raise NotImplementedError,'请在子类实现.'

	def switchScene(self, sSwitchSerialized, x, y):
		'''发包给客户端,已不用
		'''
		pass

	def send(self, sPacket):
		raise NotImplementedError,'请在子类实现.'

	def inTeam(self):
		'''是否在队
		'''
		return None

	def getTeamObj(self):
		return None

	# def getRelatedEttList(self, leader=False):
	# 	'''获取有的实体列表，包括自身
	# 	'''
	# 	return [self]

	def getTeamEttId(self):
		'''获取有的实体ID列表，包括自身
		'''
		return []

	def isTeamMember(self):
		return False

#========================================
#========================================
#传送门
class cEntityDoor(cEntity):
	pass

#NPC
class cEntityNpc(cEntity):
	pass

#========================================
#========================================
#角色
class cEntityRole(cEntity):#实体基类
	def __init__(self, iScriptEttId, iEttType, sBaseSerialized):
		cEntity.__init__(self, iScriptEttId, iEttType, sBaseSerialized)
		self.iTeamId = 0
		# self.lSeeMeEtt = [] #在地图上,全部看得见我的角色id
		# self.lSeeOtherEtt = [] #在地图上,我看得到的角色id

	def isRole(self):
		return True

	def setTeamId(self, teamId):
		self.iTeamId = teamId

	@property
	def teamId(self):
		return self.iTeamId

	@property
	def endPoint(self):
		return sceneService.gRoleIdMapEndPoint.getProxy(self.iScriptEttId)

	def send(self, sPacket):
		ep=self.endPoint
		if ep:
			ep.send(sPacket)

	def getEntityEnter(self, x, y):
		'''角色进入视野包，因为x y sceneId经常变化 所以不保存
		'''
		entityEnter = scene_pb2.entityEnter()
		entityEnter.iEttId = self.iScriptEttId
		entityEnter.iEttType = self.iEttType
		entityEnter.sSerializedEtt = self.sBaseSerialized
		entityEnter.iX = x
		entityEnter.iY = y
		entityEnter.iSceneId = self.iSceneId
		return endPoint.makePacket('rpcEttEnter', entityEnter)

	def getSerializedGroup(self, x, y):
		yield self.getEntityEnter(x, y)
		
		teamObj = self.getTeamObj()
		if teamObj and teamObj.isLeader(self.iScriptEttId):
			teamMakeInfo = teamObj.packTeamMakeInfo()
			yield endPoint.makePacket('rpcTeamBroadcastMake', teamMakeInfo)

	def onEntityEnter(self, oEtt, x, y):
		'''进入：将oEtt的信息发给自己
		'''
		if self.iScriptEttId == oEtt.iScriptEttId:
			return
		itPacket = oEtt.getSerializedGroup(x, y)
		for sPacket in itPacket:
			self.send(sPacket)

		# if oEtt.iScriptEttId not in self.lSeeOtherEtt:
		# 	self.lSeeOtherEtt.append(oEtt.iScriptEttId)
		# else:
		# 	print "有BUG，重复进入实体视野：(%s,%s)"%(oEtt.iScriptEttId, self.iScriptEttId)
		# sceneService.sceneServerLog("aoiInfo", "onEntityEnter 实体{},{}进入实体{},{}视野范围内({},{},{})".format(oEtt.iScriptEttId,oEtt.iEngineEttId,self.iScriptEttId,self.iEngineEttId,oEtt.iSceneId,x,y))

	def onEntityMove(self, oEtt, x, y):
		'''移动：将oEtt的信息发给自己
		'''
		if self.iScriptEttId == oEtt.iScriptEttId:
			return
		msg = scene_pb2.moveInfo()
		msg.iEttId = oEtt.iScriptEttId
		msg.x = x
		msg.y = y
		self.send(endPoint.makePacket("rpcEttMove", msg))
		# sceneService.sceneServerLog("aoiInfo", "onEntityMove 实体{},{}在实体{},{}视野范围内移动到({},{},{})".format(oEtt.iScriptEttId,oEtt.iEngineEttId,self.iScriptEttId,self.iEngineEttId,oEtt.iSceneId,x,y))
		# if oEtt.iScriptEttId not in self.lSeeOtherEtt:
		# 	print "有BUG，没有进入实体视野就开始移动了：(%s,%s)"%(oEtt.iScriptEttId, self.iScriptEttId)

	def onEntityLeave(self, oEtt):
		'''离开：将oEtt的信息发给自己
		'''
		if self.iScriptEttId == oEtt.iScriptEttId:
			return
		self.send(oEtt.getLeaveMsgSerialized())

		# if oEtt.iScriptEttId not in self.lSeeOtherEtt:
		# 	print "有BUG，没有进入实体视野就发离开视野：(%s,%s)"%(oEtt.iScriptEttId, self.iScriptEttId)
		# else:
		# 	self.lSeeOtherEtt.remove(oEtt.iScriptEttId)
		# sceneService.sceneServerLog("aoiInfo", "onEntityLeave 实体{},{}离开实体{},{}视野".format(oEtt.iScriptEttId,oEtt.iEngineEttId,self.iScriptEttId,self.iEngineEttId))

	def switchScene(self, sSwitchSerialized, x, y):
		'''发切换场景包给客户端,已不用
		'''
		self.send(sSwitchSerialized)
		self.setXY(x, y)
		# self.iSceneIncreaseId = iSceneIncreaseId
		# sceneService.sceneServerLog("aoiInfo", "SwitchScene {},{},{},{}".format(self.iScriptEttId,self.iEngineEttId,x,y))

	def inTeam(self):
		'''是否在队
		'''
		if not self.iTeamId:
			return None
		ssteamObj = sceneService.team4ss.getSSTeam(self.iTeamId)
		if ssteamObj and self.iScriptEttId in ssteamObj.getInTeamList():
			return ssteamObj
		return None

	def getTeamObj(self):
		if not self.iTeamId:
			return None
		return sceneService.team4ss.getSSTeam(self.iTeamId)

	# def getRelatedEttList(self, leader=False):
	# 	'''获取有的实体列表，包括自身
	# 	'''
	# 	EntityList = [self]	#整个队伍的实体列表
	# 	ssTeamObj = self.getTeamObj()
	# 	if ssTeamObj:			#有队伍，要整个队伍进入
	# 		if leader and ssTeamObj.isLeader(self.iScriptEttId):
	# 			EntityList.extend(ssTeamObj.getEttList([self.iScriptEttId]))
	# 	return EntityList

	def getTeamEttId(self):
		'''获取有的实体ID列表，包括自身
		'''
		ssTeamObj = self.getTeamObj()
		if ssTeamObj and ssTeamObj.isInTeam(self.iScriptEttId):
			return ssTeamObj.getInTeamList()
		return []

	def isTeamMember(self):
		'''是否为队伍队员，不是队长、离线
		'''
		ssTeamObj = self.getTeamObj()
		if ssTeamObj and ssTeamObj.isInTeam(self.iScriptEttId):
			if not ssTeamObj.isLeader(self.iScriptEttId):
				return True
		return False


#=======================================================
#=======================================================
import entity

gdEntityModMap = {
	entity.ETT_TYPE_DOOR: cEntityDoor,	#传送门
	entity.ETT_TYPE_NPC: cEntityNpc,	#NPC
	entity.ETT_TYPE_ROLE: cEntityRole,	#角色
}

#生成实体实例
def new(iScriptEttId, iEttType, sBaseSerialized):
	mod = gdEntityModMap.get(iEttType, None)
	if not mod:
		raise Exception,"场景服创建实体出错：不支持{}类型".format(iEttType)
	obj = mod(iScriptEttId, iEttType, sBaseSerialized)
	gEntityKeeper.addObj(obj,iScriptEttId) #实体的生命期由scene管理
	return obj

def getEttByScriptId(iScriptEttId):
	return gEntityKeeper.getObj(iScriptEttId)

def getEttByEngineId(iEngineEttId):
	return gEnginerEntityProxy.getProxy(iEngineEttId)
	
import endPoint
import sceneService
import sceneService.team4ss
import sceneService.scene4ss
import zfmPyEx
import scene_pb2

