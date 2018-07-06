# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import u
import c
import keeper
import gevent.local

def _newVirtualSceneId():
	'''生成虚拟场景的id
	存盘的请使用 genVirtualSceneId
	'''
	global gVirtualSceneId
	gVirtualSceneId = u.guIdWithPostfix(0, gVirtualSceneId, True)
	return gVirtualSceneId

def new(_type, _id, name, res, miniRes, **kwargs):
	if _type not in gdSceneModule:
		raise Exception, "不存在类型为{}的场景".format(_type)
	
	if not _id:
		_id = _newVirtualSceneId()

	cls = gdSceneModule[_type]
	sceneObj = cls(_id)
	sceneObj.onBorn(name, res, miniRes, **kwargs)
	gSceneProxy.addObj(sceneObj, sceneObj.id)
	m2ssCreateScene(sceneObj)
	return sceneObj

def getScene(_id):
	return gSceneProxy.getProxy(_id)

def initScene():  # 启服时初始化永久场景
	scene.mapdata.loadMapData()
	
	# 初始化永久场景
	for iNo, dInfo in sceneData.gdData.iteritems():
		_type = dInfo.get("类型", "默认")
		name = dInfo["场景名"]
		res = dInfo.get("资源名", 0)
		miniRes = dInfo.get("小地图资源名", 0)
		
		sceneObj = new(_type, iNo, name, res, miniRes)
		gRealSceneKeeper.addObj(sceneObj, sceneObj.id)  # 永久场景的生命期是全局管理的

		#backEnd.gSceneEp4ms.rpcCreateScene(sceneObj.id)

def m2ssCreateScene(sceneObj):
	'''通知场景服创建场景
	'''
	if 'mainService' not in SYS_ARGV:	#主服才发
		return

	iSceneId = sceneObj.id
	#注册通知场景服删除协议
	u.regDestructor(sceneObj, lambda:backEnd.gSceneEp4ms.rpcRemoveScene(iSceneId))
	msg = {}
	msg["iSceneId"] = sceneObj.id
	iWidth,iHeight = scene.mapdata.gMapWidthHeight.get(sceneObj.res, (0, 0))
	msg["iWidth"] = iWidth
	msg["iHeight"] = iHeight
	msg["iRes"] = sceneObj.res
	msg["iBroadcastRole"] = getattr(sceneObj, "broadcastRole", 0)
	backEnd.gSceneEp4ms.rpcCreateScene(**msg)

def m2ssCrateEntity(oEtt, reg=True):
	'''通知场景服创建实体
	'''
	iEttId = oEtt.id
	if reg:	#通知场景服删除协议
		u.regDestructor(oEtt, lambda:backEnd.gSceneEp4ms.rpcDeleteEntity(iEttId))
	msg = {
		"iEttId":oEtt.id,
		"iEttType":oEtt.ettType(),
		"sBaseSerialized":oEtt.getEttBaseSerialized(),
		"iSceneId":oEtt.sceneId,
		"x":oEtt.x,
		"y":oEtt.y,
	}
	backEnd.gSceneEp4ms.rpcCreateEntity(**msg)

def m2ssModEntityInfo(oEtt, entryInfo, uIgnoreId=()):
	'''修改实体信息
	'''
	msg = {
		"iEttId":oEtt.id,
		"sBaseSerialized" : oEtt.getEttBaseSerialized(),
		"sChangePacket" : endPoint.makePacket('rpcEttChange', entryInfo),
		"uIgnoreId" : list(uIgnoreId),
	}
	backEnd.gSceneEp4ms.rpcModEntityInfo(**msg)

def m2ssSendToClient(roleId, serialized):
	'''通过场景服发包给客户端
	'''
	msg ={
		"roleId":roleId,
		"sSerialized":serialized,
	}
	backEnd.gSceneEp4ms.rpcSendToClient(**msg)

def m2ssSwitchScene(iSceneId, iEttId, x, y):
	'''通知场景服加入实体
	'''
	msg = {}
	msg["iSceneId"] = iSceneId
	msg["x"] = x
	msg["y"] = y
	msg["iEttId"] = iEttId
	# if sSerialized:
	# 	msg["sSwitchSerialized"] = sSerialized
	backEnd.gSceneEp4ms.rpcSwitchScene(**msg)

