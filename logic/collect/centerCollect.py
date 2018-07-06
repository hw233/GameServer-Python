#-*-coding:utf-8-*-
'''中心服收集法
'''
# if 'gbOnce' not in globals():
# 	gbOnce=True
# 	giEventUID = 0

# def initEventId():
# 	global giEventUID
# 	rs = db4center.gConnectionPool.query(sql4center.EVENT_MAXID)
# 	for tInfo in rs.rows:
# 		if tInfo[0]:
# 			giEventUID = tInfo[0]
# 		break

# def NextEventUID():
# 	global giEventUID
# 	giEventUID += 1
# 	return giEventUID

giOneKm = 250#1000
giTwoKm = 500#2000


def initCenterStorageScheduler():
	if 'centerService' in SYS_ARGV:
		if 'storageScheduler' not in globals():
			global storageScheduler
			storageScheduler = scheduler.cScheduler()


class cCollectSingleton(object):
	'''
	'''
	def __init__(self):
		self.iLastEventId = 0	#最后生成的事件ID
		self._name = "collectEvent"

	def loadFromDB(self):
		rs = db4center.gConnectionPool.query(sql4center.SINGLETON_SELECT, self._name)
		if len(rs.rows) == 0:
			self.onBorn()
			return
		for tInfo in rs.rows:
			data = ujson.loads(tInfo[0])
			self.load(data)
		
	def onBorn(self, **args):
		self.scheduleInsert()

	def load(self, data):
		self.iLastEventId = data.get("lastEventId", 0)

	def save(self):
		data = {}
		data["lastEventId"] = self.iLastEventId
		return data

	def scheduleSave(self):#数据发生变化,加入到存盘调度队列
		storageScheduler.appendCallLater(self._saveToDB, 'singleton', self._name)

	def _saveToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.SINGLETON_UPDATE, sData, self._name)

	def scheduleInsert(self):#数据发生变化,加入到存盘调度队列
		storageScheduler.appendCallLater(self._insertToDB, 'singleton', self._name)

	def _insertToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.SINGLETON_INSERT, self._name, sData)

	def nextEventId(self):
		'''下一事件ID
		'''
		self.iLastEventId += 1
		self.scheduleSave()
		return self.iLastEventId


