# -*- coding: utf-8 -*-

if "gWarLastId" not in globals():
	gWarLastId = 0
	
def _newWarId():
	'''新战斗ID
	'''
	global gWarLastId
	gWarLastId += 1
	return gWarLastId

class War(object):
	
	def __init__(self, _type):
		self.id = _newWarId()
		war.getWarMgr().addObj(self, self.id)
		self.type = _type
		self.turnState = TURN_STATE_NONE
		
		self.roleList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}  # 参战玩家
		self.teamList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}  # 参战战士
		self.lastIdx = 0
		self.idxList = {}
		
		self.watchRoleList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}  # 观战玩家
		self.watchWarriorList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}  # 观战战士
		
		self.needCheckEnd = False  # 是否需要检查结束
		self.isEnd = False  # 是否结束
		self.needSort = False
		self.needSort2 = False
		self.winner = TEAM_SIDE_2  # 胜利者
		self.bout = 0  # 第几回合
		self.drawTime = 0  # 画图时间
		
		self.timerMgr = timer.cTimerMng()
		
		self.petStat = {}  # 宠物出战统计
		self.lineupList = {TEAM_SIDE_1:None, TEAM_SIDE_2:None}  # 阵法
		self.game = None  # 玩法对象
		self.gameNpc = None # 玩法的npc对象
		self.onWarEnd = None  # 结束处理函数

		self.teamInfoList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}} # 队伍信息
		
		self.clientDrawEndList = {} # 回合动画播放结束的客户端
		self.debugMsgList = [] # 战斗测试信息
		self.escapedList = [] # 成功逃跑的玩家
		self.funcList = {} # 附加处理函数
		
	def newIdx(self):
		'''新索引
		'''
		self.lastIdx += 1
		return self.lastIdx
	
	def addRoleFight(self, who, side):
		'''玩家进入战斗
		'''
		self.printDebugMsg("玩家[%s]进入战斗" % who.name)
		# toDo 设置只能接收战斗指令
		w = war.warrior.RoleWarrior()
		w.setup(who, self, side)
		self.addWarrior(w)
		self.addRole(who, w)
		
		if not self.teamInfoList[side]:
			teamObj = who.inTeam()
			if teamObj:
				teamId = teamObj.id
				leaderId = teamObj.leader
				size = teamObj.inTeamSize
			else:
				teamId = 0
				leaderId = who.id
				size = 1

			self.teamInfoList[side] = {
				"teamId": teamId,
				"leaderId": leaderId,
				"size": size,
			}
		
		# 参战宠
		if hasattr(who, "lastFightPetId"):
			del who.lastFightPetId
		self.petStat[who.id] = {}
		petObj = who.petCtn.getFighter()
		if petObj:
			sw = self.addPetFight(w, petObj)
			who.lastFightPetId = petObj.id
			if not hasattr(self, "noLost"):
				petObj.addLife(-1, "参战", None)
			
	def addTeamFight(self, teamObj, side):
		'''队伍进入战斗
		'''
		inTeamList = teamObj.getInTeamList()
		self.printDebugMsg("队伍进入战斗:%s" % inTeamList)
		for pid in inTeamList:
			who = getRole(pid)
			if not who:
				continue
			if who.inWar():  # 战斗中，暂离	
				teamObj.setLeave(who)
				continue
			self.addRoleFight(who, side)
	
	def addPetFight(self, roleW, petObj):
		'''宠物进入战斗
		'''
		side = roleW.side
		self.printDebugMsg("宠物[%s]进入战斗" % petObj.name)
		w = war.warrior.PetWarrior()
		w.setup(petObj, self, side)
		w.ownerIdx = roleW.idx
		self.addWarrior(w)
		roleW.petIdx = w.idx
		
		pid = roleW.getPID()
		self.petStat[pid][w.id] = self.petStat[pid].get(w.id, 0) + 1
		return w
	
	def addBuddyFight(self, roleW, buddyObj):
		'''伙伴进入战斗
		'''
		side = roleW.side
		self.printDebugMsg("伙伴[%s]进入战斗" % buddyObj.name)
		w = war.warrior.BuddyWarrior()
		w.setup(buddyObj, self, side)
		w.ownerIdx = roleW.idx
		self.addWarrior(w)
		return w
		
	def addMonsterFight(self, monsterObj, side):
		'''怪物进入战斗
		'''
		self.printDebugMsg("怪物[%s]进入战斗" % monsterObj.name)
		monsterType = monsterObj.monsterType
		if monsterType == MONSTER_TYPE_NORMAL: # 普通怪
			w = war.warrior.MonsterWarrior()
		elif monsterType == MONSTER_TYPE_BOSS: # 主怪
			w = war.warrior.BossWarrior()
		elif monsterType == MONSTER_TYPE_FRIEND: # 友军怪
			w = war.warrior.BossWarrior()
		else:
			raise Exception("[addMonsterFight]error monster type")
		
		w.monsterType = monsterType
		w.monsterIdx = monsterObj.monsterIdx
		if hasattr(monsterObj, "pos"):
			w.pos = monsterObj.pos
		w.setup(monsterObj, self, side)
		self.addWarrior(w)
		return w
		
	def addLineupEyeFight(self, eyeObj, side):
		'''阵眼进入战斗
		'''
		self.printDebugMsg("阵眼[%s]进入战斗" % eyeObj.name)
		w = war.warrior.LineupEyeWarrior()
		w.setup(eyeObj, self, side)
		self.addWarrior(w)
		return w
	
	def addRole(self, who, w):
		'''增加玩家
		'''
		self.roleList[w.side][who.id] = True
		who.enterWar(self, w)
		
	def addWatchRole(self, who, w):
		'''增加观战玩家
		'''
		self.watchRoleList[w.side][who.id] = True
		who.enterWar(self, w)
		
	def addWarrior(self, w):
		'''增加战士
		'''
		side = w.side
		self.printDebugMsg("\t[%s]队增加$type战士[%s]" % (side, w.name), w)
		
		# 站位
		if not hasattr(w, "pos"):
			w.pos = self.newPos(w)
		self.teamList[side][w.pos] = w
		
		# 索引，用于查找战士
		w.idx = self.newIdx()
		self.idxList[w.idx] = w
		
		# 阵法影响
		self.lineupEffect(w)
		self.onAddWarrior(w)
		
	def onAddWarrior(self, w):
		w.onAddWarrior()

		# 附加的处理
		for func in self.getFuncList("onAddWarrior"):
			func(w)
			
		# 玩法的特殊处理
		if hasattr(self.game, "onAddWarrior"):
			self.game.onAddWarrior(w)

	def newPos(self, w):
		if w.isPet(): # 宠物站在主人前面
			ownerW = self.getWarrior(w.ownerIdx)
			return 5 + ownerW.pos

		side = w.side
		if w.isRole():
			posList = POS_ROLE
		elif w.isBuddy():
			posList = POS_BUDDY
		elif w.isLineupEye():
			posList = POS_LINEUPEYE
		elif self.roleList[side]:
			posList = POS_FRIEND
		else:
			posList = POS_MONSTER
	
		for pos in posList:
			if pos not in self.teamList[side]:
				return pos

		raise Exception("[newPos]not found pos")
	
	def setLineup(self, lineupObj, side):
		'''设置阵法
		'''
		self.lineupList[side] = lineupObj
	
	def lineupEffect(self, w):
		'''阵法效果
		'''
		lineupObj = self.lineupList[w.side]
		if lineupObj:
			lineupObj.setupWarrior(w)
	
	def getWarrior(self, idx, notDead=True):
		'''根据索引获取战士
		'''
		w = self.idxList.get(idx)
		if not w:
			return None
		if notDead and w.isDead():
			return None
		return w
	
	def startTimer(self, func, ti, flag, interval=0):
		'''定时器开始
		'''
		self.timerMgr.run(func, ti, interval, flag)
		
	def stopTimer(self, flag):
		'''定时器结束
		'''
		self.timerMgr.cancel(flag)
		
	def hasTimer(self, flag):
		'''是否有定时器
		'''
		return self.timerMgr.hasTimerId(flag)
	
	def effectStatus(self, w, obj):
		'''战士状态影响到玩家、宠物
		'''
		if not obj:
			return
		if w.isRole():
			self.printDebugMsg("\t\t\t玩家战士[%s]状态影响到玩家" % obj.name)
		elif w.isPet():
			self.printDebugMsg("\t\t\t宠物战士[%s]状态影响到宠物" % obj.name)
		else: # 非法的战士
			try:
				raise Exception("[effectStatus]invalid warrior")
			except:
				logException()
			return
		
		if hasattr(self, "noLost"):  # 无损失
			return
		
		if hasattr(self.game, "customEffectStatus") and self.game.customEffectStatus(self, w, obj):
			pass
		else:
			obj.hp = min(w.hp, obj.hpMax)
			obj.mp = min(w.mp, obj.mpMax)
			if hasattr(obj, "sp"):
				sp = w.sp * rand(80, 100) / 100
				obj.sp = min(sp, obj.spMax)
			
		if obj.hp < 1:
			self.onDie(w, obj)

		obj.recover(False)
		obj.refreshState()
	
	def onDie(self, w, obj):
		'''死亡处理
		'''
		if hasattr(self.game, "customOnDie") and self.game.customOnDie(self, w, obj):
			return

		obj.hp = 1
		obj.mp = obj.mpMax

		if w.isRole():
			self.consumeEquipLifeOnDie(obj)
		elif w.isPet():
			obj.addLife(-10, "死亡", None)
		
	def handleForEscape(self):
		'''逃跑玩家的处理
		'''
		if not self.escapedList:
			return

		roleIdList = self.escapedList
		self.escapedList = []

		for roleId in roleIdList:
			who = getRole(roleId)
			if not hasattr(who, "warrior"):
				continue
				
			w = who.warrior
			side = w.side
			who.leaveWar()

			if who.inTeam() and len(self.roleList[side]):  # 暂离
				who.getTeamObj().setLeave(who)
			if hasattr(self.game, "onEscaped"): # 玩法对逃跑的处理
				self.game.onEscaped(self, self.gameNpc, w)
	
	def kickWarrior(self, w):
		'''踢除战士
		'''
		self.printDebugMsg("\t\t踢除$type战士[%s]!!!!" % w.name, w)
		w.release()
		self.needCheckEnd = True
					
		if w.isWatcher():  # 观战玩家
			self.kickWatcher(w)
		else:
			self._rpcWarDelWarrior(w)
			
			side = w.side
			if w.idx in self.idxList:
				del self.idxList[w.idx]
			if w.pos in self.teamList[side]:
				del self.teamList[side][w.pos]
			
			if w.type == WARRIOR_TYPE_ROLE:
				self._rpcWarEnd(w)
				
				pid = w.id
				if pid in self.roleList[side]:
					del self.roleList[side][pid]
				
				who = getRole(pid)
				self.effectStatus(w, who)
								
				if hasattr(w, "isEscaped"):	# 逃跑的玩家等待逃跑动画结束才真正离开战斗
					self.escapedList.append(who.id)
				else:
					who.leaveWar()

				# 清除参战宠物
				if w.petIdx:
					sw = self.getWarrior(w.petIdx, False)
					if sw:
						self.kickWarrior(sw)

				# 没有玩家在战斗了，清除伙伴
				if len(self.roleList[side]) == 0:
					for _w in self.teamList[side].values():
						if _w.isBuddy():
							self.kickWarrior(_w)

			elif w.type == WARRIOR_TYPE_PET:
				pw = self.getWarrior(w.ownerIdx, False)
				if pw:
					pw.petIdx = 0

				who = getRole(w.getPID())
				if who:
					petObj = who.petCtn.getItem(w.id)
					if petObj:
						self.effectStatus(w, petObj)
	
	def kickWatcher(self, w):
		self._rpcWarEnd(w)
		
		pid = w.id
		side = w.side
		if pid in self.watchWarriorList[side]:
			del self.watchWarriorList[side][pid]
		if pid in self.watchRoleList[side]:
			del self.watchRoleList[side][pid]
		
		who = getRole(pid)
		if not who:
			return
		
		who.leaveWar()
		
		if who.inTeam() and who.getTeamObj().isLeader(who.id):  # 队长退出观战，其他在队队员也退出
			for pid in who.getTeamObj().getInTeamList():
				if pid == who.id:
					continue
				obj = getRole(pid)
				if not obj or not obj.inWar():
					continue
				obj.war.kickWatcher(obj.warrior)
				message.tips(obj, "队长退出了观战")

	def addWatch(self, who, side):
		'''玩家进入观战
		'''
		w = war.warrior.WatchWarrior()
		w.setup(who, self, side)
		w.side = side
		w.idx = 0
		w.war = weakref.proxy(self)
		self.addWatchRole(who, w)
		self.watchWarriorList[side][w.id] = w
		self.reEnter(w)
		
	def addTeamWatch(self, teamObj, side):
		'''队伍进入观战
		'''
		inTeamList = teamObj.getInTeamList()
		self.printDebugMsg("队伍进入观战:%s" % inTeamList)
		for pid in inTeamList:
			memberObj = getRole(pid)
			if not memberObj:
				continue
			if memberObj.inWar():  # 战斗中，暂离	
				teamObj.setLeave(memberObj)
				continue
			self.addWatch(memberObj, side)

	def reEnter(self, w):
		'''重新进入战斗
		玩家重新进入或观点玩家进入
		'''
		if w.isRole(): # 参战玩家
			self.clearAutoFightForTimeout(w.getPID(), refresh=False)
			w.autoFight= False # 强制手动
		
		self._rpcWarStart(w)
		if hasattr(w, "autoFight"):
			del w.autoFight
	
		for side in self.teamList:
			posList = self.teamList[side].keys()
			posList.sort()
			for pos in posList:
				_w = self.teamList[side][pos]
				self.rpcAddWarrior(_w, w)
				self.rpcWarAllBuff(_w, w)
				
				if (w.isRole() or w.isPet()) and w.command:
					self._rpcWarSetCmd(w)

		if self.turnState == TURN_STATE_READY: # 进入倒计时
			self._rpcWarTurnReady(w=w)
		else: # 等待下一轮开始
			self._rpcWarTurnWait(w)

		# 标识宠物