# 实体特效:  实体ID, 特效类型,	扩展值(如爆炸伤害等), 需要通知的玩家
def updateEntityEffect(iEttId, iEffectType, lNoticeRoleIds=[], iExtendPar=0):
	if not lNoticeRoleIds:
		return
	lEntityEffect = scene_pb2.entityEffect()
	ettEfftInfo = lEntityEffect.effectStatus.add()
	ettEfftInfo.iEttId = iEttId
	ettEfftInfo.iEffect = iEffectType
	ettEfftInfo.iExtendVaule = iExtendPar
	sPacket = endPoint.makePacket('rpcEntityEfft', lEntityEffect)
	for iRoleId in lNoticeRoleIds:
		ep = mainService.getEndPointByRoleId(iRoleId)
		if ep: ep.send(sPacket)

def makeSwitchSceneSerialized(iSceneId, x, y):
	oScene = gSceneProxy.getProxy(iSceneId)
	if not oScene:
		raise Exception, '场景对象不存在'
	switchSceneMsg = scene_pb2.switchScene()	
	switchSceneMsg.iSceneId = iSceneId
	switchSceneMsg.iSceneNo = iSceneId
	switchSceneMsg.iMapRes = oScene.res
	# switchSceneMsg.sMusic=oScene.music()
	switchSceneMsg.sSceneName = oScene.name
	switchSceneMsg.x = x
	switchSceneMsg.y = y

	return endPoint.makePacket('rpcSwitchScene', switchSceneMsg)
	#return switchSceneMsg

def broadcastByAvatar(who, sMethodName, oMsg, uIgnoreId=()):
	'''根据玩家所在位置对场景周围玩家广播
	'''
	oScene = gSceneProxy.getProxy(who.sceneId)
	if not oScene:
		raise Exception, '玩家的场景id对应的场景找不到'
	sPacket = endPoint.makePacket(sMethodName, oMsg)
	oScene.broadcastByXY(who.x, who.y, sPacket, uIgnoreId)

def broadcastByXY(iSceneId, x, y, sMethodName, oMsg, uIgnoreId=()): 
	'''根据位置对场景周围玩家广播
	'''
	oScene = gSceneProxy.getProxy(iSceneId)
	if not oScene:
		raise Exception, '场景id{}对应的场景找不到'.format(iSceneId)
	sPacket = endPoint.makePacket(sMethodName, oMsg)
	oScene.broadcastByXY(x, y, sPacket, uIgnoreId)

def tryTransfer(who, sceneId, x=0, y=0):
	'''尝试传送
	'''
	if isinstance(who, (int, long)):
		roleId = who
		who = getRole(roleId)
		if not who:
			return False
		
	if who.inTeam() and not who.getTeamObj().isLeader(who.id):
		message.tips(who,"组队状态下不能传送")
		return False
	if not validTransfer(who):
		return False

	doTransfer(who, sceneId, x , y)
	return True

def doTransfer(who, sceneId, x=0, y=0):
	'''传送
	'''
	newScene = gSceneProxy.getProxy(sceneId)
	if not newScene:
		raise Exception, 'id为{}的场景对象不存在'.format(sceneId)
	
	if x is None or y is None: # 默认着陆点
		x, y = newScene.landingPoint()
	elif x == 0 or y == 0: # 随机坐标
		x, y = randSpace(sceneId)
	elif x < 0 or y < 0: # 随机坐标
		x, y = randSpace(sceneId)
	
	roleList = []
	teamObj = who.inTeam()
	if teamObj:
		if teamObj.isLeader(who.id):
			for roleId in teamObj.getInTeamList():
				roleObj = getRole(roleId)
				if not roleObj:
					continue
				roleList.append(roleObj)
	else:
		roleList.append(who)

	switchSceneSerialized = makeSwitchSceneSerialized(sceneId, x, y)
	for roleObj in roleList:
		switchScene(roleObj, sceneId, x, y, switchSceneSerialized)

def validTransfer(who):
	'''检查传送
	'''
	oldScene = gSceneProxy.getProxy(who.sceneId)
	if oldScene and oldScene.denyTransfer: # 禁止传送
		message.tips(who, oldScene.denyTransfer)
		return False
	if who.inWar():
		message.tips(who,"战斗中，不可传送")
		return False
	if who.inEscort():
		message.tips(who, "运镖中，不可传送")
		return False
	return True
		