class cRoleInfo(object):
	def __init__(self, iRoleId):
		self.iRoleId = iRoleId
		self.lComEvent = []#完成的事件,用于显示,可手动删除
		self.lComEventId = []	#完成的事件ID,用于搜索，不可手动删除
		self.lProEvent = []#生产的事件
		self.lMarkerEvent = []#标记的事件
		self.lTriggerRole = []#被动触发的玩家
		self.iServerId = 0
		self.fPosX = 0
		self.fPosY = 0
		self.sName = ""
		self.sPicture = ""
		self.iSchool = 0
		self.iGender = 0
		self.iLastId = 0	#自用id，用于被动触发列表
		self.lLastSearch = [] #上一次搜索的事件
		self.lSpecialEvent = []

	def getRoleId(self):
		return self.iRoleId

	def scheduleSave(self):#数据发生变化,加入到存盘调度队列
		storageScheduler.appendCallLater(self._saveToDB, 'role_info', self.iRoleId)

	def _saveToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.ROLEINFO_UPDATE, sData, self.iRoleId)

	def scheduleInsert(self):#数据发生变化,加入到存盘调度队列
		storageScheduler.appendCallLater(self._insertToDB, 'role_info', self.iRoleId)

	def _insertToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.ROLEINFO_INSERT, self.iRoleId, sData)

	def onBorn(self, **args):
		self.scheduleInsert()

	def load(self, data):
		self.lComEvent = data.get("comEvent", [])#完成的事件
		self.lComEventId = data.get("comEventId", [])
		self.lProEvent = data.get("proEvent", [])#生产的事件
		self.lMarkerEvent = data.get("markerEvent", [])#标记的事件
		self.lTriggerRole = data.get("tirggerRole", [])
		self.iServerId = data.get("iServerId", 0)
		self.fPosX = data.get("posX", 0)
		self.fPosY = data.get("posY", 0)
		self.sName = data.get("name", "")
		self.iSchool = data.get("school", 11)
		self.sPicture = data.get("picture", "")
		self.iGender = data.get("gender", 0)
		self.iLastId = data.get("lastId", 0)

	def save(self):
		data = {}
		data["comEvent"] = self.lComEvent
		data["comEventId"] = self.lComEventId
		data["proEvent"] = self.lProEvent
		data["markerEvent"] = self.lMarkerEvent
		data["iServerId"] = self.iServerId
		data["posX"] = self.fPosX
		data["posY"] = self.fPosY
		data["tirggerRole"] = self.lTriggerRole
		data["name"] = self.sName
		data["school"] = self.iSchool
		data["picture"] = self.sPicture
		data["gender"] = self.iGender
		data["lastId"] = self.iLastId
		return data

	def packetData(self):
		data = self.save()
		data["iRoleId"] = self.iRoleId
		return data

	def addLastId(self):
		self.iLastId += 1

	def setLastSearch(self, l):
		self.lLastSearch = l

	def getLastSearch(self):
		return self.lLastSearch

	def setSpecialEvent(self, l):
		self.lSpecialEvent = l

	def getSpecialEvent(self):
		return self.lSpecialEvent

	def removeSpecialEvent(self, iEventId):
		if iEventId in self.lSpecialEvent:
			self.lSpecialEvent.remove(iEventId)

	#=====================================================
	#=====================================================
	def updateRoleInfo(self, reqMsg):
		self.iServerId = reqMsg.iServerId
		self.fPosX = float(reqMsg.fPosX)
		self.fPosY = float(reqMsg.fPosY)
		self.sName = reqMsg.sName
		self.iGender = reqMsg.iGender
		self.iSchool = reqMsg.iSchool
		self.scheduleSave()

	def getLocationInfo(self):
		return self.fPosX,self.fPosY

	#=====================================================
	#=====================================================
	def addCompleteEvent(self, fPosX, fPosY, eventObj):
		'''增加完成事件ID
		'''
		tmp = {}
		tmp["iEventId"] = eventObj.iEventId
		tmp["iDistance"] = collect.getLineDistance(fPosX, fPosY, eventObj.fPosX, eventObj.fPosY)
		tmp["iEventNo"] = eventObj.iEventNo
		tmp["iServerId"] = eventObj.iServerId
		tmp["sName"] = eventObj.sName
		tmp["iGender"] = eventObj.iGender
		tmp["sPicture"] = eventObj.sPicture
		tmp["iComTime"] = getSecond()
		tmp["iSchool"] = eventObj.iSchool
		tmp["iRoleId"] = eventObj.iRoleId

		self.lComEvent.insert(0, tmp)
		if len(self.lComEvent) > 100:
			lRemoveEvent = self.lComEvent[100:]
			self.lComEvent = self.lComEvent[:100]
			for info in lRemoveEvent:
				collect.service4main.rpcC2BCollectDelEvent(self.iServerId, self.iRoleId, info.get("iEventId", 0), COMPLETE_EVENT)

		#删除已经消失的事件
		lRemoveId = []
		for iEventId in self.lComEventId:
			if iEventId not in collect.gCenterCollectObj.dEventInfoObj:
				lRemoveId.append(iEventId)
		for iEventId in lRemoveId:
			self.lComEventId.remove(iEventId)
		self.lComEventId.insert(0, eventObj.iEventId)
		# if len(self.lComEventId) > 100:
		# 	self.lComEventId[:100]
		self.scheduleSave()

	def removeCompleteEvent(self, iEventId):
		'''从完成列表移除事件
		'''
		bFlag = False
		for index, dEventInfo in enumerate(self.lComEvent):
			if dEventInfo.get("iEventId", 0) != iEventId:
				continue
			self.lComEvent.pop(index)
			bFlag = True
			break
		if not bFlag:
			return False
		self.scheduleSave()
		return True

	def getCompleteEvent(self):
		return self.lComEvent

	#=====================================================
	#=====================================================
	def addProductEvent(self, iEventId):
		'''增加生产事件ID
		'''
		self.lProEvent.append(iEventId)
		# if len(self.lProEvent) > 100:
		# 	self.lProEvent = self.lProEvent[:100]
		self.scheduleSave()

	def addProductEventList(self, lProEvent):
		self.lProEvent.extend(lProEvent)
		self.scheduleSave()

	def removeProEvent(self, lRemoveId):
		for iEventId in lRemoveId:
			if iEventId in self.lProEvent:
				self.lProEvent.remove(iEventId)
		self.scheduleSave()

	def getProductEvent(self):
		return self.lProEvent

	def delProEvent(self):
		'''删除没有其它玩家标记过的事件
		'''
		lRemoveId = []
		for iEventId in self.lProEvent:
			if iEventId not in collect.gCenterCollectObj.dEventInfoObj:
				lRemoveId.append(iEventId)
		for iEventId in lRemoveId:
			self.lProEvent.remove(iEventId)
		if len(self.lProEvent) < 50:
			if lRemoveId:
				self.scheduleSave()
			return []
		gCenterCollectObj = collect.getCenterCollectObj()
		lRemoveId = []
		for iEventId in self.lProEvent:
			eventObj = gCenterCollectObj.getEventInfoObj(iEventId)
			if not eventObj:
				lRemoveId.append(iEventId)
				continue
			if not eventObj.lMarkerRoleId:
				lRemoveId.append(iEventId)
		if lRemoveId:
			self.removeProEvent(lRemoveId)
		return lRemoveId

	#=====================================================
	#=====================================================
	def isMarkerEvent(self, iEventId):
		for tmp in self.lMarkerEvent:
			if iEventId == tmp.get("iEventId", 0):
				return True
		return False

	def markerEvent(self, eventObj):
		'''标记事件
		'''
		tmp = {}
		tmp["iEventId"] = eventObj.iEventId
		tmp["iEventNo"] = eventObj.iEventNo
		tmp["iServerId"] = eventObj.iServerId
		tmp["sName"] = eventObj.sName
		tmp["iGender"] = eventObj.iGender
		tmp["sPicture"] = eventObj.sPicture
		tmp["fPosX"] = eventObj.fPosX
		tmp["fPosY"] = eventObj.fPosY
		tmp["iSchool"] = eventObj.iSchool
		self.lMarkerEvent.insert(0, tmp)

		if len(self.lMarkerEvent) > 60:
			lRemoveEvent = self.lMarkerEvent[60:]
			self.lMarkerEvent = self.lMarkerEvent[:60]
			for info in lRemoveEvent:
				collect.service4main.rpcC2BCollectDelEvent(self.iServerId, self.iRoleId, info.get("iEventId", 0), MARKER_EVENT)

		self.scheduleSave()
		eventObj.addMarkerRoleId(self.iRoleId)
		return tmp

	def removeMarkerEvent(self, iEventId):
		'''从标记列表移除事件
		'''
		bFlag = False
		iEventNo = 0
		for index, dEventInfo in enumerate(self.lMarkerEvent):
			if dEventInfo.get("iEventId", 0) != iEventId:
				continue
			self.lMarkerEvent.pop(index)
			iEventNo = dEventInfo.get("iEventNo", 0)
			bFlag = True
			break
		if not bFlag:
			return False,iEventNo
		self.scheduleSave()
		return True,iEventNo

	def getMarkerEvent(self):
		return self.lMarkerEvent[:50]

	#=====================================================
	#=====================================================
	def addTriggerRoleInfo(self, eventObj, roleInfoObj):
		'''增加事件触发者
		'''
		self.addLastId()
		tmp = {}
		tmp["iLastId"] = self.iLastId
		tmp["iEventId"] = eventObj.iEventId
		tmp["iDistance"] = collect.getLineDistance(roleInfoObj.fPosX, roleInfoObj.fPosY, eventObj.fPosX, eventObj.fPosY)
		tmp["iEventNo"] = eventObj.iEventNo
		tmp["iServerId"] = roleInfoObj.iServerId
		tmp["sName"] = roleInfoObj.sName
		tmp["iGender"] = roleInfoObj.iGender
		tmp["sPicture"] = roleInfoObj.sPicture
		tmp["iComTime"] = getSecond()
		tmp["iSchool"] = roleInfoObj.iSchool
		tmp["iRoleId"] = roleInfoObj.iRoleId

		self.lTriggerRole.insert(0, tmp)
		if len(self.lTriggerRole) > 50:
			lRemoveEvent = self.lTriggerRole[50:]
			self.lTriggerRole = self.lTriggerRole[:50]
			for info in lRemoveEvent:
				collect.service4main.rpcC2BCollectDelEvent(self.iServerId, self.iRoleId, info.get("iLastId", 0), TRIGGER_EVENT)

		self.scheduleSave()

	def removeTriggerInfo(self, iEventId):
		'''从触发列表移除事件
		'''
		bFlag = False
		for index, dEventInfo in enumerate(self.lTriggerRole):
			if dEventInfo.get("iLastId", 0) != iEventId:
			#if dEventInfo.get("iEventId", 0) != iEventNo:
				continue
			self.lTriggerRole.pop(index)
			bFlag = True
			break
		if not bFlag:
			return False
		self.scheduleSave()
		return True

	def getTriggerRoleInfo(self):
		return self.lTriggerRole