# 		if w.petIdx:
# 			sw = self.getWarrior(w.petIdx)
# 			if sw:
# 				# toDo 客户端标识宠物
# 				pass

# 		if w.isRole():
# 			# toDo 设置只能接收战斗指令
# 			pass

	def start(self):
		'''战斗开始
		'''
		self.printDebugMsg("\n\n====================战斗开始====================")
		
		self.startTime = getSecond()
		#扣除装备耐久
		self.consumeEquipLifeOnWarStart()
		
		self._rpcWarStart()
					
		for side in self.teamList:
			for w in self.teamList[side].values():
				self.rpcAddWarrior(w)
				self.rpcWarAllBuff(w, None)
				
				if w.isPet():
					# toDo 客户端.标识宠物
					pass
				self.printDebugMsg("[%s]  --->%s" % (w.name, w.getWarMsg()))

		# 登场
		for side in self.teamList:
			for w in self.teamList[side].values():
				self.onStartWar(w)

		self.readyTurn()
		
	def readyTurn(self):
		'''准备新一轮
		'''
		if self.hasTimer("startTurn"):
			self.stopTimer("startTurn")

		self.bout += 1
		self.clientDrawEndList = {}
		self.printDebugMsg("\n====================第%d回合准备====================" % self.bout)
		
		self.turnState = TURN_STATE_READY
		self.readyTime = getSecond()
		self._rpcWarTurnReady(timeoutTime=TURN_TIME)
		self.startTimer(self.startTurn, TURN_TIME, "startTurn")