def switchScene(roleObj, sceneId, x, y, switchSceneSerialized=None):
	'''切换场景，一般情况下不要直接调用
	'''
	newScene = gSceneProxy.getProxy(sceneId)
	oldSceneId, oldX, oldY = roleObj.sceneId, roleObj.x, roleObj.y
	
	# 离开旧场景
	oldScene = gSceneProxy.getProxy(oldSceneId)
	if oldScene:
		oldScene.onLeave(roleObj, newScene)
		oldScene.removeEntity(roleObj)
		if not oldScene.isTempScene() :  # 旧场景是永久场景则记录场景编号
			roleObj.active.setLastRealPos(oldSceneId, oldX, oldY)
	
	# 给场景服发包
	if not switchSceneSerialized:
		switchSceneSerialized = makeSwitchSceneSerialized(sceneId, x, y)
	roleObj.sceneId = sceneId  # 不必等待客户端回复,直接将角色位置信息设为切换后的新场景坐标
	roleObj.x = x
	roleObj.y = y
	roleObj.send(switchSceneSerialized)
	
	# 进入新场景
	newScene.addEntity(roleObj, x, y, sSerialized=switchSceneSerialized)
	if oldScene:
		newScene.onEnter(roleObj, oldScene)
		
	# 更新角色的场景id到其他服务器
	role.register.updateRole(roleObj, sceneId=sceneId)
	
# def getRoleGroup(uAny):  # uAny可以是一个玩家对象,或一个玩家id,或一个list/tuple里面的一组玩家id
# 	objList = {}
# 	if isinstance(uAny, (int, long)):  # 是一个id
# 		pid = uAny
# 		obj = getRole(pid)
# 		if obj:
# 			objList[obj.id] = obj
# 	elif isinstance(uAny, (list, tuple)):
# 		for u in uAny:
# 			if isinstance(u, (int, long)):  # u是iRoleId
# 				pid = uAny
# 				obj = getRole(pid)
# 				if obj:
# 					objList[pid] = obj
# 			else:  # 是玩家对象
# 				obj = uAny
# 				objList[obj.id] = obj
# 	else:
# 		obj = uAny
# 		objList[obj.id] = obj
# 	
# 	for obj in objList.values():  # 如果组队，队长带着队员飞 :)
# 		teamObj = obj.getTeamObj()
# 		if not teamObj:
# 			continue
# 		if not teamObj.isLeader(obj.id):
# 			continue
# 		for pid in teamObj.getInTeamList():
# 			if pid in objList:
# 				continue
# 			objMember = getRole(pid)
# 			if not objMember:
# 				continue
# 			objList[objMember.id] = objMember
# 					
# 	return objList.itervalues()
	
