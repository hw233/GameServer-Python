#-*-coding:utf-8-*-

#对应C层的aoi类型
AOI_INFO_ENTER = 1		#进入
AOI_INFO_LEAVE = 2		#离开
AOI_INFO_MOVE = 3		#移动
AOI_INFO_DELETT = 4		#删除实体
AOI_INFO_DELSCENE = 5	#删除场景

#aoi方向,从哪发到哪 1或2 -1代表没效,0表示没方向区别
AOI_DIR_NO = 0
AOI_DIR_LEFT = 1 	#iEttId发到ettIds
AOI_DIR_RIGHT = 2	#ettIds发到iEttId

#=========================================
#=========================================
#aoi结构
# class aoi(object):
# 	'''没有自定义函数
# 	'''
# 	def __init__(self):
# 		self.iEttId = 0 #实体ID
# 		self.x = 0 		#实体坐标x
# 		self.y = 0 		#实体坐标y
# 		self.iInfoType = 0#aoi类型，见上面
# 		self.iDir = 0 	#aoi方向，见上面,只有进入、离开、移动有方向
# 		self.ettIds = [] #列表，3个为一组数据，如[实体ID1,坐标x,坐标y,实体ID2,坐标x,坐标y,....]
# 		# iEttId 和 ettIds实体ID 必定为角色，否则底层有问题
#=========================================
#=========================================


def duelAoiEnter(aoinfo):
	'''进入
	'''
	# sceneService.sceneServerLog("aoiInfo", "aoi 进入视野 实体：{} 方向：{} 列表：{}".format(aoinfo.iEttId, aoinfo.iDir, aoinfo.ettIds))
	iEngineEntityId = aoinfo.iEttId
	oEntity = entity4ss.getEttByEngineId(iEngineEntityId)
	if not oEntity:
		return
	iDir = aoinfo.iDir
	iEntityX = aoinfo.x
	iEntityY = aoinfo.y
	iScriptEntityId = oEntity.scriptEttId
	iEttIdCnt = len(aoinfo.ettIds)/3
	sceneObj = oEntity.sceneObj

	sceneService.sceneServerLog("aoiInfo", "aoi 进入视野 实体：{} 方向：{} 数量：{}".format(aoinfo.iEttId, aoinfo.iDir, iEttIdCnt))
	if iDir == AOI_DIR_LEFT:#oEntity进入oOther视野
		if not sceneObj.isBroadcastRole():
			return
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			if not oOther.isRole():
				continue
				# raise Exception,"场景服底层出错，实体不是角色"
			oOther.onEntityEnter(oEntity, iEntityX, iEntityY)

			#为了在组队时通过跳跃点的情况特殊处理
			if oOther.inTeam():
				oOther.onEntityMove(oEntity, iEntityX, iEntityY)

	elif iDir == AOI_DIR_RIGHT:	#oOther进入oEntity视野
		if not oEntity.isRole():
			return
			# raise Exception,"场景服底层出错，实体不是角色"
		#为了在组队时通过跳跃点的情况特殊处理
		bEntityInTeam = oEntity.inTeam()
		iBroadcastRole = sceneObj.isBroadcastRole()
		
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			if oOther.isRole() and not iBroadcastRole:
				continue
			oEntity.onEntityEnter(oOther, iOtherX, iOtherY)
			if bEntityInTeam:
				oEntity.onEntityMove(oOther, iOtherX, iOtherY)

def duelAoiLeave(aoinfo):
	'''离开
	'''
	# sceneService.sceneServerLog("aoiInfo", "aoi 离开视野 实体：{} 方向：{} 列表：{}".format(aoinfo.iEttId, aoinfo.iDir, aoinfo.ettIds))
	iEngineEntityId = aoinfo.iEttId
	oEntity = entity4ss.getEttByEngineId(iEngineEntityId)
	if not oEntity:
		return
	iDir = aoinfo.iDir
	iEntityX = aoinfo.x
	iEntityY = aoinfo.y
	iEttIdCnt = len(aoinfo.ettIds)/3
	sceneObj = oEntity.sceneObj

	sceneService.sceneServerLog("aoiInfo", "aoi 离开视野 实体：{} 方向：{} 数量：{}".format(aoinfo.iEttId, aoinfo.iDir, iEttIdCnt))
	if iDir == AOI_DIR_LEFT:#oEntity离开oOther视野
		# if not sceneObj.isBroadcastRole():
		# 	return
		# lTeamEttId = oEntity.getTeamEttId()#整个队伍的实体ID列表
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			if not oOther.isRole():
				continue
				# raise Exception,"场景服底层出错，实体不是角色"
			# if oOther.iScriptEttId in lTeamEttId:
			# 	continue
			oOther.onEntityLeave(oEntity)

	elif iDir == AOI_DIR_RIGHT:#oOther离开oEntity视野
		if not oEntity.isRole():
			return
			# raise Exception,"场景服底层出错，实体不是角色"
		iBroadcastRole = sceneObj.isBroadcastRole()
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			# lTeamEttId = oOther.getTeamEttId()#整个队伍的实体ID列表
			# if oEntity.iScriptEttId in lTeamEttId:
			# 	continue
			if oOther.isRole() and not iBroadcastRole:
				continue
			oEntity.onEntityLeave(oOther)