# 		self.startTimer(self.autoTryStartTurn, 6, "autoTryStartTurn")
		
	def startTurn(self):
		'''开始新一轮
		'''
		self.printDebugMsg("\n====================第%d回合开始====================" % self.bout)
		if self.hasTimer("startTurn"):
			self.stopTimer("startTurn")
# 		if self.hasTimer("autoTryStartTurn"):
# 			self.stopTimer("autoTryStartTurn")
			
		self.setAI()

		self.printDebugMsg("\n====================战士出手，结算====================")
		self.turnState = TURN_STATE_BEGIN
		self._rpcWarTurnBegin()
		self.drawTime = 0
		self.execute()
		self.checkEnd()
		if not self.isEnd:
			self.checkBoutLimit()

		try:
			assert self.bout <= MAX_BOUT, u.trans("回合数异常")
		except:
			logException()
			self.isEnd = True

		self.turnState = TURN_STATE_END
		self._rpcWarTurnEnd()
		self.startTimer(self.drawEnd, self.drawTime, "drawEnd")
		self.printDebugMsg("\n====================第%d回合结束，等待客户端播放动画，画图时间%s====================" % (self.bout, self.drawTime))
		
	def setAI(self):
		'''AI设置'''
		self.printDebugMsg("\n====================AI设置====================")
		for side in self.teamList:
			for w in self.teamList[side].values():
				if w.command is None:
					self.setDefaultCommand(w)
					if w.isRole() or w.isPet():
						self.setAutoFightForTimeout(w.getPID()) # 本回合没有下达指令，下回合就自动了
					
	def setDefaultCommand(self, w):
		'''设置默认指令
		'''
		cmdType = CMD_TYPE_PHY
		performId = 0
		
		if hasattr(w, "aiSetList"): # 使用自定义AI集
			cmdType = CMD_TYPE_AI
		elif w.isBuddy(): # 使用伙伴AI集
			cmdType = CMD_TYPE_AI
		else:
			if w.isRole(): # 人物
				performId = w.getAutoPerform()
			elif w.isPet(): # 宠物
				performId = w.getDefaultPerform()
			else: # 怪物等
				performId = self.getMonsterAI(w)
			if performId >= 100: # 法术攻击
				cmdType = CMD_TYPE_MAG
			elif performId > 0: # 普通物理攻击、防御等
				cmdType = performId
				performId = 0
			
		war.commands.setCommand(self, w, cmdType, performId=performId)
	
	def getMonsterAI(self, w):
		'''获取怪物AI
		'''
		performId = CMD_TYPE_PHY

		performList = []
		for performObj in w.getPerformList():
			if perform.isSEPerform(performObj.id): # 特技
				if w.hasApply("禁止特技"):
					continue
			elif w.hasApply("禁止法术"): # 法术
				continue
			performList.append(performObj.id)
		
		if len(performList):
			performId = performList[rand(len(performList))]
					
		if performId == CMD_TYPE_PHY and (w.hasApply("禁止物理攻击") or w.isLineupEye()):
			performId = CMD_TYPE_WAIT
					
		return performId
				
	def getCommandTarget(self, att, pfId):
		'''取得指令目标
		'''
		vic = None
		if pfId == CMD_TYPE_PHY:
			vic = att.getEnemyTarget(None, pfId)
		else:
			pfObj = att.getPerform(pfId)
			if pfObj:
				vic = pfObj.getCommandTarget(att)
			
		return vic
	
	def onSetRoleCommand(self, w):
		'''设置玩家指令时
		'''
		self._rpcWarSetCmd(w)
		self.tryStartTurn()
		
	def tryStartTurn(self):
		'''尝试开始新一轮，只有全部玩家都下达指令时才会成功
		'''
		for side in self.teamList:
			for w in self.teamList[side].values():
				if not (w.isRole() or w.isPet()):
					continue
				who = getRole(w.getPID())
				if not who:
					continue
				if not who.endPoint: # 已掉线
					continue