# def switchScene(who, sceneId, x=-1, y=-1, alone=False):  # 切换到新场景
# 	if isinstance(who, (int, long)):
# 		roleId = who
# 		who = getRole(roleId)
# 		if not who:
# 			return
# 				
# 	newScene = gSceneProxy.getProxy(sceneId)
# 	if not newScene:
# 		raise Exception, 'id为{}的场景对象不存在'.format(sceneId)
# 	
# 	if x < 0 or y < 0: # 随机坐标
# 		x, y = randSpace(sceneId)
# 	elif x == 0 or y == 0:  # 默认着陆点
# 		x, y = newScene.landingPoint()
# 	
# 	switchSceneSerialized = makeSwitchSceneSerialized(sceneId, x, y)
# 	dJobs = {}
# 
# 	if alone: # 单独
# 		roleList = [who,]
# 	else:
# 		roleList = getRoleGroup(who)
# 	
# 	for roleObj in roleList:
# 		oldSceneId, oldX, oldY = roleObj.sceneId, roleObj.x, roleObj.y
# 		oldScene = gSceneProxy.getProxy(oldSceneId)
# 		if oldScene:
# 			oldScene.onLeave(roleObj, newScene)
# 			oldScene.removeEntity(roleObj)  # 先从旧场景出来
# 			if not oldScene.isTempScene() :  # 旧场景是永久场景则记录场景编号
# 				roleObj.active.setLastRealPos(oldSceneId, oldX, oldY)
# 
# 		roleObj.sceneId = sceneId  # 不必等待客户端回复,直接将角色位置信息设为切换后的新场景坐标
# 		roleObj.x = x
# 		roleObj.y = y
# 		# ep.cancelPendingByRPCname('rpcSwitchScene')
# 		# job=gevent.spawn(ep.rpcSwitchScene,switchSceneMsg)
# 		# who.endPoint.rpcSwitchScene(switchSceneMsg)
# 		roleObj.send(switchSceneSerialized)
# 		# dJobs[iRoleId]=job
# 	# gevent.joinall(dJobs.values())
# 	# lRoleId=[]
# 	# for iRoleId,job in dJobs.iteritems():
# 	# 	if isinstance(job.value,tuple) and not job.value[0]:#有返回
# 	# 		lRoleId.append(iRoleId)
# 	# 	else:#超时未返回之类的
# 	# 		pass
# 			# log.log('switchScene','{}切换场景请求没有回复'.format(iRoleId))	
# 
# 	# for who in getRoleGroup(lRoleId):
# # 		iRoleId = who.id
# 		# 场景切换结束
# 		newScene.addEntity(roleObj, x, y, sSerialized=switchSceneSerialized)  # 进入场景,各实体互相发送接收各自的形象信息.
# 		# ep=mainService.getEndPointByRoleId(iRoleId)
# 		# if ep:
# 		# 	ep.rpcSwitchSceneEnd()#切换场景结束	
# 		oldScene = gSceneProxy.getProxy(oldSceneId)
# 		if oldScene:
# 			newScene.onEnter(roleObj, oldScene)
# 		
# 		role.register.updateRole(roleObj, sceneId=sceneId)
# 
# 		# gGreenletLocal.iSceneId=iNewSceneId
# 		# ep=mainService.getEndPointByRoleId(iRoleId)
# 		# if ep:
# 		# 	ep.cancelPendingByRPCname('rpcSwitchScene')
# 		# 	import timeU
# 		# 	fStart=timeU.getStamp()
# 		# 	try:
# 		# 		bFail,uMsg=ep.rpcSwitchScene(switchSceneMsg)#切换场景开始
# 		# 	except gevent.GreenletExit:
# 		# 		log.log('switchScene','rid={},GreenletExit'.format(iRoleId))
# 		# 		raise
# 		# 	who=role.gKeeper.getObj(iRoleId)
# 		# 	if not who:
# 		# 		return
# 		# 	if gGreenletLocal.iSceneId!=who.sceneId:
# 		# 		oaScene=gSceneProxy.getProxy(gGreenletLocal.iSceneId)
# 		# 		obScene=gSceneProxy.getProxy(who.sceneId)
# 		# 		saName=oaScene.name if oaScene else '原准备的场景name'
# 		# 		sbName=obScene.name if obScene else '已经切的场景name'
# 		# 		log.log('switchScene','rid={},{},{},{},msg={},cost={}'.format(iRoleId,saName,sbName,bFail,u.transMsg(uMsg),timeU.getStamp()-fStart))
# 		# 	if bFail:#
# 		# 		continue
# 			# todo:上下文切换了,各种对象可能不存在了.要检查
# 
# 	# for who in getRoleGroup(lRoleId):#切换结束
# 	# 	iRoleId=who.id

def SwitchSceneResponse(iTarget):
	oEndPoint = mainService.gEndPointKeeper.getObj(iTarget)
	if not oEndPoint:
		# raise Exception,"SwitchSceneResponse 找不到EndPoint"
		return
	who = oEndPoint.roleObj
	if not who:
		# raise Exception,"SwitchSceneResponse 找不到角色｜{}".format(oEndPoint.roleId)
		return

	m2ssSwitchScene(who.sceneId, who.id, who.x, who.y)

def switchSceneForNpc(npcObj, sceneId, x, y, d):
	'''npc切换场景
	'''
	sceneObj = getScene(sceneId)
	if not sceneObj:
		raise Exception("npc%s切换场景时找不到场景%s" % (npcObj.name, sceneId))
	
	npcObj.sceneId = sceneObj.id
	npcObj.x = x
	npcObj.y = y
	npcObj.d = d
	#npc不会重复加入场景，所以在加入前先创建实体
	m2ssCrateEntity(npcObj)
	sceneObj.addEntity(npcObj, x, y, d)
	
def switchSceneForDoor(doorObj, sceneId, x, y):
	'''door切换场景
	'''
	sceneObj = getScene(sceneId)
	if not sceneObj:
		raise Exception("door%s切换场景时找不到场景%s" % (doorObj.name, sceneId))
	
	doorObj.sceneId = sceneId
	doorObj.x = x
	doorObj.y = y
	m2ssCrateEntity(doorObj)
	sceneObj.addEntity(doorObj, x, y)
	
