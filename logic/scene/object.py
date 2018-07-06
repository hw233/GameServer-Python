# -*- coding: utf-8 -*-
import u

if 'gbOnce' not in globals():
	gbOnce = True

class Scene(object):
	'''场景基类
	'''
	
	def __init__(self, _id):
		self.iUid = _id
		self.name = "未知地图"
		self.res = 0  # 地图资源
		self.miniRes = 0  # 小地图资源
		
		self.dEttByType = {}  # 用实体的类型分类存放obj的id
		self.dEttById = {}  # 实体id映射obj
		self.iWidth = self.iHeight = 0  # 场景可行走区域的宽与高
		self.eEttRemove = u.cEvent()
		
		self.eventOnLeave = u.cEvent() # 离开场景事件
		self.eventOnEnter = u.cEvent() # 进入场景事件
		self.denyTeam = "" # 禁止组队
		self.denyTransfer = "" # 禁止传送
		self.broadcastRole = 0

	def onBorn(self, name, res, miniRes, **kwargs):
		self.name = name
		self.res = res
		self.miniRes = miniRes
		if kwargs.get("broadcastRole"):
			self.broadcastRole = kwargs["broadcastRole"]

	
	def this(self):
		return self

	@property
	def id(self):
		return self.iUid

	@property
	def kind(self):
		return SCENE_TYPE_NONE
	
	def getEntityIdsByType(self, iEttType):  # 获得某一类的实体全部id
		for iUid in self.dEttByType.get(iEttType, set()):
			yield iUid

	def removeEntityByType(self, iEttType):  # 仅仅是从场景上移除此实体.
		if iEttType not in self.dEttByType:
			return

		backEnd.gSceneEp4ms.rpcRemoveEntityByType(self.id, iEttType)#通知场景服
		s = self.dEttByType[iEttType]
		for iUid in set(s):
			oEtt = entity.gEntityProxy.getProxy(iUid)
			if oEtt:
				self.removeEntity(oEtt, notifyss=False)
		self.dEttByType.pop(iEttType, None)
	
	def onEnter(self, who, oldScene):
		'''进入场景时
		'''
		import team.platform
		if self.denyTeam: # 如果禁止组队,取消自动匹配
			team.platform.setPlayerAutoMatch(who, 0)
		self.eventOnEnter(who, oldScene, self)
	
	def onLeave(self, who, newScene):
		'''离开场景时
		'''
		self.eventOnLeave(who, self, newScene)

	def isFightScene(self):  # 是否是战斗区
		return False

	def isTempScene(self):  # 是否是临时场景(动态创建的,用完就删的场景叫临时场景.比如副本场景,活动场景)
		return False

	def addEntity(self, oEtt, x, y, d=0, sSerialized=None):  # x,y为None时表示oEtt的x,y已经是正确的了
		iEttId = oEtt.id
		if iEttId in self.dEttById:  # 实体已经在场景里
			# return
			raise Exception,'场景{},有个实体{}重复加入'.format(self.name, iEttId)
		# if x is not None:
		# 	if x<0:
		# 		x=0
		# 	elif x>=self.iWidth:
		# 		x=self.iWidth-1
		# 	oEtt.x = x
		# if y is not None:
		# 	if y<0:
		# 		y=0
		# 	elif y>=self.iHeight:
		# 		y=self.iHeight-1
		# 	oEtt.y = y
		
		#不在这里赋值
		# oEtt.sceneId = self.id
		# oEtt.x = x
		# oEtt.y = y
		# oEtt.d = d
		
		if oEtt.ettType() != entity.ETT_TYPE_ROLE:
			oEtt.setHolderScene(self)
			
		iEttType = oEtt.ettType()
		# itPacket1 = oEtt.getSerializedGroup()
		lIds = self.dEttById.keys()
		if iEttType == entity.ETT_TYPE_ROLE:#角色不会马上发
			if not oEtt.endPoint:	#断线了
				scene.m2ssSwitchScene(self.id, iEttId, oEtt.x, oEtt.y)
		else:
			scene.m2ssSwitchScene(self.id, iEttId, oEtt.x, oEtt.y)
		 
		# random.shuffle(lIds)
		# if lIds:
		# 	iRandIdx = random.randint(0, len(lIds) - 1)
		# 	lTempIds = lIds[iRandIdx:] + lIds[:iRandIdx]
		# else:
		# 	lTempIds = lIds
		# for iUId in lTempIds:  # 每次都是随机顺序的
		# 	oOther = self.dEttById.get(iUId)
		# 	if not oOther:
		# 		continue
		# 	iOtherType = oOther.ettType()
		# 	if iOtherType == entity.ETT_TYPE_ROLE:  # 被动方是玩家
		# 		if iEttType == entity.ETT_TYPE_ROLE:  # 主动方是玩家
		# 			if len(oOther.lSeeOther) < SEE_AMOUNT:
		# 				oEtt.lSeeMe.append(iUId)
		# 				oOther.lSeeOther.append(iEttId)
		# 				oOther.onEntityEnter(oEtt, itPacket1)

		# 			if len(oEtt.lSeeOther) < SEE_AMOUNT:
		# 				oEtt.lSeeOther.append(iUId)
		# 				oOther.lSeeMe.append(iEttId)
		# 				itPacket2 = oOther.getSerializedGroup()
		# 				oEtt.onEntityEnter(oOther, itPacket2)

		# 		else:  # 主动方非玩家
		# 			oOther.onEntityEnter(oEtt, itPacket1)
		# 	else:  # 被动方非玩家
		# 		if iEttType == entity.ETT_TYPE_ROLE:  # 主动方是玩家
		# 			itPacket2 = oOther.getSerializedGroup()
		# 			oEtt.onEntityEnter(oOther, itPacket2)
		# 		else:  # 主动方非玩家
		# 			pass
		
		if oEtt.ettType() == entity.ETT_TYPE_ROLE:
			# self.dEttById[iEttId]=oEtt 其实用这句就可以,但是为了捕捉对象的析构,改成下面这句
			self.dEttById[iEttId] = weakref.proxy(oEtt.this(), u.cFunctor(self.__roleDeleter, iEttId))
		else:
			self.dEttById[iEttId] = oEtt
		self.dEttByType.setdefault(iEttType, set()).add(iEttId)
		
	def __roleDeleter(self, oProxy, iRoleId):
		if iRoleId not in self.dEttById:
			return
		if id(oProxy) != id(self.dEttById.get(iRoleId)):  # 用id来判断是不是同一个proxy,避免异常 ReferenceError: weakly-referenced object no longer exists
			return
		try:
			raise Exception, '场景{},有个玩家{}未能正确踢出场景'.format(self.name, iRoleId)
		except Exception:
			logException()
		writeLog('error', '场景{},有个玩家{}未能正确踢出场景'.format(self.name, iRoleId))		
		self.dEttById.pop(iRoleId, None)
		if entity.ETT_TYPE_ROLE in self.dEttByType:
			self.dEttByType[entity.ETT_TYPE_ROLE].discard(iRoleId)
	



	# 根据ID拿到实体
	def getEntityById(self, iId):
		return  self.dEttById.get(iId)

	def removeEntity(self, oEtt, oAttacker=None, notifyss=True):  # 从场景上移除ett
		iEttId, iEttType = oEtt.id, oEtt.ettType()
		if iEttType == entity.ETT_TYPE_ROLE:  # 被移除的是玩家,只发给关注自己的玩家就行了
			for iUid in oEtt.lSeeMe:
				oOther = self.getEntityById(iUid)
				if oOther:
					if iEttId in oOther.lSeeOther:
						oOther.lSeeOther.remove(iEttId)
					# oOther.onEntityLeave(oEtt)
			for iUid in oEtt.lSeeOther:
				oOther = self.getEntityById(iUid)
				if oOther:
					if iEttId in oOther.lSeeMe:
						oOther.lSeeMe.remove(iEttId)
			oEtt.lSeeMe = []  # 没人可以再看到我了
			oEtt.lSeeOther = []  # 我也看不到其他人了
		else:  # 被移除的不是玩家,需要发给全部玩家
			for iUid, oOther in self.dEttById.items():
				if iUid == iEttId or oOther.ettType() != entity.ETT_TYPE_ROLE:  # 跳过自己
					continue
				# oOther.onEntityLeave(oEtt)
		
		oEtt = self.dEttById.pop(iEttId, None)  # pop出来的是强引用,覆盖掉oEtt这个proxy,避免下面的oEtt是no longer exist
		if iEttType in self.dEttByType:
			self.dEttByType[iEttType].discard(iEttId)
		if oEtt:
			self.eEttRemove(oEtt, oAttacker)

		if oEtt and notifyss:#通知场景服
			backEnd.gSceneEp4ms.rpcRemoveEntity(self.id, oEtt.id)	#通知场景服

	def removeAllEntity(self):  # 移除掉全部场景实体
		backEnd.gSceneEp4ms.rpcRemoveAllEntity(self.id)#通知场景服
		for iEttId, oEtt in self.dEttById.items():
			self.removeEntity(oEtt, notifyss=False)

	# def sendAroundEtt(self,who):#把周围ett的信息发给who(重新登录时会有这个需求)
	# 	iRoleId=who.id
	# 	bFightScene=self.isFightScene()

	# 	for iUId,oOther in self.dEttById.iteritems():
	# 		if iUId!=iRoleId:#跳过自己
	# 			itPacket=oOther.getSerializedGroup()
	# 			who.onEntityEnter(oOther,itPacket)

	def broadcastByXY(self, x, y, sPacket, uIgnoreId=()):  # 根据座标进行场景广播
		# for iUid, oOther in self.dEttById.iteritems():  # 暂时全广播,待优化
		# 	if oOther.ettType() != entity.ETT_TYPE_ROLE:
		# 		continue
		# 	if uIgnoreId and oOther.id in uIgnoreId:
		# 		continue
		# 	oOther.send(sPacket)
		msg = {
			"iSceneId":self.id,
			"x":x,
			"y":y,
			"sPacket":sPacket,
			"uIgnoreId":list(uIgnoreId),
		}
		backEnd.gSceneEp4ms.rpcBroadcastByXY(**msg)	#通知场景服
				
	def height(self):
		return self.iHeight

	def width(self):
		return self.iWidth

	def getRoleIds(self):
		pass

	# def roleMove(self, who, reqMsg):  # 转发角色移动信息
	# 	sPacket = endPoint.makePacket('rpcEttMove', reqMsg)
	# 	for iUid in who.lSeeMe:  # 只发给看得见我的人
	# 		ep = mainService.getEndPointByRoleId(iUid)
	# 		if ep:
	# 			ep.send(sPacket)
				
	def randSpace(self):
		'''随机坐标
		'''
		raise NotImplementedError("还没有实现")
	
	def release(self):
		'''释放场景
		'''
		self.clearRole()
		
	def getRoleList(self):
		'''获取玩家列表
		'''
		st = self.dEttByType.get(entity.ETT_TYPE_ROLE)
		if st:
			return list(st)
		return []
	
	def clearRole(self):
		'''清除玩家
		'''
		roleIdList = self.dEttByType.get(entity.ETT_TYPE_ROLE, set())
		for roleId in list(roleIdList):
			who = getRole(roleId)
			if not who:
				continue
			teamObj = who.inTeam()
			if teamObj and not teamObj.isLeader(roleId):
				continue
			scene.doTransfer(who, *who.getLastRealPos())

			