# 				if hasattr(who.warrior, "autoFight") and (getSecond() - self.readyTime) >= 6: # 上回合超时的玩家本回合6秒后忽略
# 					continue
				if not w.command: # 还有玩家未下达指令
					return

		self.startTurn()
		
# 	def autoTryStartTurn(self):
# 		'''自动尝试开始新一轮'''
# 		if self.hasTimer("autoTryStartTurn"):
# 			self.stopTimer("autoTryStartTurn")
# 		self.startTimer(self.autoTryStartTurn, 3, "autoTryStartTurn")
# 		self.tryStartTurn()
	
	def execute(self):
		'''出招
		'''
		# 计算出招速度
		for side in self.teamList:
			for w in self.teamList[side].values():
				w.calSpeed()
				w.isAct = False  # 是否已出招
				if hasattr(w, "ignoreAct"):
					del w.ignoreAct

		# 回合开始
		self.newRound()
		
		self.needSort = True
		self.needSort2 = True
		
		# 未死亡的战士出招
		while self.needSort:
			if self.isEnd:
				break
			self.executeCmd(False)
	
		# 复活的战士出招
		while self.needSort or self.needSort2:
			if self.isEnd:
				break
			self.executeCmd(True)
		
		# 回合结束
		self.endRound()

	def newRound(self):
		'''回合开始
		'''
		for side in self.teamList:
			for w in self.teamList[side].values():
				if self.isEnd:
					return
				if not w.inWar():
					continue
				w.newRound()
				if self.needCheckEnd:
					self.checkEnd()
					
		# 附加的处理
		for func in self.getFuncList("onNewRound"):
			func(self)

	def endRound(self):
		'''回合结束
		'''
		for side in self.teamList:
			for w in self.teamList[side].values():
				if self.isEnd:
					return
				w.endRound()
				if self.needCheckEnd:
					self.checkEnd()
		
		# 清理
		for side in self.teamList:
			for w in self.teamList[side].values():
				if self.isEnd:
					return
				if w.hasApply("逃跑指令") and w.isDead() and self.isDeadEscape(w):
					w.isEscaped = True
					self.kickWarrior(w)
					continue
				w.cleanRound()
				if self.needCheckEnd:
					self.checkEnd()
		
		# 附加的处理
		for func in self.getFuncList("onEndRound"):
			func(self)
			
	def executeCmd(self, isRevive):
		'''执行指令
		'''
		if self.isEnd:
			return
		
		wList = self.sortWarrior()
		for w in wList:
			if not w.inWar():
				continue
			if w.isAct:
				continue
			if w.isDead():
				w.ignoreAct = True
				continue
			
			if isRevive:
				if not hasattr(w, "ignoreAct"):
					continue
				del w.ignoreAct
			else:
				if hasattr(w, "ignoreAct"):
					continue

			w.isAct = True
			if w.hasApply("禁止指令"):
				message.tips(w.getPID(), "封禁状态，无法行动")
			else:
				if w.isPet():
					self.setRandomEscape(w)
				self.onCommand(w)
				w.command(w)
			
			if hasattr(self, "addDeadTime"):
				if self.addDeadTime == 1:
					self.drawTime += magicTimeData.getTime(MAGIC_DIE, w.shape)
				elif self.addDeadTime == 2:
					if isRevive:
						self.drawTime += 1.2
					else:
						self.drawTime += 0.6
				del self.addDeadTime

			if self.needCheckEnd:
				self.checkEnd()
			if self.isEnd:
				break
			if self.needSort:
				break
			
	def setRandomEscape(self, w):
		'''随机逃跑
		'''
		if w.hasApply("禁止逃跑"):
			return
		
		ratio = w.hp * 100 / w.hpMax
		if ratio < 30 and rand(100) < 5:
			war.commands.setCommand(self, w, CMD_TYPE_ESCAPE)
		
	def sortWarrior(self):
		'''根据速度排序战士
		'''
		self.needSort = False
		self.needSort2 = False
		wlist = []
		for side in self.teamList:
			for w in self.teamList[side].values():
				wlist.append(w)
		
		wlist.sort(key=lambda w: w.getSpeCmdAll(), reverse=True)
		return wlist
	
	def checkEnd(self):
		'''检查是否结束
		'''
		self.needCheckEnd = False
		
		if hasattr(self.game, "customCheckEnd") and self.game.customCheckEnd(): # 玩法的自定义检查结束
			return
		
		for side in (TEAM_SIDE_1, TEAM_SIDE_2): # 默认规则是挑战者全死了就算失败，哪怕被挑战者也全死了
			isEnd = True
			for w in self.teamList[side].values():
				if w.isLineupEye(): # 阵眼
					continue
				if hasattr(w, "summonIdx"): # 召唤出来的怪物
					continue
				if not w.isDead():
					isEnd = False
					break

			if isEnd:
				self.isEnd = True
				self.winner = side ^ 1
				return
			
	def checkBoutLimit(self):
		'''检查回合上限
		'''
		if hasattr(self.game, "customCheckBoutLimit") and self.game.customCheckBoutLimit(self):
			return
		
		if self.bout >= 30:
			self.isEnd = True
			self.winner = TEAM_SIDE_2
			
	def drawEnd(self):
		'''画图结束
		'''
		self.printDebugMsg("\n====================画图结束====================")
		if self.hasTimer("drawEnd"):
			self.stopTimer("drawEnd")
			
		self.handleForEscape()
			
		if self.isEnd:
			self.end()
		else:
			self.readyTurn()
			self.tryStartTurn()
			
	def setClientDrawEnd(self, w):
		'''记录回合动画播放结束的客户端
		'''
		if self.turnState != TURN_STATE_END:
			return
		self.handleForEscape()
		self.clientDrawEndList[w.getPID()] = 1
		self.tryDrawEnd()
		
	def tryDrawEnd(self):
		'''尝试画图结束，只有全部客户端播放完动画时才会成功
		'''
		for _side in self.roleList:
			for pid in self.roleList[_side]:
				who = getRole(pid)
				if not who:
					continue
				if not who.endPoint: # 已掉线
					continue
				if pid not in self.clientDrawEndList: # 还有客户端未播放完动画
					return
		
		self.drawEnd()
		
	def end(self):
		'''战斗结束
		'''
		self.printDebugMsg("\n====================战斗结束 Start====================")
		self.endTime = getSecond()

		if not war.getWarMgr().getObj(self.id):
			try:
				raise Exception("[war end]%d 战斗卡机了!!!!!!!!!!" % self.id)
			except:
				logException()
			self.endForce()
			return
		
		war.getWarMgr().removeObj(self)
		if self.hasTimer("startTurn"):
			self.stopTimer("startTurn")
		if self.hasTimer("drawEnd"):
			self.stopTimer("drawEnd")
		
		# 玩家战士，包括死亡和非死亡
		for side in self.teamList:
			for w in self.teamList[side].values():
				if not w.isRole():
					continue
				who = getRole(w.getPID())
				self.effectStatus(w, who)
		
		# 非玩家战士
		for side in self.teamList:
			for w in self.teamList[side].values():
				if w.isRole():
					continue
				if w.isPet():
					if w.isDead():
						self.kickWarrior(w)
					else:
						who = getRole(w.getPID())
						if who:
							petObj = who.petCtn.getItem(w.id)
							if petObj:
								self.effectStatus(w, petObj)
								
		self._rpcWarEnd()
		
		# 战斗结束处理
		endFunc = self.onWarEnd
		if endFunc:
			self.onWarEnd = None
			try:
				endFunc(self)
			except:
				logException()

		# 参战玩家离开战斗
		for side in self.roleList:
			for pid in self.roleList[side]:
				who = getRole(pid)
				if who:
					who.leaveWar()
					
		# 观战玩家离开战斗
		for side in self.watchRoleList:
			for pid in self.watchRoleList[side]:
				who = getRole(pid)
				if who:
					who.leaveWar()
		