def broadcastEttChange(entityObj, attrList):
	'''广播实体属性改变
	'''
	# 清缓存
	entityObj.sSerialized1 = None
	if hasattr(entityObj, "sEnterSerialized"):
		entityObj.sEnterSerialized = None

	entityType = entityObj.ettType()
	if entityType == entity.ETT_TYPE_ROLE: # 玩家
		msgObj = scene_pb2.roleInfo()
	elif entityType == entity.ETT_TYPE_NPC: # npc
		msgObj = scene_pb2.npcInfo()
	elif entityType == entity.ETT_TYPE_DOOR: # 传送门
		msgObj = scene_pb2.doorInfo()
	else:
		raise Exception("广播实体属性改变:错误的实体类型{}".format(entityType))

	# 修改对应类型的消息体
	for attrName, attrVal in attrList.iteritems():
		if isinstance(attrVal, (list, tuple)):
			attrObj = getattr(msgObj, attrName)
			attrObj.extend(attrVal)
		else:
			setattr(msgObj, attrName, attrVal)

	# 发协议到场景服
	changeMsg = scene_pb2.entityChange()
	changeMsg.iEttId = entityObj.id
	changeMsg.iEttType = entityType
	changeMsg.sSerializedEtt = msgObj.SerializeToString()
	m2ssModEntityInfo(entityObj, changeMsg, [entityObj.id])

def m2ssEntityMove(oEtt):
	'''非角色移动
	'''
	msg = {}
	msg["iEttId"] = oEtt.id
	msg["x"]	 = oEtt.x
	msg["y"]	 = oEtt.y
	msg["sceneId"] = oEtt.sceneId
	backEnd.gSceneEp4ms.rpcSSEntityMove(**msg)

def getSurroundPlayer(who):
	oScene = gSceneProxy.getProxy(who.sceneId)
	return oScene.getEntityIdsByType(entity.ETT_TYPE_ROLE)

def isNearBy(objA, objB, distance=10):
	'''是否在身边
	'''
	if isinstance(objA, (list, tuple)):
		sceneIdA, xA, yA = objA
	else:
		sceneIdA, xA, yA = objA.sceneId, objA.x, objA.y
	
	if isinstance(objB, (list, tuple)):
		sceneIdB, xB, yB = objB
	else:
		sceneIdB, xB, yB = objB.sceneId, objB.x, objB.y
	
	if sceneIdA != sceneIdB:
		return 0
	return pow(xA - xB, 2) + pow(yA - yB, 2) <= pow(distance, 2)

def getSceneResId(sceneId):
	'''获取地图的资源id
	'''
	sceneObj = getScene(sceneId)
	return sceneObj.res

def randSpace(sceneId):
	'''怪物随机坐标，以固定NPC所在点为中心，正负3个坐标点内，不会刷新出
	'''
	if sceneId in gSceneRandMapData:
		posList = gSceneRandMapData[sceneId].keys()
		if not posList:
			raise Exception,"没有{}场景资源的随机坐标".format(sceneId)
		return posList[rand(len(posList))]
	return randSpaceEx(sceneId)
	# raise Exception("不存在此场景资源的随机坐标")

def randSpaceEx(sceneId):
	'''随机坐标,不会排除坐标
	'''
	resId = getSceneResId(sceneId)
	mapDataList = scene.mapdata.gRandMapDataList
	if resId in mapDataList:
		posList = mapDataList[resId].keys()
		return posList[rand(len(posList))]
	
	raise Exception("不存在此场景资源的随机坐标")

def validPos(sceneId, x, y):
	'''检查坐标是否合法
	'''
	resId = getSceneResId(sceneId)
	mapDataList = scene.mapdata.gValidMapDataList
	if resId in mapDataList:
		return (x, y) in mapDataList[resId]
	return 0

def getFixPos(sceneId, x, y):
	'''修正坐标
	'''
	resId = getSceneResId(sceneId)
	mapDataList = scene.mapdata.gValidMapDataList
	if resId in mapDataList:
		posList = mapDataList[resId].keys()
		if (x, y) not in posList:
			for x2, y2 in createNearbyPosList(x, y):
				if (x2, y2) in mapDataList:
					return x2, y2

	return randSpace(sceneId)

