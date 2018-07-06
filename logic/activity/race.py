# -*- coding: utf-8 -*-
'''竞技场
'''
from activity.object import Activity as customActivity

# 匹配状态
MATCH_STATE_STOP = 0 # 停止匹配
MATCH_STATE_START = 1 # 开始匹配中
MATCH_STATE_SUCCESS = 2 # 匹配成功


#导表开始
class Activity(customActivity):

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*360+700,"宠物经验":lambda PLV:PLV*360+700,"银币":lambda LV:LV*500+1000,"物品":[1001],"活跃点":2},
		1002:{"经验":lambda LV:LV*180+350,"宠物经验":lambda PLV:PLV*180+350,"银币":lambda LV:LV*250+500,"物品":[1002],"活跃点":2},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":200,"物品":"225001","数量":"2"},
			{"权重":200,"物品":"225002","数量":"2"},
			{"权重":200,"物品":"225003","数量":"2"},
			{"权重":200,"物品":"225004","数量":"2"},
			{"权重":200,"物品":"225005","数量":"2"},
			{"权重":200,"物品":"225006","数量":"2"},
			{"权重":200,"物品":"225007","数量":"2"},
			{"权重":200,"物品":"225008","数量":"2"},
			{"权重":200,"物品":"225009","数量":"2"},
			{"权重":200,"物品":"225010","数量":"2"},
			{"权重":180,"物品":"230101","数量":"1"},
			{"权重":180,"物品":"230102","数量":"1"},
			{"权重":180,"物品":"230101","数量":"2"},
			{"权重":180,"物品":"230102","数量":"2"},
			{"权重":250,"物品":"230103","数量":"1"},
			{"权重":220,"物品":"234901","数量":"1","传闻":"SM3002"},
			{"权重":180,"物品":"246001","数量":"1"},
			{"权重":180,"物品":"246002","数量":"1"},
			{"权重":180,"物品":"246003","数量":"1"},
			{"权重":180,"物品":"246004","数量":"1"},
			{"权重":180,"物品":"246005","数量":"1"},
			{"权重":180,"物品":"246006","数量":"1"},
			{"权重":180,"物品":"246007","数量":"1"},
			{"权重":180,"物品":"246008","数量":"1"},
			{"权重":180,"物品":"246009","数量":"1"},
			{"权重":180,"物品":"246010","数量":"1"},
		),
		1002:(
			{"权重":200,"物品":"225001","数量":"1"},
			{"权重":200,"物品":"225002","数量":"1"},
			{"权重":200,"物品":"225003","数量":"1"},
			{"权重":200,"物品":"225004","数量":"1"},
			{"权重":200,"物品":"225005","数量":"1"},
			{"权重":200,"物品":"225006","数量":"1"},
			{"权重":200,"物品":"225007","数量":"1"},
			{"权重":200,"物品":"225008","数量":"1"},
			{"权重":200,"物品":"225009","数量":"1"},
			{"权重":200,"物品":"225010","数量":"1"},
			{"权重":180,"物品":"230101","数量":"1"},
			{"权重":180,"物品":"230102","数量":"1"},
			{"权重":180,"物品":"230101","数量":"2"},
			{"权重":180,"物品":"230102","数量":"2"},
			{"权重":250,"物品":"230103","数量":"1"},
			{"权重":220,"物品":"234901","数量":"1","传闻":"SM3002"},
			{"权重":180,"物品":"246001","数量":"1"},
			{"权重":180,"物品":"246002","数量":"1"},
			{"权重":180,"物品":"246003","数量":"1"},
			{"权重":180,"物品":"246004","数量":"1"},
			{"权重":180,"物品":"246005","数量":"1"},
			{"权重":180,"物品":"246006","数量":"1"},
			{"权重":180,"物品":"246007","数量":"1"},
			{"权重":180,"物品":"246008","数量":"1"},
			{"权重":180,"物品":"246009","数量":"1"},
			{"权重":180,"物品":"246010","数量":"1"},
		),
	}

	groupInfo = {
	}

	chatInfo = {
		1001:'''活动开启时间为#C04每周六19:55#n''',
		1002:'''参加竞技场需要#C04≥20级#n''',
		1003:'''为了公平对抗，竞技场只能#C04单人参加#n''',
		1004:'''本场景无法传送，请点击#C04【竞技场】#n按钮离开''',
		2001:'''竞技积分为零，不能再匹配''',
		3002:'''#C01$roleName#n幸运的在#L1<14,5>*[竞技场]*02#n战斗中获得了$lnkProps''',
		3003:'''你战胜了#C01$name#n''',
		3004:'''你被#C01$name#n击败了''',
		3005:'''对手已离线，重新开始匹配''',
		3006:'''冷却中，请稍候''',
		3007:'''出战成员中，治疗、辅助、封印职业数量之和#C04不能大于3#n''',
		3008:'''匹配太过频繁，请稍候再试''',
		3009:'''江湖风起云涌，能人辈出，诸位侠女少侠可在#C0420:00#n参与#L1<14,5>*[竞技场]*02#n一展身手，看谁才是真正佼佼者！''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	sceneInfo = {
		101:{"名称":"竞技场","资源":1130},
	}

	configInfo = {
		"清场时间":3600,
		"匹配等待时间":5,
		"胜利竞技积分":10,
		"失败竞技积分":-5,
		"胜利武勋":400,
		"失败武勋":320,
		"胜利冷却时间":10,
		"失败冷却时间":15,
		"奖励场数上限":5,
		"回合上限":30,
		"战报数上限":50,
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.raceInfoList = {} # 竞技信息列表
		self.orderList = [] # 排序列表
		
	def init(self):
		sceneObj = self.addScene(101)
		sceneObj.eventOnEnter += onEnter
		sceneObj.eventOnLeave += onLeave
		sceneObj.denyTeam = "单人竞技"
		sceneObj.denyTransfer = self.getText(1004)
		
		if self.inNormalTime():
			self.begin()
			
	def getTermNo(self):
		'''第几期
		'''
		return self.fetch("termNo")
	
	def addTermNo(self, val):
		self.add("termNo", val)
		
	def getGameScene(self):
		'''活动场景
		'''
		return self.getSceneByIdx(101)
		
	def inGameScene(self, who):
		'''是否在活动场景
		'''
		sceneObj = self.getGameScene()
		if sceneObj and sceneObj.id == who.sceneId:
			return True
		return False

	def inNormalTime(self):
		'''是否活动正式时间
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]

		if wday != 6:
			return False
		if hour not in (20, 21,):
			return False
		return True
	
	def inReadyTime(self):
		'''是否提前入场时间
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]

		if wday != 6:
			return False
		if hour != 19:
			return False
		if minute < 55:
			return False
		return True
	
	def getLeftTime(self):
		'''活动剩余时间
		'''
		if not self.inNormalTime():
			return 0
		
		datePartNow = getDatePart()
		year = datePartNow["year"]
		month = datePartNow["month"]
		day = datePartNow["day"]
		endTime = getSecond(year, month, day, 22)
		return max(0, endTime - getSecond())
	
	def onNewHour(self, day, hour, wday):
		if self.inNormalTime():
			if self.state == 0:
				self.begin()
		else:
			if self.state != 0:
				self.end()
				
		if wday == 6 and hour in (12, 19,):
			message.sysMessageRoll(self.getText(3009, 0))

	def begin(self):
		'''开始活动
		'''
		self.timerMgr.cancel("clearForEnd")
		self.state = 1
		self.raceInfoList = {}
		self.orderList = []
		self.addTermNo(1)
		
		# 活动开始，竞技积分减半
# 		for roleId, point in self.pointList.items():
# 			self.pointList[roleId] = max(30, int(point/2))

		rankObj = rank.getRankObjByName("rank_race_point")
		if rankObj:
			rankObj.onRaceBegin()
		
		sceneObj = self.getGameScene()
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who:
				continue
			self.createRaceInfo(who)
			rpcRaceEnter(who)
			rpcRaceInfo(who)
			if not self.validBuddy(who):
				self.doScript(who, None, "TP3007")
				continue
			self.setMatchState(who, MATCH_STATE_START, True) # 设置成开始匹配

		self.sysAutoMatch()
		rankObj.onRaceEnd()
	
	def end(self):
		'''结束活动
		'''
		self.state = 0

		ti = getattr(self, "clearTime", self.configInfo["清场时间"])
		self.timerMgr.run(self.clearForEnd, ti, 0, "clearForEnd")

		sceneObj = self.getGameScene()
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who:
				continue
			self.stopTimerMatch(who)
			rpcRaceEnter(who)

		rankObj = rank.getRankObjByName("rank_race_point")
		rankObj.onRaceEnd()
		
	def clearForEnd(self):
		'''结束清场
		'''
		self.timerMgr.cancel("clearForEnd")
		self.raceInfoList = {}
		self.orderList = []
		sceneObj = self.getGameScene()
		if not sceneObj:
			return
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who:
				continue
			self.leaveScene(who)
		
	def enterScene(self, who):
		'''进入竞技场
		'''
		sceneObj = self.getGameScene()
		if sceneObj:
			self.transfer(who, sceneObj.id)
		rank.updateRacePointRank(who)
		
	def leaveScene(self, who):
		'''离开竞技场
		'''
		sceneId, x, y = who.getLastRealPos()
		if not self.inNormalTime() and not self.inReadyTime():
			x = 0
			y = 0
		self.transfer(who, sceneId, x, y)
		
	def getRaceInfo(self, roleId):
		'''获取竞技信息
		'''
		return self.raceInfoList.get(roleId)
		
	def createRaceInfo(self, who):
		'''创建竞技信息
		'''
		roleId = who.id
		raceInfo = self.raceInfoList.get(roleId)

		if raceInfo:
			raceInfo["name"] = who.name, # 玩家名称
			raceInfo["shape"] = who.shape, # 玩家头像
			raceInfo["level"] = who.level, # 玩家等级
			raceInfo["pkPoint"] = who.getPKPoint()
			raceInfo["fightPower"] = who.fightPower
		else:
			who.addRacePoint(30, "竞技场")
			raceInfo = {
				"name": who.name, # 玩家名称
				"shape": who.shape, # 玩家头像
				"level": who.level, # 玩家等级
				"school": who.school, # 玩家门派

				"countWin": 0, # 胜利场数
				"countFight": 0, # 战斗场数
				"racePoint": who.getRacePoint(), # 竞技积分
				"pkPoint": who.getPKPoint(), # 武勋
				"fightPower": who.fightPower, # 战力
				"matchState": MATCH_STATE_STOP, # 匹配状态
				"matchTime": getSecond(), # 上次开始匹配时间
				"frozenTime": 0, # 冷却时间
				"fightInfoList": [], # 战报列表
			}
			self.raceInfoList[roleId] = raceInfo
			
	def updateRaceInfo(self, who, refresh=True, **attrList):
		'''更新竞技信息
		'''
		roleId = who.id
		raceInfo = self.raceInfoList.get(roleId)
		if not raceInfo:
			return

		refreshList = []
		for attrName, attrVal in attrList.iteritems():
			raceInfo[attrName] = attrVal
			if attrName in ("countWin", "countFight", "racePoint", "pkPoint", "matchState",):
				refreshList.append(attrName)
				
		if refresh and refreshList:
			rpcRaceInfoChange(who, *refreshList)
			
	def setMatchState(self, who, matchState, refresh=False):
		'''设置匹配状态
		'''
		self.updateRaceInfo(who, refresh, matchState=matchState)
		if matchState == MATCH_STATE_START:
			self.updateRaceInfo(who, matchTime=getSecond())
			
	def getMatchState(self, who):
		'''获取匹配状态
		'''
		raceInfo = self.getRaceInfo(who.id)
		if raceInfo:
			return raceInfo["matchState"]
		return MATCH_STATE_STOP
		
	def addCountWin(self, who, count, refresh=False):
		'''增加胜利场数
		'''
		raceInfo = self.getRaceInfo(who.id)
		if not raceInfo:
			return
		
		raceInfo["countWin"] += count
		if refresh:
			rpcRaceInfoChange(who, "countWin")
		
	def addCountFight(self, who, count, refresh=False):
		'''增加战斗场数
		'''
		raceInfo = self.getRaceInfo(who.id)
		if not raceInfo:
			return
		raceInfo["countFight"] += count
		if refresh:
			rpcRaceInfoChange(who, "countFight")
		who.day.set("raceFightCount", raceInfo["countFight"])
		
	def addRacePoint(self, who, val, refresh=False):
		'''增加竞技积分
		'''
		who.addRacePoint(val, "竞技场")
		point = who.getRacePoint()
		self.updateRaceInfo(who, refresh, racePoint=point)
		if point <= 0: # 竞技积分为0时，停止匹配
			self.setMatchState(who, MATCH_STATE_STOP, True)
		rank.updateRacePointRank(who)
			
	def addPKPoint(self, who, val, refresh=False):
		'''增加武勋值
		'''
		who.addPKPoint(val, "竞技场")
		point = who.getPKPoint()
		self.updateRaceInfo(who, refresh, pkPoint=point)
		
	def addFightInfo(self, who, result):
		'''增加战报
		'''
		raceInfo = self.getRaceInfo(who.id)
		if not raceInfo:
			return
				
		fightInfo = {
			"time": getSecond(),
			"times": raceInfo["countFight"],
			"result": result,
		}
		fightInfoList = raceInfo["fightInfoList"]
		fightInfoList.append(fightInfo)
		if len(fightInfoList) > self.configInfo["战报数上限"]:
			del fightInfoList[0]
		rpcRaceFightInfoAdd(who, fightInfo)
		message.tips(who, result)
			
	def inFrozen(self, who):
		'''是否冷却中
		'''
		raceInfo = self.getRaceInfo(who.id)
		if raceInfo and raceInfo["frozenTime"] > getSecond():
			return True
		return False
	
	def setFrozenTime(self, who, ti, refresh=False):
		'''设置冷却时间
		'''
		raceInfo = self.getRaceInfo(who.id)
		if not raceInfo:
			return
		
		if ti > 0:
			ti += getSecond()
		raceInfo["frozenTime"] = ti
		if refresh:
			rpcRaceInfoChange(who, "frozenTime")
		
	def matchStart(self, who):
		'''开始匹配
		'''
		if not self.state:
			return
		if self.getMatchState(who) != MATCH_STATE_STOP: # 不是停止匹配中
			return
		if who.getRacePoint() <= 0:
			self.doScript(who, None, "TP2001")
			return
		if self.inFrozen(who):
			self.doScript(who, None, "TP3006")
			return
		if not self.validBuddy(who):
			self.doScript(who, None, "TP3007")
			return
		
		self.stopTimerMatch(who)
		self.setMatchState(who, MATCH_STATE_START, True)
		self.doMatch(who)
	
	def matchStop(self, who):
		'''停止匹配
		'''
		self.stopTimerMatch(who)
		if self.state:
			self.setMatchState(who, MATCH_STATE_STOP, True)
		
	def doMatch(self, who):
		'''匹配PK
		'''
		if not self.validMatch(who):
			return

		self.makeOrderList()
		for i in xrange(2):
			targetId = self.searchMatchTarget(who, 30*i, 30*(i+1))
			if targetId:
				self.doPK(who.id, targetId)
			
	def searchMatchTarget(self, who, rangeBegin, rangeEnd):
		'''搜索匹配目标
		'''
		roleId = who.id
		if roleId not in self.orderList:
			return 0

		idx = self.orderList.index(roleId)
		idxMax = len(self.orderList) - 1
		targetList = []
		
		rangeBegin += 1
		rangeEnd += 1

		for i in xrange(rangeBegin, rangeEnd):
			idxLeft = idx - i # 向左更高排名找
			idxRight = idx + i # 向右更低排名找
			if idxLeft >= 0:
				targetList.append(self.orderList[idxLeft])
			if idxRight <= idxMax:
				targetList.append(self.orderList[idxRight])
				
		if not targetList:
			return 0
		
		tmpTargetList = targetList
		targetList = []
		lastRaceTarget = getattr(who, "lastRaceTarget", 0)
		for targetId in tmpTargetList:
			if lastRaceTarget and who.lastRaceTarget == targetId:
				continue
			targetObj = getRole(targetId)
			if not self.validMatch(targetObj):
				continue
			targetList.append(targetId)
			
		if not targetList:
			return 0
			
		targetList.sort(key=self._searchKey)
		return targetList[0]
	
	def _searchKey(self, roleId):
		raceInfo = self.getRaceInfo(roleId)
		return raceInfo["matchTime"], rand(100)
	
	def validMatch(self, who):
		'''检验可否匹配
		'''
		if not who:
			return False

		roleId = who.id
		if not self.inGameScene(who):
			return False
		if who.getRacePoint() <= 0:
			return False

		raceInfo = self.getRaceInfo(roleId)
		if not raceInfo:
			return False
		if who.isDisconnected(): # 已掉线
			return False
		if raceInfo["matchState"] != MATCH_STATE_START: # 不是开始匹配中
			return False
		if raceInfo["frozenTime"] > getSecond(): # 冷却中
			return False
		if who.inWar(): # 战斗中
			return False

		return True
	
	def validBuddy(self, who):
		'''检验助战伙伴
		'''
		count = 0

		if who.school in (12, 14, 16,):
			count += 1
		for buddyObj in who.buddyCtn.getCurrentBuddyList():
			if buddyObj.kind in ("治疗型", "辅助型", "封印型"):
				count += 1
		
		if count > 3:
			return False
		return True
	
	def makeOrderList(self):
		'''生成排序列表
		'''
		orderList = self.raceInfoList.keys()
		orderList.sort(key=self._orderKey)
		self.orderList = orderList
		
	def _orderKey(self, roleId):
		raceInfo = self.getRaceInfo(roleId)
		return -raceInfo["racePoint"], -raceInfo["fightPower"], roleId
	
	def sysAutoMatch(self):
		'''系统自动匹配
		'''
		self.makeOrderList()
		orderList = []
		for roleId in self.orderList:
			who = getRole(roleId)
			if not who:
				continue
			if not self.validMatch(who):
				continue
			orderList.append(roleId)
		
		step = 10 # 每10名随机匹配
		idxBegin = 0
		idxEnd = idxBegin + step
		roleIdList = orderList[idxBegin: idxEnd]

		while roleIdList:
			self.doAutoMatch(roleIdList)
			idxBegin = idxEnd
			idxEnd = idxBegin + step
			roleIdList = orderList[idxBegin:idxEnd]
			
	def doAutoMatch(self, roleIdList):
		'''自动匹配PK
		'''
		roleIdList = shuffleList(roleIdList)
		count = len(roleIdList)
		if count % 2 != 0:
			count -= 1

		for i in xrange(0, count, 2):
			roleId = roleIdList[i]
			targetId = roleIdList[i+1]
			self.doPK(roleId, targetId)
			
	def doPK(self, roleId, targetId):
		'''战斗PK
		'''
		who = getRole(roleId)
		targetObj = getRole(targetId)
		if not who or not targetObj:
			return
		if who.inWar() or targetObj.inWar():
			return
		
		# 停止定时匹配
		self.stopTimerMatch(who)
		self.stopTimerMatch(targetObj)
		
		# 匹配状态设成匹配成功
		self.setMatchState(who, MATCH_STATE_SUCCESS, True)
		self.setMatchState(targetObj, MATCH_STATE_SUCCESS, True)
		
		# 发送匹配对手信息
		rpcRaceMatchSend(who, targetObj)
		rpcRaceMatchSend(targetObj, who)

		# 等待几秒后开始战斗PK
		who.timerMgr.run(functor(self.startPK, who.id, targetId), self.configInfo["匹配等待时间"], 0, "startPK")
	
	def startPK(self, roleId, targetId):
		'''开始PK
		'''
		who = getRole(roleId)
		targetObj = getRole(targetId)
		if not who:
			self.doScript(who, None, "TP3005")
			self.doMatch(who)
			return
		if not targetObj:
			self.doScript(targetObj, None, "TP3005")
			self.doMatch(targetObj)
			return
		if who.inWar() or targetObj.inWar():
			return
		
		# 标记本次对手
		who.lastRaceTarget = targetObj.id
		targetObj.lastRaceTarget = who.id
		
		warObj = war.warctrl.createPKWar(who, targetObj, self, None)
		warObj.pkList = {
			TEAM_SIDE_1: {"roleId":roleId, "name":who.name},
			TEAM_SIDE_2: {"roleId":targetId, "name":targetObj.name},
		}
		
	def onWarWin(self, warObj, npcObj, w):
		'''战斗胜利时
		'''
		who = getRole(w.id)
		if not who:
			return

		self.addCountFight(who, 1)
		self.addCountWin(who, 1)
		self.addRacePoint(who, self.configInfo["胜利竞技积分"])
		self.addPKPoint(who, self.configInfo["胜利武勋"])

		# 冷却n秒后重新开始匹配
		self.setMatchState(who, MATCH_STATE_STOP)
		if who.getRacePoint() > 0:
			self.setFrozenTime(who, self.configInfo["胜利冷却时间"])
			self.setTimerMatch(who, self.configInfo["胜利冷却时间"])
		
		# 刷新数据给客户端
		rpcRaceInfoChange(who, "countFight", "countWin", "racePoint", "pkPoint", "matchState", "frozenTime")
		
		targetName = warObj.pkList[w.side^1]["name"]
		result = self.getText(3003)
		result = result.replace("$name", targetName)
		self.addFightInfo(who, result)
		
		self.doScript(who, npcObj, "R1001")
	
	def onWarFail(self, warObj, npcObj, w):
		'''战斗失败时
		'''
		who = getRole(w.id)
		if not who:
			return

		self.addCountFight(who, 1)
		self.addRacePoint(who, self.configInfo["失败竞技积分"])
		self.addPKPoint(who, self.configInfo["失败武勋"])

		# 冷却n秒后重新开始匹配
		self.setMatchState(who, MATCH_STATE_STOP)
		if who.getRacePoint() > 0:
			self.setFrozenTime(who, self.configInfo["失败冷却时间"])
			self.setTimerMatch(who, self.configInfo["失败冷却时间"])
		
		# 刷新数据给客户端
		rpcRaceInfoChange(who, "countFight", "racePoint", "pkPoint", "matchState", "frozenTime")
		
		targetName = warObj.pkList[w.side^1]["name"]
		result = self.getText(3004)
		result = result.replace("$name", targetName)
		self.addFightInfo(who, result)
		message.tips(who, result)
		
		self.doScript(who, npcObj, "R1002")
		
	def setTimerMatch(self, who, ti):
		'''设置定时匹配
		'''
		if not self.state:
			return
		if not self.inGameScene(who):
			return
		if who.getRacePoint() <= 0:
			return
		who.timerMgr.run(functor(self.doTimerMatch, who.id), ti, 0, "doTimerMatch")
		
	def stopTimerMatch(self, who):
		'''停止定时匹配
		'''
		who.timerMgr.cancel("doTimerMatch")
		
	def doTimerMatch(self, roleId):
		'''定时匹配
		'''
		who = getRole(roleId)
		if not who:
			return
		self.matchStart(who)
	
	def validReward(self, who, rwdIdx, npcObj):
		'''检查是否可奖励
		'''
		if rwdIdx in (1001, 1002,):
			raceInfo = self.getRaceInfo(who.id)
			if raceInfo and raceInfo["countFight"] <= self.configInfo["奖励场数上限"]:
				return True
			return False
		return True
	
	def customCheckBoutLimit(self, warObj):
		if warObj.bout >= self.configInfo["回合上限"]:
			countList = {TEAM_SIDE_1: 0, TEAM_SIDE_2: 0,}
			for side in warObj.teamList:
				for w in warObj.teamList[side].values():
					if w.isRole() or w.isPet() or w.isBuddy():
						countList[side] += 1

			if countList[TEAM_SIDE_1] > countList[TEAM_SIDE_2]:
				winner = TEAM_SIDE_1
			elif countList[TEAM_SIDE_2] > countList[TEAM_SIDE_1]:
				winner = TEAM_SIDE_2
			else:
				roleId = warObj.pkList[TEAM_SIDE_1]["roleId"]
				targetId = warObj.pkList[TEAM_SIDE_2]["roleId"]
				if self.orderList.index(roleId) < self.orderList.index(targetId):
					winner = TEAM_SIDE_1
				else:
					winner = TEAM_SIDE_2

			warObj.isEnd = True
			warObj.winner = winner
			
		return True
	
	def setupWar(self, warObj, who, npcObj):
		'''战斗设置
		'''
		warObj.noLost = True # 无损失
		warObj.deadEscape = True # 死亡可以逃跑
	
	def onAddWarrior(self, w):
		if w.isRole():
			w.sp = 50
			
	def customEscapeRatio(self, w):
		if w.isRole():
			return 100
		return None
		
	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("101-设置清场时间")
			txtList.append("201-结束")
			txtList.append("202-系统自动匹配")
			txtList.append("203-开始匹配")
			txtList.append("204-停止匹配")
			txtList.append("301-查看我的竞技信息")
			txtList.append("302-统计在场人数")
			txtList.append("303-查看排序")
			txtList.append("304-增加竞技积分")
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 101:
			try:
				ti = int(args[0])
			except:
				message.tips(who, "参数：时间(秒)")
				return
			if ti > 0:
				self.clearTime = ti
				message.tips(who, "设置清场时间为%d秒" % ti)
			elif hasattr(self, "clearTime"):
				del self.clearTime
				message.tips(who, "恢复清场时间为%d秒" % self.configInfo["清场时间"])
		elif cmdIdx == 201:
			self.end()
		elif cmdIdx == 202:
			self.sysAutoMatch()
		elif cmdIdx == 203:
			self.matchStart(who)
		elif cmdIdx == 204:
			self.matchStop(who)
		elif cmdIdx == 301:
			raceInfo = self.getRaceInfo(who.id)
			message.dialog(who, str(raceInfo))
		elif cmdIdx == 302:
			import entity
			sceneObj = self.getGameScene()
			roleIdList = list(sceneObj.getEntityIdsByType(entity.ETT_TYPE_ROLE))
			message.dialog(who, "在场人数:%d" % len(roleIdList))
		elif cmdIdx == 303:
			message.dialog(who, str(self.orderList))
		elif cmdIdx == 304:
			val = int(args[0])
			self.addRacePoint(who, val, True)
		elif cmdIdx == 400:
			rankObj = rank.getRankObjByName("rank_race_point")
			rankObj.onRaceEnd()
		elif cmdIdx == 401:
			who.addRacePoint(30, "指令")
			rank.updateRacePointRank(who)

			
	def getValueByVarName(self, varName, who):
		if varName == "R":
			return who.day.fetch("raceFightCount")
		return customActivity.getValueByVarName(self, varName, who)


def getActivity():
	return activity.getActivity("race")

def onEnter(who, oldScene, newScene):
	'''进入活动场景时
	'''
	if oldScene is newScene:
		return
	rpcRaceEnter(who)
	actObj = getActivity()
	if actObj.state:
		actObj.createRaceInfo(who)
		rpcRaceInfo(who)
		rpcRaceFightInfoList(who)

def onLeave(who, oldScene, newScene):
	'''离开活动场景时
	'''
	if oldScene is newScene:
		return
	actObj = getActivity()
	actObj.stopTimerMatch(who)
	actObj.setMatchState(who, MATCH_STATE_STOP)
	rpcRaceEnd(who)
	
	if hasattr(who, "lastMatchTime"):
		del who.lastMatchTime


# ================================================================
# 客户端发往服务端
# ================================================================
def validReceive(func):
	'''检查接收数据
	'''
	def _rpc(who, reqMsg):
		#print "\n", func.__name__, "roleId:%d" % who.id, str(reqMsg).replace("\n", ",")
		actObj = getActivity()
		if not actObj:
			return
		if not actObj.inGameScene(who):
			return
		if who.inWar():
			return
		func(actObj, who, reqMsg)
	return _rpc

@validReceive
def rpcRaceRankGet(actObj, who, reqMsg):
	'''请求竞技排行榜数据
	'''
	pass
# 	sendRaceRank(who)

@validReceive
def rpcRaceQuit(actObj, who, reqMsg):
	'''请求离开竞技场
	'''
	actObj.leaveScene(who)

@validReceive
def rpcRaceMatchStart(actObj, who, reqMsg):
	'''开始匹配
	'''
	if hasattr(who, "lastMatchTime") and (getSecond() - who.lastMatchTime) < 5:
		actObj.doScript(who, None, "TP3008")
		return
	who.lastMatchTime = getSecond()
	actObj.matchStart(who)

@validReceive
def rpcRaceMatchStop(actObj, who, reqMsg):
	'''停止匹配
	'''
	actObj.matchStop(who)


#===============================================================================
# 服务端发往客户端
#===============================================================================
# def sendRaceRank(who):
# 	'''发送竞技排行榜数据
# 	'''
# 	rankListMsg = []
# 	for i in xrange(10):
# 		rankNo = i + 1
# 		name = "玩家%s" %  rankNo
# 		rankMsg = act_race_pb2.rankMsg()
# 		rankMsg.rankNo = rankNo
# 		rankMsg.name = name
# 		rankMsg.schoolId = 11 + rand(6)
# 		rankMsg.racePoint = rand(1, 200)
# 		rankListMsg.append(rankMsg)
# 		
# 	rankMyMsg = act_race_pb2.rankMsg()
# 	rankMyMsg.rankNo = 0
# 	rankMyMsg.name = who.name
# 	rankMyMsg.schoolId = who.school
# 	rankMyMsg.racePoint = 11
# 		
# 	#toDo 排行榜数据
# 	msgObj = act_race_pb2.rankAllMsg()
# 	msgObj.rankList.extend(rankListMsg)
# 	msgObj.rankMy.CopyFrom(rankMyMsg)
# 	who.endPoint.rpcRaceRankSend(msgObj)