# 		# 队伍离开战斗
# 		for teamInfo in self.teamInfoList.values():
# 			if not teamInfo:
# 				continue
# 			teamId = teamInfo["teamId"]
# 			if not teamId:
# 				continue
# 			teamObj = team.getTeam(teamId)
# 			if not teamObj:
# 				continue
# 			teamObj.leaveWar()

		self.release()
		self.printDebugMsg("\n====================战斗结束 End!!!!====================\n\n")
		
	def endForce(self):
		'''强制战斗结束，用于战斗卡机
		'''
		self.printDebugMsg("\n====================强制战斗结束 Start====================")

		if self.hasTimer("startTurn"):
			self.stopTimer("startTurn")
		if self.hasTimer("drawEnd"):
			self.stopTimer("drawEnd")

		self._rpcWarEnd()

		# 参战玩家离开战斗
		for side in self.roleList:
			for pid in self.roleList[side]:
				who = getRole(pid)
				if who:
					who.leaveWar()
					
		# 观战玩家离开战斗
		for side in self.watchRoleList:
			for pid in self.watchRoleList[side]:
				who = getRole(pid)
				if who:
					who.leaveWar()

		self.release()
		self.printDebugMsg("\n====================强制战斗结束 End!!!!====================\n\n")
		
	def release(self):
		for side in self.teamList:
			for w in self.teamList[side].values():
				w.release()
		for side in self.watchWarriorList:
			for w in self.watchWarriorList[side].values():
				w.release()
				
		self.roleList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}
		self.teamList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}
		self.idxList = {}
		self.watchRoleList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}
		self.watchWarriorList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}
		self.lineupList = {TEAM_SIDE_1:None, TEAM_SIDE_2:None}
		self.teamInfoList = {TEAM_SIDE_1:{}, TEAM_SIDE_2:{}}
		self.game = None
		self.gameNpc = None
		self.timerMgr.cancelAll()
	
	def calTime(self):
		'''计算时间
		'''
		if not hasattr(self,"startTime") or not hasattr(self,"endTime"):
			return 0

		return self.endTime - self.startTime

	def getRoleList(self, side=-1):
		'''获取参战玩家
		'''
		lst = []
		for _side in self.roleList:
			if side != -1 and side != _side:
				continue
			for pid in self.roleList[_side]:
				who = getRole(pid)
				if who:
					lst.append(who)
		return lst
	
	def getWatchRoleList(self, side=-1):
		'''获取观战玩家
		'''
		lst = []
		for _side in self.watchRoleList:
			if side != -1 and side != _side:
				continue
			for pid in self.watchRoleList[_side]:
				who = getRole(pid)
				if who:
					lst.append(who)
		return lst
	
	def getRoleListAll(self):
		'''获取所有玩家，包括参战、观战
		'''
		return self.getRoleList() + self.getWatchRoleList()
	
	def transDebugMsg(self, msg, att=None, vic=None):
		if "$type" in msg:
			if att.isRole():
				typeName = "玩家"
			elif att.isPet():
				typeName = "宠物"
			elif att.isBuddy():
				typeName = "伙伴"
			else:
				typeName = "怪物"
			msg = msg.replace("$type", typeName)
		return msg
	
	def printDebugMsg(self, msg, att=None, vic=None):
		'''直接输出调试信息
		'''
		import config
		if not config.IS_INNER_SERVER:
			return
		
		isPrint = False
		msg = self.transDebugMsg(msg, att, vic)
		for who in self.getRoleList():
			who.endPoint.rpcWarDebugTips(msg)
			if who.id in (111, 1611,):
				isPrint = True
				