def createNearbyPosList(x, y, distance=5):
	'''创建附近坐标列表
	'''
	funcList = (
		lambda i:(x, y + i),
		lambda i:(x, y - i),
		lambda i:(x + i, y),
		lambda i:(x + i, y + i),
		lambda i:(x + i, y - i),
		lambda i:(x - i, y),
		lambda i:(x - i, y + i),
		lambda i:(x - i, y - i),
	)
	
	funcList = shuffleList(funcList)
	for i in xrange(1, distance + 1):
		for func in funcList:
			yield func(i)

def walkGuard(who, sceneId):
	'''巡逻
	'''
	if not validTransfer(who):
		return
	if who.sceneId != sceneId:
		if not tryTransfer(who, sceneId):
			return
	msg = scene_pb2.walkGuardInfo()
	msg.sceneId = sceneId
	who.endPoint.rpcRoleWalkGuard(sceneId)
	
def walkToPos(who, sceneId, x, y, responseFunc=None):
	'''寻路到指定坐标
	'''
	bSwitchScene = False
	if who.sceneId != sceneId:  # 不在目标场景，先传送过去
		if not validTransfer(who):
			return
		if not tryTransfer(who, sceneId, None, None):
			return
		bSwitchScene = True
	qanda.service.rpcWalkToPosRequest(who, sceneId, x, y, responseFunc)

def walkToEtt(who, ettObj):
	'''寻路到指定实体
	'''
	if who.sceneId != ettObj.sceneId:  # 不在目标场景，先传送过去
		if not validTransfer(who):
			return
		if not tryTransfer(who, ettObj.sceneId, None, None):
			return
	who.endPoint.rpcWalkToEtt(ettObj.id,ettObj.x,ettObj.y,ettObj.sceneId)
	
def playEttEffect(who, effectNo, ettId):
	'''播放实体特效
	'''
	who.endPoint.rpcEttEffect(effectNo, ettId)
	
def playSceneEffect(who, effectNo, sceneId, x=0, y=0):
	'''播放场景特效
	'''
	if x == 0 or y == 0:
		x = who.x
		y = who.y
	who.endPoint.rpcScreenEffect(effectNo, sceneId, x, y)

def addFollow(who, followInfo):
	'''增加跟随
	'''
	who.endPoint.rpcAddFollower(followInfo)

def delFollow(who, followNo):
	'''删除跟随
	'''
	who.endPoint.rpcDelFollower(followNo)

def broadcastEttEffect(effectNo, ettId):
	'''广播播放实体特效
	'''
	oEtt = entity.gEntityProxy.getProxy(ettId)
	if not oEtt:
		return
	msg = scene_pb2.effectMsg()
	msg.effectNo = effectNo
	msg.ettId = ettId
	broadcastByXY(oEtt.sceneId, oEtt.x, oEtt.y, "rpcEttEffect", msg)
	
def broadcastSceneEffect(effectNo, sceneId, x, y):
	'''广播播放场景特效
	'''
	msg = scene_pb2.effectMsg()
	msg.effectNo = effectNo
	msg.sceneId = sceneId
	msg.x = x
	msg.y = y
	broadcastByXY(sceneId, x, y, "rpcScreenffect", msg)
	
def findPath(sceneId, srcX, srcY, destX, destY):
	mapDataList = scene.mapdata.gMapDataList
	
	resId = getSceneResId(sceneId)
	mapData = mapDataList[resId]
	
	srcJump, destJump = scene.mapdata.getJumps(resId, srcX, srcY, destX, destY)
	if not srcJump or not destJump:
		writeLog("scene/jumps", "not found jumps: sceneId %d (%d,%d) to (%d,%d)" % (sceneId, srcX, srcY, destX, destY))
		return None

	if srcJump != (srcX, srcY) or destJump != (destX, destY):  # 需要跳跃
		srcJumpX, srcJumpY = srcJump
		destJumpX, destJumpY = destJump
		srcPosList = scene.walkpath.findPath(mapData, srcX - 1, srcY - 1, srcJumpX - 1, srcJumpY - 1) # 从原坐标到原区跳跃点
		destPosList = scene.walkpath.findPath(mapData, destJumpX - 1, destJumpY - 1, destX - 1, destY - 1) # 从目的区跳跃点到目的坐标
		posList = destPosList + srcPosList
# 		print "found jumps %s %s: sceneId %d (%d,%d) to (%d,%d)" % (srcJump, destJump, sceneId, srcX, srcY, destX, destY)
	else:
		posList = scene.walkpath.findPath(mapData, srcX - 1, srcY - 1, destX - 1, destY - 1)
		if not posList:
