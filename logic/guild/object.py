# -*- coding: utf-8 -*-
import pst
import block
import npc.object

class Guild(pst.cEasyPersist, block.cBlock):
	'''仙盟对象
	'''
	def __init__(self, guildId):
		pst.cEasyPersist.__init__(self, self._dirtyEventHandler)
		block.cBlock.__init__(self, "仙盟", guildId)
		self.setIsStm(sql.GUILD_INSERT)
		self.setUdStm(sql.GUILD_UPDATE)
		self.setSlStm(sql.GUILD_SELECT)
		self.setDlStm(sql.GUILD_DELETE)

		self.id = guildId
		self.memberList = {} # 成员列表
		self.applyList = {} # 申请列表，不存盘
		self.buildList = {} # 建筑列表
		self.banList = {} # 禁言列表，不存盘
		self.advertiseTime = 0 # 最近一次宣传时间
		self.mailTime = 0 # 最近一次群发邮件时间
		self.upgrading = 0 # 正在升级的建筑
		self.scene = None # 仙盟场景
		self.scene2 = None # 仙盟场景2
		self.day = cycleData.cCycDay(7, self._dirtyEventHandler)
		self.posMemberIds = {} # 职位列表{职位:set()}
		self.npcList = {} # npc列表
		self.guildFight = GuildFight(self, self._dirtyEventHandler) # 仙盟大战管理器

	def getValByName(self, attrName):
		'''根据属性名获取属性值
		'''
		if attrName in ("isAutoSignUp", "isSignUp"):
			return getValByName(self.guildFight, attrName)
		return getValByName(self, attrName)

	def getGuildId(self):
		'''获取仙盟ID
		'''
		return self.id

	def onBorn(self, **data):
		self.set("name", data["name"])
		self.set("tenet", data["tenet"])
		self.set("builder", data["chairmanId"])
		self.set("level", 1)
		self.set("fund", 1000000)
		self.set("birth", getSecond())
		self.initBuilding()
		self.set("sceneId", block.sysActive.gActive.genVirtualSceneId())
		self.set("scene2Id", block.sysActive.gActive.genVirtualSceneId())
		self.createScene()
		self.createNpc()
		self.createDoor()

	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		data["id"] = self.id
		memberList = {}
		for roleId, memberObj in self.memberList.iteritems():
			memberList[roleId] = memberObj.save()
		data["memberList"] = memberList
		data["build"] = self.saveBuilding()
		data["guildFight"] = self.guildFight.save()
		dDay=self.day.save()
		if dDay:
			data["d"]=dDay
		return data

	def load(self, data):
		if not data:
			return
		pst.cEasyPersist.load(self, data["data"])
		self.id = data["id"]
		memberList = data["memberList"]
		for memberId, memberData in memberList.iteritems():
			memberObj = Member(memberId)
			memberObj.load(memberData)
			self.memberList[memberId] = memberObj
			self.onAddMember(memberObj)
		if not self.scene2Id:
			self.set("scene2Id", block.sysActive.gActive.genVirtualSceneId())
		self.loadBuilding(data.get("build"))
		self.createScene()
		self.createNpc()
		self.createDoor()

		if data.get("guildFight"):
			self.guildFight.load(data["guildFight"])
		self.day.load(data.pop("d",{}))

	def _dirtyEventHandler(self):
		import factoryConcrete
		factoryConcrete.guildFtr.schedule2tail4save(self.id)

	def onAddMember(self, memberObj):
		memberObj.eDirtyEvent += self._dirtyEventHandler
		memberObj.ownerId = self.id
		self.updatePosition(memberObj.id, memberObj.getJob())

	def onRemoveMember(self, memberObj):
		self.updatePosition(memberObj.id, memberObj.getJob(), True)

	@property
	def name(self):
		return self.fetch("name", "未知仙盟")

	@property
	def chairmanName(self):
		chairmanId = self.getChairmanId()
		oChairman = self.getMember(chairmanId)
		return oChairman.name if oChairman else ""

	@property
	def level(self):
		return self.fetch("level")

	@property
	def sceneId(self):
		return self.fetch("sceneId")

	@property
	def scene2Id(self):
		return self.fetch("scene2Id")

	def getNotice(self):
		return self.fetch("notice", "管理员很懒，没有留下任何东西")

	def setNotice(self, notice):
		self.set("notice", notice)

	def getTenet(self):
		return self.fetch("tenet", "管理员很懒，没有留下任何东西")

	def setTenet(self, tenet):
		self.set("tenet", tenet)

	@property
	def birth(self):
		return self.fetch("birth")

	def getChairmanId(self):
		'''获取帮主ID
		'''
		chairman = list(self.posMemberIds.get(GUILD_JOB_CHAIRMAN, set()))
		return chairman[0] if len(chairman) > 0 else 0

	def setVitality(self, iValue):
		'''设置仙盟活跃度
		'''
		self.set("vitality", iValue)
		self.updateInfo("vitality")

	def getVitality(self):
		'''获取仙盟活跃度
		'''
		return self.fetch("vitality")

	def updateVitality(self, actCnt):
		'''仙盟活跃度更新
		'''
		vitality3 = self.day.fetch("vitality", iWhichCyc=-3)
		vitality2 = self.day.fetch("vitality", iWhichCyc=-2)
		vitality1 = self.day.fetch("vitality", iWhichCyc=-1)
		vitality = int(vitality3 * 0.2 + vitality2 * 0.3 + vitality1 * 0.6)
		curVitality = int(100 * actCnt / self.getSize()) 
		self.day.set("vitality", curVitality)
		self.setVitality(vitality)

	def getAllOnlineCount(self):
		'''获取所有在线的人员，包括学徒
		'''
		iCnt = 0
		for oMember in self.memberList.itervalues():
			if oMember.isOnline:
				iCnt += 1
		return iCnt

	def getOnline(self):
		'''获取在线成员
		'''
		iCnt = 0
		for oMember in self.memberList.itervalues():
			if oMember.getJob() != GUILD_JOB_APPRENTICE and oMember.isOnline:
				iCnt += 1
		return iCnt

	def getSize(self):
		'''获取仙盟成员数
		'''
		iCnt = 0
		for oMember in self.memberList.itervalues():
			if oMember.getJob() != GUILD_JOB_APPRENTICE:
				iCnt += 1
		return iCnt

	def getMaxSize(self):
		'''成员上限
		'''
		oWing = self.buildList.get(BUILD_WING)
		level = oWing.getLevel() if oWing else 0
		return guildData.getGuildMemberMax(level, "成员上限")

	def getApprenticeOnline(self):
		'''学徒在线人数
		'''
		iCnt = 0
		for roleId in self.posMemberIds.get(GUILD_JOB_APPRENTICE, set()):
			oMember = self.getMember(roleId)
			if oMember.isOnline:
				iCnt += 1
		return iCnt

	def getApprenticeSize(self):
		'''学徒数量
		'''
		return len(self.posMemberIds.get(GUILD_JOB_APPRENTICE, set()))

	def getApprenticeMax(self):
		'''学徒上限
		'''
		oWing = self.buildList.get(BUILD_WING)
		level = oWing.getLevel() if oWing else 0
		return guildData.getGuildMemberMax(level, "学徒上限")

	def getMaintainFund(self):
		'''维护资金
		'''
		return guildData.getGuildMaintain(self.level, "资金")

	def getMember(self, memberId):
		'''获取成员
		'''
		return self.memberList.get(memberId)

	def addMember(self, memberObj):
		'''增加成员
		'''
		memberObj.set("joinTime", getSecond())
		
		memberId = memberObj.id
		self.memberList[memberId] = memberObj
		self.onAddMember(memberObj)
		self.markDirty()
		
		who = getRole(memberId)
		if who:
			who.setGuildId(self.id)
			who.attrChange("guildId")
		else:
			offlineHandler.addHandler(memberId, "guildAddMember", guildId=self.id)
		self.updateMemberTitle(memberId, memberObj.getJob(), False)

	def removeMember(self, memberId):
		'''移除成员
		'''
		memberObj = self.memberList.pop(memberId, None)
		if not memberObj:
			return
		job = memberObj.getJob()
		self.onRemoveMember(memberObj)
		self.markDirty()
		self.guildFight.removeFromFightTeam(memberId)
		
		who = getRole(memberId)
		if who:
			who.setGuildId(0)
			who.attrChange("guildId")
		else:
			offlineHandler.addHandler(memberId, "guildRemoveMember", guildId=self.id)
		self.updateMemberTitle(memberId, job, True)

	def removeAllMember(self):
		'''移除所有成员
		'''
		memberList = self.memberList.keys()
		for roleId in memberList:
			who = getRole(roleId)
			oMember = self.getMember(roleId)
			if who and oMember:
				guild.service.rpcGuildMemberNotify(who, 2, oMember)
			self.removeMember(roleId)
			title = "仙盟解散"
			content = "你的仙盟已经被解散，你可以打开仙盟界面申请加入新的仙盟"
			mail.sendGuildMail(roleId, title, content, [], 0)

	def addApplyMember(self, roleId, level, school, name):
		'''增加申请成员
		'''
		applyInfo = {}
		applyInfo["level"] = level
		applyInfo["school"] = school
		applyInfo["name"] = name
		self.applyList[roleId] = applyInfo

	def removeApplyMember(self, roleId):
		'''删除申请成员
		'''
		self.applyList.pop(roleId, None)

	def clearApplyList(self):
		'''清空申请
		'''
		self.applyList = {}

	def isApplied(self, roleId):
		'''是否申请过
		'''
		return roleId in self.applyList

	def dismiss(self):
		'''解散
		'''
		self.scene.release()
		if self.scene2:
			self.scene2.release()
		self.removeAllMember()
		self.markDirty()
		block.cBlock._deleteFromDB(self)

	def checkDismiss(self):
		'''检查是否要强制解散
		'''
		warnStamp = self.fetch("fundWarn")
		if not warnStamp:
			return
		ti = getSecond()
		iLast = ti - warnStamp
		if iLast <= 0:
			return
		if iLast > 3600 * 24 * 3 - 10:
			# 超过三天强制解散
			import guild
			guild.dismissGuild(self.id)
		else:
			hour = iLast / 3600
			for roleId in self.memberList:
				title = "仙盟资金过低"
				content = "仙盟资金过低，请仙盟成员积极增加活跃度获得仙盟资金。若仙盟持续72小时无法进行正常维护，则仙盟会被强制解散。目前已持续#C02{}#n小时".format(hour)
				mail.sendGuildMail(roleId, title, content, [], 0)

	def createFundRebate(self):
		'''创建资金返还，建帮时返还了一次，还需返还三次
		'''
		cnt = self.fetch("rebate")
		if cnt >= 3:
			return
		builderId = self.fetch("builder")
		if not builderId:
			builderId = self.getChairmanId()
		cnt += 1
		self.set("rebate", cnt)
		title = "仙盟创建返利"
		content = "感谢你创建了仙盟，这是返还的#R<500,2,2>#n。[{}/3]".format(cnt)
		propsObj = props.new(200002)
		propsObj.setValue(500)
		mail.sendSysMail(builderId, title, content, [propsObj], 0)

	def calcActCnt(self):
		'''计算仙盟活跃点数与人数
		'''
		ttVitality, actCnt = 0, 0
		for oMember in self.memberList.itervalues():
			if oMember.getJob() == GUILD_JOB_APPRENTICE:
				continue
			v = oMember.fetch("vitality")
			ttVitality += v
			if v > 50:
				actCnt += 1
				oMember.addActiveDays()
		return ttVitality, actCnt

	def calcDailyAddBonus(self, ttVitality):
		'''计算每天仙盟增加的资金和分红
		'''
		fund = ttVitality * 500
		depotMax = self.getFundMax()
		depotDaily = max(self.getDailyAddFundMax() - self.day.fetch("fund", iWhichCyc=-1), 0)
		addFundDaily = min(depotDaily, fund)
		addFund = min(addFundDaily, depotMax-self.getFund())
		# 仙盟每天获得的仙盟资金会增加仙盟分红资金。不超过库房上限为50%，超过库房上限为60%。
		if addFundDaily < depotMax:
			addBonus = int(addFundDaily*0.5)
		else:
			addBonus = int(depotMax*0.5+(addFundDaily-depotMax)*0.6)
		return addFund, addBonus

	def dailyMaintain(self):
		'''日常维护
		'''
		if not self.getSize():
			import guild
			guild.dismissGuild(self.id)
			return
		ti = getSecond()
		# 一天资金结算
		ttVitality, actCnt = self.calcActCnt()
		addFund, addBonus = self.calcDailyAddBonus(ttVitality)
		maintain = self.getMaintainFund()
		self.addFund(addFund) # 资金增加
		self.addBonus(addBonus) # 分红增加
		# 仙盟库房里面的仙盟资金不够扣除维护费用时，仙盟训练场、铸币场、异兽房全部失效。若此状态持续3天，则仙盟会被强制解散。
		isNewGuild = True if ti - self.fetch("birth") < 3600 * 24 * 7 else False
		# 新建仙盟7天内不扣除仙盟维护资金
		if not isNewGuild:
			if self.getFund() > maintain:
				self.addFund(-maintain) # 维护消耗
				self.addLog("仙盟维护扣除了#C02{}#n仙盟资金".format(maintain))
				if self.fetch("fundWarn"):
					self.delete("fundWarn")
			else:
				if not self.fetch("fundWarn"):
					self.set("fundWarn", ti)
				self.addLog("仙盟资金无法正常维护，请补充资金。")
		self.updateVitality(actCnt)
		self.checkDismiss()

	def clearMemberWeeklyBonus(self):
		for memberId, memberObj in self.memberList.iteritems():
			memberObj.clearWeeklyData()
			memberObj.setBonus(0)

	def settleWeeklyBonus(self):
		'''仙盟每周分红结算
		'''
		self.clearMemberWeeklyBonus()
		b = self.fetch("bonus")
		if not b:
			return
		ttWeight = 0
		ttWeight += guildData.getWeight(GUILD_JOB_CHAIRMAN) * 1
		ttWeight += guildData.getWeight(GUILD_JOB_CHAIRMAN_VICE) * 1
		ttWeight += guildData.getWeight(GUILD_JOB_ELDER) * 4
		ttWeight += guildData.getWeight(GUILD_JOB_ELITE) * 20
		ttWeight += guildData.getWeight(GUILD_JOB_COMMON) * (self.getMaxSize() - 26)
		perBonus = b / ttWeight
		if not perBonus:
			return
		for memberId, memberObj in self.memberList.iteritems():
			job = memberObj.getJob()
			bonus = perBonus * guildData.getWeight(job)
			memberObj.setBonus(bonus)
		self.set("bonus", 0)
		self.updateInfo("bonus")
		self.addLog("仙盟上周总共获得了#C02{}#n仙盟分红".format(b))

	def onNewWeek(self):
		'''刷周时
		'''
		self.createFundRebate()

	def onNewDay(self, year, month, day, hour, wday):
		'''刷天时
		'''
		self.dailyMaintain()
		if wday == 1:
			self.settleWeeklyBonus()

	def onNewHour(self,now):
		'''刷时
		'''
		self.cleanTimeOutApprentice(now)
		self.updateApprenticeJob(now)
		self.dismissNotify(now)

	def onNewMinu(self):
		'''刷分钟
		'''
		if self.upgrading:
			self.checkBuildUpgrade()
		if self.banList:
			self.checkBan()
		if self.fetch("dismissApply"):
			self.dismissApplyHandle()
		if self.fetch("dismissCheck"):
			self.dismissCheckHandle()

	def addLog(self, log):
		'''增加日志
		'''
		log = "{}:{}".format(time.strftime("%Y-%m-%d", time.localtime(getSecond())), log)
		logs = self.fetch("log", [])
		logs.append(log)
		self.set("log", logs)
		self.updateInfo("log")

	def initBuilding(self):
		'''初始化仙盟建筑
		'''
		self.buildList = {}
		for idx, level in guildInitialBuild.iteritems():
			buildObj = Building(idx)
			buildObj.setLevel(level)
			self.buildList[idx] = buildObj

	def loadBuilding(self, buildList):
		'''加载仙盟建筑
		'''
		if not buildList or isinstance(buildList[1], int):
			self.initBuilding()
			return
		for idx, data in buildList.iteritems():
			buildObj = Building(idx)
			buildObj.load(data)
			self.buildList[idx] = buildObj
			if idx == BUILD_MAIN and self.fetch("level") != buildObj.getLevel():
				self.set("level", buildObj.getLevel())
		self.checkBuildUpgrade()

	def saveBuilding(self):
		'''保存仙盟建筑
		'''
		buildList = {}
		for idx, buildObj in self.buildList.iteritems():
			buildList[idx] = buildObj.save()
		return buildList

	def checkBuildUpgrade(self):
		'''检查仙盟建筑升级
		'''
		for idx, buildObj in self.buildList.iteritems():
			t = buildObj.getTime()
			if t is None:
				continue
			elif t == 0:
				upList = ["build"]
				if idx == BUILD_MAIN:
					self.add("level", 1)
					upList.extend(["level", "maintain"])
				elif idx == BUILD_WING:
					upList.extend(["maxSize", "apprenticeMax"])
				buildObj.upgrade()
				log = "#C02{}#n成功升级到了#C02{}#n级".format(buildObj.name, buildObj.getLevel())
				self.addLog(log)
				message.guildMessage(self.id, log)
				self.upgrading = 0
				self.updateInfo(*upList)
			else:
				self.upgrading = idx

	def buildingUpgrade(self, idx):
		'''升级仙盟建筑
		'''
		buildObj = self.buildList.get(idx)
		if not buildObj:
			return
		self.upgrading = idx
		buildObj.setTime(getSecond())

	def getBuilding(self, idx):
		'''获取建筑对象
		'''
		return self.buildList.get(idx)

	def getFund(self):
		'''仙盟资金
		'''
		return self.fetch("fund")

	def addFund(self, val, reason=""):
		'''增减仙盟资金
		'''
		if not val:
			return
		fundOld = self.fetch("fund")
		fundMax = self.getFundMax()
		fundNew = fundOld + val
		ret = val
		if val > 0:
			if self.day.fetch("fund") >= self.getDailyAddFundMax():
				return 0
			fundNew = min(fundMax, fundNew)
			ret = fundNew - fundOld
			self.day.add("fund", val)
		else:
			fundNew = max(fundNew, 0)
		self.set("fund", fundNew)
		self.updateInfo("fund")
		writeLog("guild/fund", "%d %d%+d->%d %s" % (self.id, fundOld, val, fundNew, reason))
		return ret

	def getFundMax(self):
		'''帮派资金上限
		'''
		wareHouse = self.buildList.get(BUILD_WAREHOUSE)
		level = wareHouse.getLevel() if wareHouse else 0
		return guildData.gdGuildDepot[level]["库房上限"]

	def getDailyAddFundMax(self):
		'''每日获得资金上限
		'''
		wareHouse = self.buildList.get(BUILD_WAREHOUSE)
		level = wareHouse.getLevel() if wareHouse else 0
		return guildData.gdGuildDepot[level]["获得资金"]

	def getBonus(self):
		'''仙盟分红
		'''
		return self.fetch("bonus")

	def addBonus(self, bonus):
		'''增减仙盟分红
		'''
		self.add("bonus", bonus)
		self.updateInfo("bonus")

	def cleanTimeOutApprentice(self, now):
		'''清理不上线的学徒
		'''
		removeList = []
		for oMember in self.memberList.itervalues():
			if oMember.getJob() != GUILD_JOB_APPRENTICE:
				continue
			offlineTime = oMember.getOfflineTime()
			if offlineTime and now - offlineTime > 72*60*60: #超过72小时的踢了
				removeList.append(oMember.id)
		for memberId in removeList:
			oMember = self.getMember(memberId)
			name = "学徒"
			if oMember:
				name = oMember.name
				guild.service.pushGuildMemberChange(self, 2, oMember)
				guild.service.pushGuildMemberSizeNotify(self)
			self.removeMember(memberId)
			mail.sendGuildMail(memberId,"仙盟踢人","由于你长期不上线，已被逐出了仙盟",[])
			message.guildMessage(self.id, "#C02{}#n因长期不上线被系统逐出了仙盟".format(name))

	def updateApprenticeJob(self, now):
		'''更新学徒职位
		'''
		for oMember in self.memberList.itervalues():
			if self.checkCanUpdate(oMember,now):
				oMember.setJob(GUILD_JOB_COMMON)

	def checkCanUpdate(self, oMember, now):
		'''检查能否更新学徒职位
		'''
		if oMember.getJob() != GUILD_JOB_APPRENTICE:
			return False
		if oMember.level < 50:
			return False
		if oMember.fetch("totalContri") < 100:
			return False
		if now - oMember.fetch("joinTime") <= 48*60*60: #需要超过48小时
			return False
		return True

	def createScene(self):
		'''创建仙盟场景
		'''
		import sceneData
		sceneRes = sceneData.getConfig(3010, "资源名")
		x = sceneData.getConfig(3010, "着陆点x")
		y = sceneData.getConfig(3010, "着陆点y")
		sceneName = sceneData.getConfig(3010, "场景名")
		self.scene2 = scene.new("仙盟", self.scene2Id, sceneName, sceneRes, 0, landX=x, landY=y)
		sceneRes = sceneData.getConfig(3020, "资源名")
		x = sceneData.getConfig(3020, "着陆点x")
		y = sceneData.getConfig(3020, "着陆点y")
		sceneName = sceneData.getConfig(3020, "场景名")
		self.scene = scene.new("仙盟", self.sceneId, sceneName, sceneRes, 0, landX=x, landY=y)

	def setBan(self, pos, roleId):
		'''禁言
		'''
		# {roleId:(pos, stamp)}
		if roleId in self.banList:
			return 0
		iBanTime = getSecond()+3600
		self.banList[roleId] = (pos, iBanTime)
		updateBanInfoToChat(roleId, iBanTime)
		return roleId

	def unBan(self, pos, roleId):
		'''解禁
		@return 0不在禁言列表 -1解禁权限不足 roleId解禁成功
		'''
		if roleId not in self.banList:
			return 0
		tBan = self.banList[roleId]
		if tBan[0] < pos:
			return -1
		self.banList.pop(roleId)
		updateBanInfoToChat(roleId, 0)
		return roleId

	def checkBan(self):
		ti = getSecond()
		dBan = dict(self.banList)
		for roleId, tBan in dBan.iteritems():
			if tBan[1] < ti:
				self.banList.pop(roleId)
				updateBanInfoToChat(roleId, 0)
				oMember = self.getMember(roleId)
				if oMember:
					guild.service.pushGuildMemberChange(self, 3, oMember)

	def updateInfo(self, *infoName):
		'''更新信息到客户端
		'''
		guild.service.pushGuildUpdateInfo(self, *infoName)

	def dismissNotify(self, ti):
		'''解散相关通知
		'''
		iApply = self.fetch("dismissApply")
		iCheck = self.fetch("dismissCheck")
		if iApply:
			hour = (3600 * 72 - (getSecond() - iApply)) / 3600
			msg = "盟主已经发起了解散仙盟，本仙盟将在#C02{}#n小时小时后由盟主前往仙盟管理员确认解散，等待期间盟主可主动取消。".format(hour)
			message.guildMessage(self.id, msg)
			return
		if iCheck:
			hour = (3600 * 72 - (getSecond() - iCheck)) / 3600
			msg = "本帮已经符合解散条件，请盟主{}小时内前往仙盟管理员确认解散，也可主动取消。".format(hour)
			message.guildMessage(self.id, msg)

	def dismissApplyHandle(self):
		'''解散申请检查
		'''
		iApply = self.fetch("dismissApply")
		ti = getSecond()
		if ti - iApply >= 3600 * 72:
			self.set("dismissCheck", ti)
			self.delete("dismissApply")
			msg = "您已经发起解散仙盟行动，请在#C0248#n小时内前往仙盟管理员处确认解散，等待期间可自动取消"
			title = "仙盟解散确认"
			mail.sendGuildMail(self.getChairmanId(), title, msg, [], 0)

	def dismissCheckHandle(self):
		'''解散确认检查
		'''
		iCheck = self.fetch("dismissCheck")
		ti = getSecond()
		if ti - iCheck >= 3600 * 48:
			self.delete("dismissCheck")	# 过期自动取消解散
			self.set("dismissCancel", ti)
			
	def searchMemberList(self, keyword):
		'''搜索成员
		'''
		if keyword.isdigit():
			keywordId = int(keyword)
		else:
			keywordId = 0
			
		resultList = []
		for memberId, memberObj in self.memberList.iteritems():
			if memberId == keywordId:
				resultList.append(memberObj)
			elif keyword in memberObj.name:
				resultList.append(memberObj)
				
		return resultList
	
	def getJob(self, memberId):
		'''职位
		'''
		memberObj = self.getMember(memberId)
		if memberObj:
			return memberObj.getJob()
		return 0

	def updatePosition(self, roleId, job, isClear=False):
		'''更新职位信息
		@roleId:成员ID
		@job:职位
		@isClear:是否清除该职位
		'''
		if isClear:
			self.posMemberIds.get(job, set()).discard(roleId)
			return
		memberObj = self.getMember(roleId)
		if not memberObj:
			return
		oldJob = memberObj.getJob()
		if oldJob != job:
			self.posMemberIds.setdefault(oldJob, set()).discard(roleId)
		self.posMemberIds.setdefault(job, set()).add(roleId)
		if oldJob == GUILD_JOB_APPRENTICE:
			upList = ["apprenticeSize", "apprenticeOnline", "online", "size"]
			self.updateInfo(*upList)

	def appoint(self, roleId, job):
		'''任命
		'''
		oMember = self.getMember(roleId)
		self.updatePosition(roleId, job)
		oMember.setJob(job)
		self.updateMemberTitle(roleId, job, False)

	def notifyMail(self, title, content, *jobList):
		'''发提醒邮件
		'''
		for memberId in self.memberList:
			if jobList and self.getJob(memberId) not in jobList:
				continue
			mail.sendGuildMail(memberId, title, content)

	def createNpc(self):
		'''创建仙盟NPC
		'''
		import guild.guildNpc.load
		for mod in guild.guildNpc.load.getModuleList().itervalues():
			npcObj = mod.Npc()
			npcObj.guild = weakref.proxy(self)
			self.npcList[npcObj.typeName] = npcObj
			x, y, d = npcObj.pos
			scene.switchSceneForNpc(npcObj, self.sceneId, x, y, d)
			
	def transSceneId(self, sceneId):
		'''转换仙盟地图id
		'''
		if isinstance(sceneId, str):
			if sceneId == "$scene1":
				return self.sceneId
			if sceneId == "$scene2":
				return self.scene2Id
			raise Exception("非法的仙盟地图传送门编号:%s" % sceneId)
		return sceneId

	def createDoor(self):
		'''创建仙盟地图的传送门
		'''
		for doorNo, info in guildData.gdGuildDoor.iteritems():
			sceneId = self.transSceneId(info["场景编号"])
			x = info["传送点x"]
			y = info["传送点y"]
	
			doorObj = Door(doorNo)
			doorObj.shape = info["造型"]
			doorObj.guild = weakref.proxy(self)

			scene.switchSceneForDoor(doorObj, sceneId, x, y)

	def getNpcByType(self, typeName):
		'''获取仙盟npc
		'''
		return self.npcList[typeName]

	def getHyperLink(self, roleId):
		'''获取仙盟申请超链接
		'''
		return "#L2<{},6,0,{}>*[申请加入]*02#n".format(roleId, self.id)

	def updateMemberTitle(self, roleId, job, isClear):
		'''更新成员称谓
		'''
		titleNo = guildTitles.get(job)
		who = getRole(roleId)
		if who:
			if isClear:
				title.removeTitle(who, titleNo)
				return
			title.newTitle(who, titleNo)
		else:
			offlineHandler.addHandler(roleId, "guildTitle", titleNo=titleNo, isClear=1 if isClear else 0)

	def addMemberGuildFight(self, roleId):
		'''增加成员盟战次数
		'''
		oMember = self.getMember(roleId)
		if not oMember:
			return
		oMember.addGuildFight()