class RealScene(Scene):
	'''实场景
	'''

	def music(self):  # 背景音乐
		return self.getConfig('music', '')

	@property
	def kind(self):  # 场景类型
		return SCENE_TYPE_REAL

	def landingPoint(self):  # 场景着陆点(通过世界地图传送时会用到)
		return self.getConfig('着陆点x', 100), self.getConfig('着陆点y', 100)

	def anim(self):  # 场景特效动画(落叶、飘雪等)
		return self.getConfig('anim', 0)

	def maskAlpha(self):
		return self.getConfig('alpha', 0)
	
	def backgroundMusic(self):
		return self.getConfig('music', 0)
	
	def getConfig(self, sKey, uDefault=0):
		return sceneData.getConfig(self.id, sKey, uDefault)


class VirtualScene(Scene):
	'''虚拟场景
	'''
	
	def __init__(self, _id):
		Scene.__init__(self, _id)
		self.landX = 0 # 默认登陆x坐标
		self.landY = 0 # 默认登陆y坐标
	
	def onBorn(self, name, res, miniRes, **kwargs):
		Scene.onBorn(self, name, res, miniRes, **kwargs)
		if kwargs.get("landX"):
			self.landX = kwargs["landX"]
			self.landY = kwargs["landY"]
	
	def isTempScene(self):
		return True
	
	def landingPoint(self):
		return self.landX, self.landY


from common import *
from scene.defines import *
import weakref
import gevent
import scene
import sceneData
import mainService
import endPoint
import entity
import backEnd