class cRoleInfoMng(object):
	def __init__(self):
		self.dRoleInfoObj = {}
	
	def loadAllFromDB(self):
		rs = db4center.gConnectionPool.query(sql4center.ROLEINFO_SELECT_ALL)
		for tInfo in rs.rows:
			iRoleId = tInfo[0]
			data = ujson.loads(tInfo[1])
			roleInfoObj = cRoleInfo(iRoleId)
			roleInfoObj.load(data)
			self.dRoleInfoObj[iRoleId] = roleInfoObj

	def getRoleInfoObj(self, iRoleId):
		if iRoleId not in self.dRoleInfoObj:
			roleInfoObj = cRoleInfo(iRoleId)
			self.dRoleInfoObj[iRoleId] = roleInfoObj
			roleInfoObj.onBorn()
			
		return self.dRoleInfoObj[iRoleId]

	def getAroundRole(self, iRoleId, iServerId, fPosX, fPosY):
		dOneKmRole = {}	#坐标相同只显示一个
		dTwoKmRole = {}	#坐标相同只显示一个
		roleInfoObj = self.dRoleInfoObj.get(iRoleId, None)
		iGender = roleInfoObj.iGender
		for _iRoleId, _roleInfoObj in self.dRoleInfoObj.iteritems():
			if iRoleId == _iRoleId:
				continue
			fLatitude = _roleInfoObj.fPosX
			fLongitude = _roleInfoObj.fPosY
			if not fLatitude and not fLongitude:
				continue
			iDistance = collect.getLineDistance(fPosX, fPosY, fLatitude, fLongitude)
			if iDistance > giTwoKm:
				continue
			if iDistance < giOneKm:
				# lOneKmRole.append(_iRoleId)
				dOneKmRole.setdefault((fLatitude, fLongitude), []).append(_iRoleId)
				if len(dOneKmRole) >= 20:
					# lTwoKmRole = []
					dTwoKmRole = {}
					break
			else:
				# lTwoKmRole.append(_iRoleId)
				dTwoKmRole.setdefault((fLatitude, fLongitude), []).append(_iRoleId)
				
		lOneKmRole = []
		lTwoKmRole = []
		for k,v in dOneKmRole.iteritems():
			_len = len(v)
			if _len > 1:
				lOneKmRole.append(v[rand(_len)])
			else:
				lOneKmRole.append(v[0])

		for k,v in dTwoKmRole.iteritems():
			_len = len(v)
			if _len > 1:
				lTwoKmRole.append(v[rand(_len)])
			else:
				lTwoKmRole.append(v[0])

		lAllRole = lOneKmRole + lTwoKmRole
		lSureRole = []		#确定列表
		lPrepareRole = []	#预备列表
		lWaitingRole = []	#待选列表
		for _iRoleId in lAllRole:
			_roleInfoObj = self.dRoleInfoObj.get(_iRoleId, None)
			if not _roleInfoObj:
				continue
			if iServerId == _roleInfoObj.iServerId:	#同服
				if iGender == _roleInfoObj.iGender: #同性
					lSureRole.append(_iRoleId)
				else:
					lWaitingRole.append(_iRoleId)
			else:
				lPrepareRole.append(_iRoleId)
		
		if len(lSureRole) < 20:
			lSureRole.extend(lWaitingRole)
			lSureRole.extend(lPrepareRole)
		return lSureRole[:20]