def validSend(func):
	'''检查发送数据
	'''
	def _func(who, *args, **kwargs):
		#print "\n", func.__name__, "roleId:%d" % who.id, args, kwargs
		actObj = getActivity()
		if not actObj:
			return
		if not actObj.inGameScene(who):
			return
		func(actObj, who, *args, **kwargs)
	return _func

@validSend
def rpcRaceEnter(actObj, who):
	'''进入竞技场
	'''
	timeout = 0
	state = 0 # 已结束
	if actObj.inReadyTime(): # 准备中
		state = 1
	elif actObj.state: # 进行中
		timeout = actObj.getLeftTime()
		state = 2
	msg = {
		"timeout": timeout,
		"state": state
	}
	who.endPoint.rpcRaceEnter(**msg)

@validSend
def rpcRaceInfo(actObj, who):
	'''显示竞技信息
	'''
	raceInfo = actObj.getRaceInfo(who.id)
	msg = {
		"countWin": raceInfo["countWin"], # 胜利场数
		"countFight": raceInfo["countFight"], # 战斗场数
		"racePoint": raceInfo["racePoint"], # 竞技积分
		"pkPoint": raceInfo["pkPoint"], # 武勋值
		"matchState": raceInfo["matchState"], # 匹配状态
	}
	who.endPoint.rpcRaceInfo(**msg)