#		if isPrint:
#			print msg
			
	def say(self, w, msg, event=0):
		'''战士说话
		'''
		for who in self.getRoleListAll():
			who.endPoint.rpcWarSay(w.idx, msg, event)
					
	def _rpcWarStart(self, target=None):
		roleList = []
		if target:
			who = getRole(target.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
		
		# 阵法
		lineupList = {}
		for side, lineupObj in self.lineupList.iteritems():
			if lineupObj:
				lineupId = lineupObj.id
			else:
				lineupId = 0
			lineupList[side] = lineupId 
			
		for who in roleList:
			w = who.warrior
			if w.isWatcher():
				args = {
					"type": self.type,
					"lineup0": lineupList[TEAM_SIDE_1],
					"lineup1": lineupList[TEAM_SIDE_2],
					"watch": True,
					"side": w.side,
				}
			else:
				args = {
					"type": self.type,
					"lineup0": lineupList[TEAM_SIDE_1],
					"lineup1": lineupList[TEAM_SIDE_2],
					"watch": False,
					"side": w.side,
					"summonNumMax": w.getSummonNumMax(),
					"summonNum": w.summonNum,
					"propsNumMax": w.getPropsNumMax(),
					"propsNum": w.propsNum,
					"autoFight": self.isAutoFight(w),
					"petIdList": self.petStat[who.id].keys(),
				}
			who.endPoint.rpcWarStart(**args)
			
	def setAutoFight(self, isAuto):
		'''设置是否自动战斗，只在第一回合生效
		'''
		self.autoFight = isAuto
			
	def isAutoFight(self, w):
		'''是否自动战斗
		'''
		autoFight = False
		if hasattr(w, "autoFight"): # 超时时系统设置的自动战斗
			autoFight = w.autoFight
		elif self.bout <= 1 and hasattr(self, "autoFight"): # 玩法设置的自动战斗只在第一回合生效
			autoFight = self.autoFight
		else: # 玩家设置的自动战斗
			who = getRole(w.getPID())
			if who:
				autoFight = who.isAutoFight()

		if autoFight:
			return True
		else:
			return False
		
	def clearAutoFightForTimeout(self, pid, refresh=True):
		'''清除超时导致的自动战斗
		'''
		who = getRole(pid)
		if not who:
			return

		w = who.warrior
		if hasattr(w, "autoFight"):
			del w.autoFight
		if refresh:
			self.rpcWarChange(w, "autoFight")
				
	def setAutoFightForTimeout(self, pid):
		'''设置超时导致的自动战斗
		'''
		who = getRole(pid)
		if not who:
			return

		w = who.warrior
		w.autoFight = True
		self.rpcWarChange(w, "autoFight")
				
	def rpcWarChange(self, target=None, *attrNameList):
		'''修改战斗信息
		'''
		roleList = []
		if target:
			who = getRole(target.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()

		for who in roleList:
			args = {}
			for attrName in attrNameList:
				if attrName in ("summonNum", "propsNum",):
					val = getattr(who.warrior, attrName)
				elif attrName in ("autoFight",):
					func = getattr(self, "is%s" % toTitle(attrName), None)
					val = func(who.warrior)
				elif attrName == "petIdList":
					val = self.petStat[who.id].keys()
				else:
					val = getValByName(self, attrName)
				args[attrName] = val
					
			who.endPoint.rpcWarChange(**args)
	
	def _rpcWarEnd(self, w=None):
		roleList = []
		if w:
			who = getRole(w.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
		
		for who in roleList:
			who.endPoint.rpcWarEnd()
				
	def rpcAddWarrior(self, w, target=None, hidden=False):
		'''增加战士
		'''
		args = {
			"idx":w.idx,
			"pid":w.id,
			"name":w.name,
			"shape":w.shape,
			"shapeParts":w.shapeParts,
			"colors":w.getColors(),
			"type":w.type,
			"side":w.side,
			"pos":w.pos,
			"level":w.level,
			"hp":w.hp,
			"hpMax":w.getHPMax(),
			"mp":w.mp,
			"mpMax":w.getMPMax(),
			"sp":w.sp,
			"spMax":w.spMax,
			"fuwen":w.fuwen,
			"fuwenMax":w.fuwenMax,
			"status":w.status,
			"hidden":hidden,
			"defaultPerform":w.getDefaultPerform(),
			"fiveEl": w.fiveElAttack,
		}
		if w.isLineupEye():
			args["performList"] = w.skillList.keys()
			args["spe"] = w.spe
		roleList = []
		if target:
			who = getRole(target.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
		
		for who in roleList:
			who.endPoint.rpcWarAddWarrior(**args)
			
	def _rpcWarDelWarrior(self, w):
		'''删除战士
		'''
		for who in self.getRoleListAll():
			who.endPoint.rpcWarDelWarrior(w.idx)
			
	def rpcWarChangeAttr(self, target=None, **args):
		roleList = []
		if target:
			who = getRole(target.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
			
		for obj in roleList:
			obj.endPoint.rpcWarChangeAttr(**args)
			
	def rpcWarAllBuff(self, w, target=None):
		'''战士buff
		'''
		roleList = []
		if target:
			who = getRole(target.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
		
		for typePos in w.buffList:
			for bfObj in w.buffList[typePos]:
				if not bfObj:
					continue

				args = {
					"idx": w.idx,
					"type": bfObj.type,
					"pos": bfObj.pos,
					"id": bfObj.id,
					"bout": bfObj.bout,
				}
				self.rpcWarBuff(roleList, **args)
					
	def rpcWarBuff(self, target=None, **args):
		'''战士buff
		'''
		roleList = []
		if target:
			if isinstance(target, list):
				roleList = target
			else:
				who = getRole(target.getPID())
				if who:
					roleList.append(who)
		else:
			roleList = self.getRoleListAll()
				
		for who in roleList:
			who.endPoint.rpcWarBuff(**args)
	
	def _rpcWarTurnReady(self, timeoutTime=0, w=None):
		'''新一轮准备，可下达指令
		'''
		roleList = []
		if w:
			who = getRole(w.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()
		
		if not timeoutTime:
			timeoutTime = self.getReadyTimeoutTime()
		for who in roleList:
			who.endPoint.rpcWarTurnReady(self.bout, timeoutTime)
			
	def getReadyTimeoutTime(self):
		'''新一轮准备的剩余时间
		'''
		timeout = TURN_TIME - (getSecond() - self.readyTime)
		return max(0, timeout)
			
	def _rpcWarTurnBegin(self, w=None):
		'''本轮开始，不可再下达指令，服务端开始结算
		'''
		roleList = []
		if w:
			who = getRole(w.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()

		for who in roleList:
			who.endPoint.rpcWarTurnBegin()
			
	def _rpcWarTurnEnd(self, w=None):
		'''本轮结束，服务端发送数据完毕，客户端开始播放动画
		'''
		if self.isEnd:
			last = 1
		else:
			last = 0
		
		roleList = []
		if w:
			who = getRole(w.getPID())
			if who:
				roleList.append(who)
		else:
			roleList = self.getRoleListAll()

		for who in roleList:
			who.endPoint.rpcWarTurnEnd(last)
			
	def _rpcWarTurnWait(self, w):
		'''等待本轮播放动画结束
		'''
		if self.isEnd:
			last = 1
		else:
			last = 0
			
		who = getRole(w.getPID())
		if who:
			who.endPoint.rpcWarTurnWait(self.bout, last)
			
	def _rpcWarSetCmd(self, w):
		'''已设置指令的战士
		'''
		for who in self.getRoleListAll():
			who.endPoint.rpcWarSetCmd(w.idx)
			
	def rpcWarWarriorStatus(self, **kwArgs):
		'''战士状态
		'''
		roleList = self.getRoleListAll()
		for who in roleList:
			who.endPoint.rpcWarWarriorStatus(**kwArgs)
			
	def rpcWarWarriorValStatus(self, **kwArgs):
		'''战士数值状态
		'''
		roleList = self.getRoleListAll()
		for who in roleList:
			who.endPoint.rpcWarWarriorValStatus(**kwArgs)
		
	def rpcWarPerform(self, w, magicId, targets=None, propsNo=0):
		'''法术攻击、物理攻击、逃跑等时播放动画
		'''
		if magicId < 100:
			magicName = war.defines.magicNameList[magicId]
		else:
			magicName = magicId
		self.drawTime += magicTimeData.getTime(magicId, w.shape)
		
		if w:
			idx = w.idx
		else:
			idx = 0
		
		if not targets:
			targets = []
		else:
			if not isinstance(targets, (list, tuple)):
				targets = [targets]
			targets = [w.idx for w in targets]

		args = {
			"idx": idx,
			"magicId": magicId,
			"targets": targets,
			"propsNo": propsNo,
		}
		
		for who in self.getRoleListAll():
			who.endPoint.rpcWarPerform(**args)
		
	def rpcWarTogetherAttack(self, atts, target):
		idxs = [w.idx for w in atts]
		args = {
			"idxs": idxs,
			"targets":target.idx,
		}
		
		for who in self.getRoleListAll():
			who.endPoint.rpcWarTogetherAttack(**args)
				
	def rpcWarCmdEnd(self, w):
		'''出招结束
		'''
		for who in self.getRoleListAll():
			who.endPoint.rpcWarCmdEnd(idx=w.idx)

	def exchangePos(self, srcW, targetW):
		'''交换位置
		'''
		if srcW.side != targetW.side:
			return
		srcW.pos,targetW.pos = targetW.pos,srcW.pos
		self.teamList[srcW.side][srcW.pos] = srcW
		self.teamList[srcW.side][targetW.pos] = targetW
		for obj in self.getRoleListAll():
			obj.endPoint.rpcWarExchangePos(srcW.idx,targetW.idx,srcW.side,targetW.pos,srcW.pos)

	def consumeEquipLifeOnWarStart(self):
		'''
		武器每10场耐久度-1，其他部位的装备每50场耐久度-1，进战斗扣除
		'''
		if hasattr(self, "noLost"):  # 无损失
			return
		for side in self.roleList:
			for pid in self.roleList[side]:
				who = getRole(pid)
				if not who:
					continue
				
				for equipObj in who.equipCtn.getAllWearEquipByValid():
					equipObj.addFightCnt(1)
					if equipObj.wearPos() == EQUIP_WEAPON:
						if equipObj.getFightCnt() >= 10:
							equipObj.addLife(-1)
							equipObj.setFightCnt(0)
					else:
						if equipObj.getFightCnt() >= 50:
							equipObj.addLife(-1)
							equipObj.setFightCnt(0)

	def consumeEquipLifeOnDie(self, who):
		'''
		战斗结束时，如果玩家处于倒地状态，则玩家身上所有装备都扣除该装备最大耐久 * 1%的耐久度
		人物等级 < 50死亡不损伤耐久
		人物等级 >= 50后，部分关卡死亡不掉耐久，这种特殊处理会在具体关卡中说明(比如竞技场、仙盟大战、服战等)
		战斗结束时，如果玩家处于倒地状态，则玩家身上所有装备都扣除该装备最大耐久 * 1%的耐久度
		'''
		if who.level < 50:
			return
		for equipObj in who.equipCtn.getAllWearEquipByValid():
			iSub = min(equipObj.getLife(), int(equipObj.maxLife()/100))
			equipObj.addLife(-iSub)
		message.tips(who,"很遗憾，直至战斗结束你都未能起身再战，身上所有装备损失#C021%#n的耐久度")
		
	def onStartWar(self, w):
		'''战斗开始时
		'''
		for func in w.getFuncList("onStartWar"):
			func(w)
		if hasattr(self.game, "onStartWar"):
			self.game.onStartWar(w)
		words.triggerEvent(w, "登场")

	def onCommand(self, w):
		'''出招时
		'''
		for func in w.getFuncList("onCommand"):
			func(w)
		if hasattr(self.game, "onCommand"):
			self.game.onCommand(w)
		if w.command in (war.commands.doPerform, war.commands.doPerformSE, war.commands.doPhyAttack,war.commands.doAI):
			words.triggerEvent(w, "出招")
			
	def isDeadEscape(self, w):
		'''死亡可否逃跑
		'''
		if not w.isRole():
			return False
		if self.isPVESingle():
			return True
		if hasattr(self, "deadEscape"):
			return True
		return False
			
	def isPVESingle(self):
		'''是否单人打怪物
		'''
		if self.type != WAR_COMMON:
			return False
		teamInfo = self.teamInfoList[TEAM_SIDE_1]
		if not teamInfo["teamId"] or teamInfo["size"] <= 1:
			return True
		return False
	
	def onSummon(self, att, vic):
		'''召唤时
		'''
		att.onSummon(vic)
		vic.onSummoned(att)
		
	def getFuncList(self, name):
		'''获取处理函数
		'''
		if name in self.funcList:
			return self.funcList[name].values()
		return []
		
	def addFunc(self, name, func, flag="flag"):
		'''增加处理函数
		'''
		import types
		if type(func) == types.MethodType: # 实例方法
			func = functor(func)

		if name not in self.funcList:
			self.funcList[name] = {}
		self.funcList[name][flag] = func
		
	def removeFunc(self, name, flag="flag"):
		'''移除处理函数
		'''
		if name in self.funcList:
			if flag in self.funcList[name]:
				del self.funcList[name][flag]
	
	def removeFuncByFlag(self, flag):
		'''根据标识移除处理函数
		'''
		for name in self.funcList.iterkeys():
			if flag in self.funcList[name]:
				del self.funcList[name][flag]


from props.defines import *
from common import *
from war.defines import *
import weakref
import timer
import war
import war.commands
import u
import magicTimeData
import pet
import time
import scene
import perform
import team
import message
import words