def duelAoiMove(aoinfo):
	'''移动
	'''
	# sceneService.sceneServerLog("aoiInfo", "aoi 移动视野 实体：{} 方向：{} 列表：{}".format(aoinfo.iEttId, aoinfo.iDir, aoinfo.ettIds))
	iEngineEntityId = aoinfo.iEttId
	oEntity = entity4ss.getEttByEngineId(iEngineEntityId)
	if not oEntity:
		return
	iDir = aoinfo.iDir
	iEntityX = aoinfo.x
	iEntityY = aoinfo.y
	iEttIdCnt = len(aoinfo.ettIds)/3
	sceneObj = oEntity.sceneObj
	bIsTeamMember = oEntity.isTeamMember()	#是否为队伍队员
	sceneService.sceneServerLog("aoiInfo", "aoi 移动视野 实体：{} 方向：{} 数量：{}".format(aoinfo.iEttId, aoinfo.iDir, iEttIdCnt))

	if iDir == AOI_DIR_LEFT:	#oEntity在oOther视野范围内移动
		if not sceneObj.isBroadcastRole():
			return
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			if not oOther.isRole():
				continue
				# raise Exception,"场景服底层出错，实体不是角色"
			_bIsTeamMember = oOther.isTeamMember()	#是否为队伍队员
			if bIsTeamMember and _bIsTeamMember:	#互相都是队伍队员
				continue
			oOther.onEntityMove(oEntity, iEntityX, iEntityY)

	#移动不会产生AOI_DIR_RIGHT
	elif iDir == AOI_DIR_RIGHT:	#oOther在oEntity视野范围内移动
		if not oEntity.isRole():
			return
			# raise Exception,"场景服底层出错，实体不是角色"
		iBroadcastRole = sceneObj.isBroadcastRole()
		for index in xrange(iEttIdCnt):
			iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
			oOther = entity4ss.getEttByEngineId(iEngineOtherId)
			if not oOther:
				continue
			if oOther.isRole() and not iBroadcastRole:
				continue
			_bIsTeamMember = oOther.isTeamMember()	#是否为队伍队员
			# print oEntity.id,oOther.id,bIsTeamMember,_bIsTeamMember
			if bIsTeamMember and _bIsTeamMember:	#互相都是队伍队员
				continue
			oEntity.onEntityMove(oOther, iOtherX, iOtherY)

def duelAoiDelEtt(aoinfo):
	'''删除实体
	'''
	# sceneService.sceneServerLog("aoiInfo", "aoi 删除实体 实体：{}".format(aoinfo.iEttId))
	iEngineEntityId = aoinfo.iEttId
	oEntity = entity4ss.getEttByEngineId(iEngineEntityId)
	if not oEntity:
		sceneService.sceneServerLog("aoiInfo", "aoi 删除实体,实体不存在.实体id：{}".format(aoinfo.iEttId))
		return
	iScriptEttId = oEntity.scriptEttId
	sceneService.entity4ss.gEntityKeeper.removeObj(iScriptEttId)

def duelAoiDelScene(aoinfo):
	'''删除场景
	'''
	# sceneService.sceneServerLog("aoiInfo", "aoi 删除场景 场景：{}".format(aoinfo.iSceneId))
	iEngineSceneId = aoinfo.iSceneId
	oScene=sceneService.scene4ss.getSceneByEngineId(iEngineSceneId)
	if not oScene:#场景不存在
		sceneService.sceneServerLog("aoiInfo", "aoi 删除场景, 场景不存在 场景id：{}".format(aoinfo.iSceneId))
		return
	iScriptSceneId = oScene.scriptSceneId
	sceneService.scene4ss.gSceneKeeper.removeObj(iScriptSceneId)