#===============================================================
#===============================================================
#===============================================================
MAX_EVENT_CNT = 20 #事件点最多收集20个
SEARCH_EVENT_CNT = 5	#事件数

class cEventInfo(object):
	def __init__(self, iEventId):
		self.iEventId = iEventId
		# 产生事件的玩家信息
		self.iEventNo = 0
		self.iRoleId = 0
		self.iServerId = 0
		self.sName = ""
		self.sPicture = ""
		self.iGender = 0
		self.iSchool = 0
		self.fPosX = 0
		self.fPosY = 0
		self.iEndTime = 0
		self.lTrigger = []
		self.lMarkerRoleId = []

	def scheduleSave(self):
		storageScheduler.appendCallLater(self._saveToDB, 'event_info', self.iEventId)

	def _saveToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.EVENT_UPDATE, sData, self.iEventId)

	def scheduleInsert(self):
		storageScheduler.appendCallLater(self._insertToDB, 'event_info', self.iEventId)

	def _insertToDB(self):
		dData = self.save()
		sData = ujson.dumps(dData)
		db4center.gConnectionPool.query(sql4center.EVENT_INSERT, self.iEventId, sData)

	def load(self, data):
		self.iEventNo = data.get("iEventNo", 0)
		self.iRoleId = data.get("iRoleId", 0)
		self.iServerId = data.get("iServerId", 0)
		self.sName = data.get("sName", "")
		self.sPicture = data.get("sPicture", "")
		self.iGender = data.get("iGender", 0)
		self.iSchool = data.get("school", 11)
		self.fPosX = data.get("fPosX", 0)
		self.fPosY = data.get("fPosY", 0)
		self.iEndTime = data.get("EndTime", 0)
		self.lTrigger = data.get("triger", [])
		self.lMarkerRoleId = data.get("marker", [])

	def save(self):
		data = {}
		data["iEventNo"] = self.iEventNo
		data["iRoleId"] = self.iRoleId
		data["iServerId"] = self.iServerId
		data["sName"] = self.sName
		data["sPicture"] = self.sPicture
		data["iGender"] = self.iGender
		data["school"] = self.iSchool
		data["fPosX"] = self.fPosX
		data["fPosY"] = self.fPosY
		data["EndTime"] = self.iEndTime
		data["triger"] = self.lTrigger
		data["marker"] = self.lMarkerRoleId
		return data

	def packetData(self):
		data = self.save()
		return data
	
	def onBorn(self, iEventNo, iRoleId, iServerId, sName, iGender, iSchool, fPosX, fPosY, **args):
		mainOutCollectObj = collect.getMainCollectObj()
		iTotalTime = mainOutCollectObj.getEventTime(iEventNo)

		self.iEventNo = iEventNo
		self.iRoleId = iRoleId
		self.iServerId = iServerId
		self.sName = sName
		self.iGender = iGender
		self.iSchool = iSchool
		self.fPosX = fPosX
		self.fPosY = fPosY
		self.iEndTime = getSecond() + iTotalTime * 3600
		self.lTrigger =[]

		self.scheduleInsert()

	def triggerSubEndTime(self):
		'''每个事件点一旦被触发
			 如果剩余时间 <= 1小时30分，则不做处理
			 如果剩余时间 > 1小时30分，则剩余时间 = 剩余时间 - 1小时
		'''
		if getSecond() - self.iEndTime < 90*60:
			return
		self.iEndTime = max(0, self.iEndTime-60*60)
		self.scheduleSave()

	def isValid(self):
		return True

	def eventName(self):
		mainOutCollectObj = collect.getMainCollectObj()
		return mainOutCollectObj.getEventName(self.iEventNo)

	def addMarkerRoleId(self, iRoleId):
		if iRoleId in self.lMarkerRoleId:
			return
		self.lMarkerRoleId.append(iRoleId)
		self.scheduleSave()

	def canSearch(self, fPosX, fPosY):
		iCurrentTime = getSecond()
		if self.iEndTime - iCurrentTime <= 30*60:
			return False,0
		iDistance = collect.getLineDistance(fPosX, fPosY, self.fPosX, self.fPosY)
		if iDistance > giTwoKm:
			return False,0
		return True,iDistance