class Member(pst.cEasyPersist):
	'''仙盟成员
	'''

	def __init__(self, roleId):
		pst.cEasyPersist.__init__(self)
		self.id = roleId # 玩家id
		self.ownerId = 0 # 仙盟id
		self.isOnline = False# 是否在线
		self.isRequested = False # 是否请求过仙盟信息

	@property
	def name(self):
		return self.fetch("name", "")
	
	@property
	def level(self):
		return self.fetch("level")
	
	@property
	def school(self):
		return self.fetch("school")

	@property
	def shape(self):
		return self.fetch("shape")

	@property
	def shapeParts(self):
		return self.fetch("shapeParts", [1, 1, 1, 1, 1, 0])

	@property
	def colors(self):
		return self.fetch("colors", [0, 0, 0, 0, 0, 0])

	def getOfflineTime(self):
		return 0 if self.isOnline else self.fetch("offlineTime")

	def updateInfo(self, who, guildObj=None):
		'''更新成员信息
		'''
		self.isOnline = True
		oldName = self.name
		self.set("name", who.name)
		self.set("level", who.level)
		self.set("school", who.school)
		self.set("shape", who.shape)
		self.set("fightPower", who.fightPower)
		self.set("curContri", who.getGuildPoint())
		self.set("totalContri", who.getTtGuildPoint())
		self.set("shapeParts", who.shapeParts)
		self.set("colors",who.getColors())
		self.set("vitality", who.getActPoint())
		self.set("guildRing", who.week.fetch("guildRing"))
		if guildObj:
			if oldName != self.name:
				guildObj.updateInfo("chairman")
			guild.service.pushGuildMemberChange(guildObj, 3, self)

	def setJob(self, job):
		'''设置职位
		'''
		self.set("job", job)

	def getJob(self):
		'''职位
		'''
		return self.fetch("job", GUILD_JOB_COMMON)

	def setBonus(self, bonus):
		'''设置分红
		'''
		self.set("bonus", bonus)
		who = getRole(self.id)
		if not who:
			return
		guild.service.rpcGuildWelfareInfo(who)

	def getBonus(self):
		'''分红
		'''
		return self.fetch("bonus")

	def setLogin(self, isLogin, guildObj):
		if isLogin:
			self.isOnline = True
			who = getRole(self.id)
			if who:
				if not title.hasTitleGroup(who, 20101):
					title.newTitle(who, guildTitles.get(self.getJob()))
				guild.service.rpcGuildWelfareInfo(who)
		else:
			self.isOnline = False
			self.isRequested = False
			self.set("offlineTime", getSecond())
		if self.getJob() == GUILD_JOB_APPRENTICE:
			upList = ["apprenticeOnline"]
		else:
			upList = ["online"]
		guildObj.updateInfo(*upList)
		guild.service.pushGuildMemberChange(guildObj, 3, self)

	def addActiveDays(self):
		'''增加周活跃天数
		'''
		self.add("activeDays", 1)

	def addTtGuildFight(self):
		'''增加总盟战次数
		'''
		self.add("ttGuildFight", 1)

	def addGuildFight(self):
		'''增加周盟战次数
		'''
		self.add("guildFight", 1)
		self.addTtGuildFight()

	def clearWeeklyData(self):
		self.delete("activeDays")
		self.delete("guildFight")