if 'gbOnce' not in globals():
	gbOnce=True
	if 'sceneService' in SYS_ARGV:
		gAoiTimerMgr = None
		gdDealAoiFuncMap = {
			AOI_INFO_ENTER:duelAoiEnter,
			AOI_INFO_LEAVE:duelAoiLeave,
			AOI_INFO_MOVE:duelAoiMove,
			AOI_INFO_DELETT:duelAoiDelEtt,
			AOI_INFO_DELSCENE:duelAoiDelScene,
		}

def initTimer():#设置定时器
	global gAoiTimerMgr
	gAoiTimerMgr = timer.cTimerMng()
	gAoiTimerMgr.run(getAoi, 0.1, 0, "getAoi")


def getAoi():
	if gAoiTimerMgr:
		gAoiTimerMgr.run(getAoi, 0.1, 0, "getAoi")
	aoinfo = zfmPyEx.getAOIinfo()
	while aoinfo:
		func = gdDealAoiFuncMap.get(aoinfo.iInfoType, None)
		if not func:
			print "aoi信息没有对应的处理函数：{}".format(aoinfo.iInfoType)
			continue
		func(aoinfo)
		aoinfo = zfmPyEx.getAOIinfo()

#----------------------测试代码开始---------------
def onAoiAsync():
	#asyncWatcher.stop()
	#getAoi() 
	myGreenlet.cGreenlet.spawn(getAoi)#因为这是在hub协程,不能有block的逻辑,但是getAoi发现有block的逻辑

def wakeupAoiAsync():#被另一个线程调用
	global asyncWatcher
	if asyncWatcher:
		asyncWatcher.send()

def initAoiAsyncWatch():
	global asyncWatcher
	asyncWatcher = gevent.get_hub().loop.async()
	asyncWatcher.start(onAoiAsync)#u.cFunctor(onAoiAsync,asyncWatcher)

#----------------------测试代码结束---------------

import gevent
import timer
import entity4ss
import scene4ss
import scene_pb2
import sceneService
import myGreenlet

if 'aoiInit' not in globals():
	aoiInit=True
	if 'sceneService' in SYS_ARGV:
		import zfmPyEx
		zfmPyEx.aoiInit(wakeupAoiAsync)


# for iUId in aoinfo.ettIds:
# 	oOther = entity4ss.getEttByEngineId(iUId)
# 	if not oOther:
# 		continue
# 	iOtherType = oOther.ettType
# 	if iDir == 1:#oEntity进入oOther视野
# 		oOther.onEntityEnter(oEntity)
# 	else:
# 		oEntity.onEntityEnter(oOther)
# return

# if iDir == 1:#oEntity进入oOther视野
# 	#有队伍，要整个队伍进入
# 	EntityList = oEntity.getRelatedEttList()#整个队伍的实体列表
# 	for index in xrange(iEttIdCnt):
# 		iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
# 	# for tEttInfo in aoinfo.ettIds:
# 	# 	iEngineOtherId,iOtherX,iOtherY = tEttInfo
# 		oOther = entity4ss.getEttByEngineId(iEngineOtherId)
# 		if not oOther or not oOther.isRole():
# 			continue
# 		for ettObj in EntityList:
# 			#加入队伍时要先进入队长视野，跳过进入自身视野
# 			if ettObj.scriptEttId == oOther.scriptEttId:	
# 				continue
# 			oOther.onEntityEnter(ettObj, iEntityX, iEntityY)
# else:	#oOther进入oEntity视野
# 	if not oEntity.isRole():
# 		return
# 	# for tEttInfo in aoinfo.ettIds:
# 	# 	iEngineOtherId,iOtherX,iOtherY = tEttInfo
# 	for index in xrange(iEttIdCnt):
# 		iEngineOtherId,iOtherX,iOtherY = aoinfo.ettIds[index*3],aoinfo.ettIds[index*3+1],aoinfo.ettIds[index*3+2]
# 		oOther = entity4ss.getEttByEngineId(iEngineOtherId)
# 		if not oOther:
# 			continue
# 		#有队伍，要整个队伍进入
# 		EntityList = oOther.getRelatedEttList(leader=True)
# 		for ettObj in EntityList:
# 			#加入队伍时要先进入队长视野，跳过进入自身视野
# 			if ettObj.scriptEttId == oEntity.scriptEttId:
# 				continue
# 			oEntity.onEntityEnter(ettObj, iOtherX, iOtherY)