@validSend
def rpcRaceInfoChange(actObj, who, *attrNames):
	'''修改竞技信息
	'''
	raceInfo = actObj.getRaceInfo(who.id)
	if not raceInfo:
		return

	msg = {}
	for attrName in attrNames:
		if attrName == "frozenTime":
			attrVal = max(0, raceInfo["frozenTime"] - getSecond())
		else:
			attrVal = raceInfo[attrName]
		msg[attrName] = attrVal
	who.endPoint.rpcRaceInfoChange(**msg)

@validSend
def rpcRaceEnd(actObj, who):
	'''结束竞技
	'''	
	who.endPoint.rpcRaceEnd()

@validSend
def rpcRaceFightInfoList(actObj, who):
	'''发送全部战报
	'''
	raceInfo = actObj.getRaceInfo(who.id)
	if not raceInfo:
		return

	infoList = []
	for fightInfo in raceInfo["fightInfoList"]:
		infoList.append(packetFightInfo(fightInfo))
		
	if not infoList:
		return
		
	msgObj = act_race_pb2.fightInfoList()
	msgObj.infoList.extend(infoList)
	who.endPoint.rpcRaceFightInfoList(msgObj)

@validSend
def rpcRaceFightInfoAdd(actObj, who, fightInfo):
	'''增加战报
	'''
	msgObj = packetFightInfo(fightInfo)
	who.endPoint.rpcRaceFightInfoAdd(msgObj)
	
def packetFightInfo(fightInfo):
	msgObj = act_race_pb2.fightInfo()
	msgObj.time = fightInfo["time"]
	msgObj.times = fightInfo["times"]
	msgObj.result = fightInfo["result"]
	return msgObj

@validSend
def rpcRaceMatchSend(actObj, who, targetObj):
	'''发送匹配对手信息
	'''
	msgObj = act_race_pb2.matchInfo()
	msgObj.roleId = targetObj.id
	msgObj.name = targetObj.name
	msgObj.shape = targetObj.shape
	msgObj.level = targetObj.level
	msgObj.school = targetObj.school
	msgObj.timeout = actObj.configInfo["匹配等待时间"]
	msgObj.fightPower = targetObj.fightPower
	who.endPoint.rpcRaceMatchSend(msgObj)

from common import *
from war.defines import *
import activity
import message
import act_race_pb2
import war.warctrl
import pst
import rank
import scene