class Building(pst.cEasyPersist):
	'''仙盟建筑
	'''
	def __init__(self, idx):
		pst.cEasyPersist.__init__(self)
		self.idx = idx # 建筑序号
		self.ownerId = 0 # 仙盟id

	@property
	def name(self):
		return buildName.get(self.idx, "仙盟建筑")

	def getLevel(self):
		'''建筑等级
		'''
		return self.fetch("lv")

	def setLevel(self, lv):
		'''设置等级
		'''
		return self.set("lv", lv)

	def getCost(self):
		'''升级消耗
		'''
		return guildData.getBuildingUpgrade(self.getLevel()+1, "资金")

	def getTime(self):
		'''升级剩余时间
		'''
		start = self.fetch("up")
		if not start:
			return None
		hour = guildData.getBuildingUpgrade(self.getLevel()+1, "时间")
		ti = getSecond()
		surplus = hour * 3600 - (ti - start)
		return max(0, surplus)

	def setTime(self, ti):
		'''设置升级开始时间
		'''
		self.set("up", ti)

	def upgrade(self):
		'''建筑升级
		'''
		self.add("lv", 1)
		self.delete("up")


class GuildFight(pst.cEasyPersist):
	'''仙盟大战管理器
	'''
	
	def __init__(self, guildObj, dirtyHandler):
		pst.cEasyPersist.__init__(self, dirtyHandler)
		self.guildObj = guildObj

		# 仙盟大战精英
		self.fightTeam = {
			1: [], # 精英一队
			2: [], # 精英二队
			3: [], # 精英三队
		}
		
	def save(self):
		data = pst.cEasyPersist.save(self)
		data["fightTeam"] = self.fightTeam
		return data
		
	def load(self, data):
		if not data:
			return
		pst.cEasyPersist.load(self, data)
		self.fightTeam = data["fightTeam"]
		
	def isAutoSignUp(self):
		'''是否自动报名
		'''
		if self.fetch("autoSignUp"):
			return True
		return False
	
	def setAutoSignUp(self, isAutoSignUp):
		'''设置是否自动报名
		'''
		if isAutoSignUp:
			self.set("autoSignUp", 1)
		else:
			self.delete("autoSignUp")
			
	def isSignUp(self):
		'''是否已报名
		'''
		import activity
		actObj = activity.getActivity("guildFight")
		if actObj and actObj.isSignUp(self.guildObj.id):
			return True
		return False
		
	def addFightTeamMember(self, memberId, teamNo):
		'''增加仙盟大战精英
		'''
		self.fightTeam[teamNo].append(memberId)
		self.markDirty()
	
	def removeFromFightTeam(self, memberId):
		'''从仙盟大战精英队中移除
		'''
		for teamNo, memberList in self.fightTeam.iteritems():
			if memberId in memberList:
				memberList.remove(memberId)
				self.markDirty()
				return True
		return False
			
	def getFightTeamNo(self, memberId):
		'''获取玩家在仙盟大战精英队中的队号
		'''
		for teamNo, memberList in self.fightTeam.iteritems():
			if memberId in memberList:
				return teamNo
		return 0
		
	def getFightCount(self):
		'''仙盟大战次数
		'''
		return self.fetch("fightCount")
	
	def addFightCount(self, count):
		'''增加仙盟大战次数
		'''
		return self.add("fightCount", count)
	
	def getWinCount(self):
		'''胜利场数
		'''
		return self.fetch("winCount")
	
	def addWinCount(self, count):
		'''增加胜利场数
		'''
		return self.add("winCount", count)
	
	def getPKResultList(self):
		'''获取战况列表
		'''
		return self.fetch("pkResultList", [])
	
	def addPKResult(self, pkResult):
		'''增加战况
		'''
		pkResultList = self.fetch("pkResultList", [])
		pkResultList.append(pkResult)
		self.set("pkResultList", pkResultList)
		writeLog("guild/guildFight/pkResult", "%d %s" % (self.guildObj.id, pkResultList))
		
	def getPoint(self):
		'''仙盟大战积分
		'''
		return self.fetch("point")
	
	def addPoint(self, val):
		'''增加仙盟大战积分
		'''
		pointOld = self.fetch("point")
		point = pointOld + val
		if point < 0:
			point = 0
		self.set("point", point)
		writeLog("guild/guildFight/point", "%d %d%+d->%d" % (self.guildObj.id, pointOld, val, point))


import npc.object
class Npc(npc.object.NpcBase):
	'''仙盟npc
	'''
	
	def trigger(self, ep, who):
		if who.getGuildId() != self.guild.id:
			return
		npc.object.NpcBase.trigger(self, ep, who)


import door
class Door(door.cDoor):
	'''仙盟地图的传送门
	'''
	
	def destScNo(self):
		sceneId = self.getConfig("目标场景编号")
		return self.guild.transSceneId(sceneId)
	
	def getConfig(self, key, defaultVal=0):
		info = guildData.gdGuildDoor[self.no()]
		return info.get(key, defaultVal)



def updateBanInfoToChat(roleId, iBanTime):
	'''更新禁言信息到聊天服
	'''
	who = getRole(roleId)
	if who:
		role.register.updateRole(who, guildBan=iBanTime)


import time
from common import *
from guild.defines import *
import offlineHandler
import guildData
import sql
import mail
import timerEvent
import scene
import cycleData
import guild.service
import props
import message
import role.register
import task
import task.guildt
import block.sysActive
import title
import weakref