# 			print scene.validPos(sceneId, srcX, srcY), scene.validPos(sceneId, destX, destY), "not found path: sceneId %d (%d,%d) to (%d,%d)" % (sceneId, srcX, srcY, destX, destY)
			writeLog("scene/path", "not found path: sceneId %d (%d,%d) to (%d,%d)" % (sceneId, srcX, srcY, destX, destY))
			return None
		
	# 　转成以1开始的坐标
	for idx, (x, y) in enumerate(posList):
		posList[idx] = [x + 1, y + 1]

	return posList

def isJump(sceneId, x, y):
	'''该坐标是否是跳跃点
	'''
	resId = getSceneResId(sceneId)
	jumpDataList = scene.mapdata.gJumpDataList
	if resId not in jumpDataList: # 此场景没有跳跃点
		return 0

	xy = (x, y)
	return xy in jumpDataList[resId]

from common import *
import config
import sceneData
import scene_pb2
import endPoint
import role
import mainService
import log
import timeU
import scene.object
import scene.scenehd
import scene.sceneguild
import scene.mapdata
import role.register
import qanda
import backEnd
import scene.walkpath
import main_scene_pb2
import message
import entity

def init():
	print "init scene"
	global gVirtualSceneId, gSaveVirtualSceneId
	global gRealSceneKeeper, gSceneProxy, gGreenletLocal, gdSceneModule
	global gbInitScene
	gVirtualSceneId = u.guIdWithPostfix(0, 200, False) # 不需要存盘的虚拟场景开始编号, 如2XX01
	gSaveVirtualSceneId = u.guIdWithPostfix(config.ZONE_NO, 200, False) # 需要存盘的虚拟场景开始编号, 如2XX+区号
	gRealSceneKeeper = keeper.cKeeper()  # 永久场景实例存放处,临时场景的实例不在这里
	gSceneProxy = u.cKeyMapProxy()  # 永久场景与临时场景都可以在这里查找
	gGreenletLocal = gevent.local.local()

	# 场景类
	gdSceneModule = {
		"默认": scene.object.RealScene,  # 默认实场景
		"活动": scene.scenehd.Scene,  # 活动场景
		"仙盟": scene.sceneguild.Scene,  # 帮派场景
	}
	
	initScene()
	gbInitScene = True

	initSceneRandMapData()


if "gSceneRandMapData" not in globals():
	gSceneRandMapData = {} #场景可以生成随机坐标的数据

def initSceneRandMapData():
	'''可以生成随机坐标的数据,排除以固定NPC所在点为中心，正负3个坐标点内
		场景资源相同，但每个场景的固定NPC不一样
	'''
	import npc
	import copy
	npc.initSceneNpcPos()
	
	mapDataList = scene.mapdata.gRandMapDataList
	global gSceneRandMapData
	gSceneRandMapData = {}
	for sceneId, dInfo in sceneData.gdData.iteritems():
		resId = dInfo.get("资源名", 0)
		if resId not in mapDataList:
			continue
		sceneMapData = {}
		for pos, val in mapDataList[resId].items():
			x, y = pos
			if npc.inSceneNpcAround(sceneId, x, y):
				continue
			sceneMapData[pos] = val
		gSceneRandMapData[sceneId] = sceneMapData

#=========================================
#单独重启场景服时恢复场景服数据

if 'gbInitScene' not in globals():
	gbInitScene = False

def recoverySceneService():
	if not gbInitScene:
		return

	log.log("scene/recovery", "recovery start")
	#恢复场景
	for _,sceneObj in gSceneProxy.getAll().iteritems():
		m2ssCreateScene(sceneObj)
		#恢复实体
		for iEttId, oEtt in sceneObj.dEttById.iteritems():
			if oEtt.ettType() == entity.ETT_TYPE_ROLE:
				if oEtt.endPoint:#没断线才恢复
					role.register.registerRoleToScene(oEtt)#进入场景前先注册角色到场景服务器
					m2ssCrateEntity(oEtt, reg=False)
			else:
				m2ssCrateEntity(oEtt)
			m2ssSwitchScene(sceneObj.id, oEtt.id, oEtt.x, oEtt.y)

	#恢复队伍
	import team
	import team.service
	for teamObj in team.getAllTeam():
		team.service.rpcSSModTeamInfo(teamObj)

	log.log("scene/recovery", "recovery end")