class cCenterCollectMng(object):
	def __init__(self):
		self.timerMgr = timer.cTimerMng()
		self.dEventInfoObj = {}

	def loadAllFromDB(self):
		rs = db4center.gConnectionPool.query(sql4center.EVENT_SELECT_ALL)
		iCurrentTime = getSecond()
		for tInfo in rs.rows:
			iEventId = tInfo[0]
			data = ujson.loads(tInfo[1])
			eventObj = cEventInfo(iEventId)
			eventObj.load(data)
			self.dEventInfoObj[iEventId] = eventObj

	def autoCheckTimeOutEvent(self):
		self.timerMgr.run(self.checkTimeOutEvent, 1*60, 0, "autoCheckTimeOutEvent")

	def checkTimeOutEvent(self):
		'''定时删除事件
		'''
		self.autoCheckTimeOutEvent()
		iCurrentTime = getSecond()
		lDelEventId = []
		mainOutCollectObj = collect.getMainCollectObj()
		for iEventId, eventInfoObj in self.dEventInfoObj.iteritems():
			if iCurrentTime >= eventInfoObj.iEndTime:
				lDelEventId.append(iEventId)

		for iEventId in lDelEventId:
			self.removeEventInfo(iEventId)
	
	def newEventInfo(self, iEventNo, iRoleId, iServerId, sName, iGender, iSchool, fPosX, fPosY):
		'''产生新的事件
		'''
		# iEventId = NextEventUID()
		iEventId = collect.gCollectSingletonObj.nextEventId()
		eventObj = cEventInfo(iEventId)
		eventObj.onBorn(iEventNo, iRoleId, iServerId, sName, iGender, iSchool, fPosX, fPosY)
		self.dEventInfoObj[iEventId] = eventObj
		return iEventId

	def removeEventInfo(self, iEventId):
		'''删除的事件
		'''
		pass
		eventInfoObj = self.dEventInfoObj.get(iEventId, None)
		if not eventInfoObj:
			return
		self.dEventInfoObj.pop(iEventId, None)
		db4center.gConnectionPool.query(sql4center.EVENT_DELETE, iEventId)

	def getEventInfoObj(self, iEventId):
		'''事件
		'''
		if iEventId not in self.dEventInfoObj:
			# raise Exception,"室外收集玩法，{}事件不存在".format(iEventId)
			return None
		return self.dEventInfoObj[iEventId]

	def searchEvent(self, reqMsg):
		'''	如果达到1000米时事件 >= 5个，则搜索停止，不扩大范围
			如果1000米之内的事件 < 5个并且 >= 1个，则搜索范围往外扩展至2000米
			如果1000米之内的事件 = 0 或者 2000米之内的事件 < 5，则进入“自生产”流程
		'''
		iRoleId = reqMsg.iRoleId
		iServerId = reqMsg.iServerId
		iGender = reqMsg.iGender
		iSchool = reqMsg.iSchool
		fPosX,fPosY = float(reqMsg.fPosX), float(reqMsg.fPosY)
		lOneKmEvent = []
		lTwoKmEvent = []
		# mainOutCollectObj = collect.getMainCollectObj()
		roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
		# roleInfoObj.fPosX = fPosX
		# roleInfoObj.fPosY = fPosY
		#优先上一次搜索的事件
		lAllEventId = []
		lAllEventId.extend(roleInfoObj.getLastSearch())
		lAllEventId.extend(self.dEventInfoObj.keys())
		for iEventId in lAllEventId:
			if iEventId in lOneKmEvent or iEventId in lTwoKmEvent:
				continue
			eventInfoObj = self.dEventInfoObj.get(iEventId, None)
			if not eventInfoObj:
				continue
			if iEventId in roleInfoObj.lComEventId:#曾经完成过
				continue
			bFail,iDistance = eventInfoObj.canSearch(fPosX, fPosY)
			if not bFail:
				continue
			if iDistance < giOneKm:
				lOneKmEvent.append(iEventId)
				if len(lOneKmEvent) >= 5:
					lTwoKmEvent = []
					break
			else:
				lTwoKmEvent.append(iEventId)

		iOneKmEvent = len(lOneKmEvent)
		if iOneKmEvent <= 0:
			lTwoKmEvent = []
		lSelfProEvent = []
		if len(lOneKmEvent) == 0 or len(lTwoKmEvent) < 5:
			#进入自生产
			lSelfProEvent = self.selfProduction(reqMsg.iRoleId, reqMsg.iServerId, reqMsg.sName, reqMsg.iGender, reqMsg.iSchool, fPosX, fPosY)
		
		lAllEvent = lOneKmEvent + lSelfProEvent + lTwoKmEvent
		if len(lAllEvent) > 20:
			lAllEvent = lAllEvent[:20]

		lSureEvent = []#事件点列表
		lPrepareEvent = []#预备事件点列表
		lWaitingEvent = []#待选事件点列表
		for iEventId in lAllEvent:
			eventInfoObj = self.dEventInfoObj.get(iEventId, None)
			if not eventInfoObj:
				continue
			if iServerId == eventInfoObj.iServerId:	#同服
				if iGender == eventInfoObj.iGender: #同性
					lSureEvent.append(iEventId)
				else:
					lWaitingEvent.append(iEventId)
			else:
				lPrepareEvent.append(iEventId)
		
		if len(lSureEvent) < 20:
			lSureEvent.extend(lWaitingEvent)
			lSureEvent.extend(lPrepareEvent)
		roleInfoObj.setLastSearch(lSureEvent[:20])
		return roleInfoObj.lLastSearch

	def selfProduction(self, iRoleId, iServerId, sName, iGender, iSchool, fPosX, fPosY):
		'''自生产
			玩家自生产的点击最多50个，如果自生产时超过50个，则删除所有未被其他玩家标记的事件点
			如果删除后的事件点还是大于50个，则自生产数量 = 1
			自生产数量默认在5-15中随机
			以玩家所在点为中心，在100米-1000米之间随机产生自生产数量的事件点
		'''
		#玩家自生产的点击最多50个，如果自生产时超过50个，则删除所有未被其他玩家标记的事件点
		roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
		lRemoveId = roleInfoObj.delProEvent()
		for iEventId in lRemoveId:
			self.removeEventInfo(iEventId)

		# 如果删除后的事件点还是大于50个，则自生产数量 = 1
		# 自生产数量默认在5-15中随机
		iProCnt = 0
		if len(roleInfoObj.lProEvent) >= 50:
			 iProCnt = 1
		else:
			iProCnt = random.randint(5, 15)
		
		mainOutCollectObj = collect.getMainCollectObj()
		lEventNoKeys = shuffleList(mainOutCollectObj.eventInfo.keys())
		if not lEventNoKeys:
			raise Exception,"室外收集玩法，战斗表为空"
		index = 0
		iTotal = len(lEventNoKeys)-1
		lProEvent = []
		for i in xrange(iProCnt):
			iEventNo = lEventNoKeys[index]
			fLatitude, fLongitude = collect.getRandLatAndLongitude(fPosX, fPosY, 1, giOneKm)
			# print "===========fLatitude, fLongitude=",fPosX, fPosY,fLatitude, fLongitude,collect.getLineDistance(fPosX, fPosY, fLatitude, fLongitude)
			iEventId = self.newEventInfo(iEventNo, iRoleId, iServerId, sName, iGender, iSchool, fLatitude, fLongitude)
			lProEvent.append(iEventId)
			index += 1
			if index >= iTotal:
				index = 0
		roleInfoObj.addProductEventList(lProEvent)
		return lProEvent

	def triggerProduction(self, iRoleId, iServerId, sName, iGender, iSchool, fLatitude, fLongitude):
		'''触发生产
			玩家达到某个事件点附近并完成该事件时，进入“触发生成”流程
			以玩家当时所在点为中心，计算2000米内的事件点数量
			如果事件点数量 >= 10000，则跳出“触发生产”流程
			如果事件点数量 < 10000，则在200-2000米内随机产生一个事件点
		'''
		iCnt = 0
		iMaxCnt = 10000
		for iEventId, eventInfoObj in self.dEventInfoObj.iteritems():
			#距离
			fEventPosX = eventInfoObj.fPosX
			fEventPosY = eventInfoObj.fPosY
			iDistance = collect.getLineDistance(fPosX, fPosY, fEventPosX, fEventPosY)
			if iDistance < 20000:
				iCnt += 1
			if iCnt >= 10000:
				return

		mainOutCollectObj = collect.getMainCollectObj()
		lEventNoKeys = shuffleList(mainOutCollectObj.eventInfo.keys())
		if not lEventNoKeys:
			raise Exception,"室外收集玩法，战斗表为空"
		
		iEventNo = lEventNoKeys[index]
		fLatitude, fLongitude = collect.getRandLatAndLongitude(fPosX, fPosY, 1, giTwoKm)
		# print "===========fLatitude, fLongitude=",fPosX, fPosY,fLatitude, fLongitude
		iEventId = self.newEventInfo(iEventNo, iRoleId, iServerId, sName, iGender, iSchool, fLatitude, fLongitude)

	def triggerEvent(self, reqMsg):
		'''触发事件
		'''
		eventObj = self.getEventInfoObj(reqMsg.iEventId)
		if not eventObj:
			return 0,"该怪物已离开，此处只是它留下的幻影"
		#触发者
		iRoleId = reqMsg.iRoleId
		roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
		fPosX = float(reqMsg.fPosX)
		fPosY = float(reqMsg.fPosY)
		#判断距离
		if not config.IS_INNER_SERVER:
			iDistance = collect.getLineDistance(fPosX, fPosY, eventObj.fPosX, eventObj.fPosY)
			if iDistance > 100:
				return 0,"离怪物太远"
		eventObj.triggerSubEndTime()
		return eventObj.iEventNo,""


	def warWin(self, reqMsg):
		'''战斗胜利，加入事件列表
		'''
		eventObj = self.getEventInfoObj(reqMsg.iEventId)
		if not eventObj:
			return
		#触发者
		iRoleId = reqMsg.iRoleId
		fPosX = float(reqMsg.fPosX)
		fPosY = float(reqMsg.fPosY)
		roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
		#增加完成事件
		roleInfoObj.addCompleteEvent(fPosX, fPosY, eventObj)
		roleInfoObj.removeSpecialEvent(reqMsg.iEventId)
		collect.service4main.rpcC2BCollectAddEvent(COMPLETE_EVENT, eventObj, roleInfoObj)

		#产生者
		proRoleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(eventObj.iRoleId)
		if proRoleInfoObj:
			proRoleInfoObj.addTriggerRoleInfo(eventObj, roleInfoObj)
			collect.service4main.rpcC2BCollectAddEvent(TRIGGER_EVENT, eventObj, proRoleInfoObj, roleInfoObj)
		return eventObj.iEventNo,""


import ujson
import random
from common import *
import u
import collect
import timer
import config
import db4center
import sql4center
import center_collect_pb2
import scheduler
import collect.service4main
from collect.defines import *