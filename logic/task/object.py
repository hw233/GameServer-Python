# -*- coding: utf-8 -*-
from task.defines import *
import template
import pst

class Task(template.Template, pst.cEasyPersist):
	'''单人任务
	'''

	parentId = 0  # 父任务编号
	targetType = TASK_TARGET_TYPE_NONE  # 目标类型
	icon = 0 # 图标
	title = ""  # 任务标题
	intro = ""  # 任务简介
	detail = ""  # 任务详情
	rewardDesc = "" # 奖励描述
	goAheadScript = "" # 前往脚本
	initScript = ""  # 初始化脚本

	def __init__(self, _id):
		template.Template.__init__(self)
		pst.cEasyPersist.__init__(self)
		self.id = _id
		self._ownerId = 0
		self.timerMgr = timer.cTimerMng()
		self.tmpNpcList = {}  # 临时npc,不存盘
		
	def save(self):
		npcList = {}
		for typeFlag, lst in self.npcList.iteritems():
			npcList[typeFlag] = [npcObj.save() for npcObj in lst]
		
		data = pst.cEasyPersist.save(self)
		data["eventList"] = self.eventList
		data["npcList"] = npcList
		return data
		
	def load(self, data):
		npcList = {}
		for typeFlag, lst in data.pop("npcList", {}).iteritems():
			npcList[typeFlag] = []
			for d in lst:
				npcObj = Npc(self)
				npcObj.load(d)
				npcList[typeFlag].append(npcObj)
		
		pst.cEasyPersist.load(self, data)
		self.eventList = data.pop("eventList", {})
		self.npcList = npcList
	
	@property
	def key(self):
		return self.id
	
	@property
	def ownerId(self):
		return self._ownerId
	
	@ownerId.setter
	def ownerId(self, ownerId):
		self._ownerId = ownerId
		
	def getOwnerObj(self):
		return getRole(self.ownerId)
		
	@property
	def name(self):
		return "task%05d" % self.id
	
	@property
	def logName(self):
		return "task/t%05d" % self.parentId
	
	def getTitle(self, who):
		return self.transString(self.title, who.id)
	
	def getIntro(self, who):
		return self.transString(self.intro, who.id)
	
	def getDetail(self, who):
		return self.transString(self.detail, who.id)
	
	def onBorn(self, who, npcObj, **kwargs):
		'''出生时初始化，只在给予任务时执行一次
		'''
		if self.initScript:
			self.doScript(who, npcObj, self.initScript)
		if kwargs.get("initScript"):
			self.doScript(who, npcObj, kwargs["initScript"])
# 		self.setTime(30*60) # 计时任务
		
	def setup(self, who):
		'''配置
		'''
		ti = self.getTime()
		if ti != None:
			if ti > 0:
				self.timerMgr.run(self.timeOut, ti, 0, "timeOut")
			else:
				self.timeOut()
				return
			
		if self.getAnlei():
			self.onTriggerWar = functor(self.triggerWar)  # 挂上触发暗雷函数
	
	def onLogin(self, who, reLogin):
		'''玩家登录时
		'''
		self.checkStoryPlay(who)
	
	def inGame(self, who):
		if not self.ownerId:
			return 1
		return who in self.getRoleList()
				
	def setTime(self, ti):
		self.set("endTime", getSecond() + ti)
			
	def getTime(self):
		if self.fetch("endTime"):
			return self.fetch("endTime") - getSecond()
		return None
	
	def timeOut(self):
		'''超时
		'''
		if self.timerMgr.hasTimerId("timeOut"):
			self.timerMgr.cancel("timeOut")

		who = self.getOwnerObj()
		task.removeTask(who, self.id)

		if hasattr(self, "onTimeOut"):
			self.onTimeOut()
			
	def isDone(self):
		'''是否已完成
		'''
		if self.fetch("done"):
			return True
		
		who = self.getOwnerObj()
		if self.targetType == TASK_TARGET_TYPE_ITEM: # 寻物任务
			return self.hasAllNeededProps(who)

		return False
	
	def setDone(self, isDone):
		'''设置是否已完成
		'''
		if isDone:
			self.set("done", 1)
		else:
			self.delete("done")
	
	def missionDone(self, who, npcObj):
		'''完成
		'''
		task.removeTask(who, self.id)
		template.Template.missionDone(self, who, npcObj)
		
		import listener
		for roleObj in self.getRoleList():
			listener.doListen("完成任务", roleObj, taskId=self.id, taskType=self.parentId)

	def doneEffect(self, who, npcObj, args):
		scene.playSceneEffect(who, EFFECT_TASK, who.id)
	
	def missionFail(self, who, npcObj):
		'''失败
		'''
		task.removeTask(who, self.id)
		template.Template.missionFail(self, who, npcObj)
			
	def release(self):
		'''释放
		'''
		self.timerMgr.cancelAll()
		
	def getRoleList(self):
		roleList = [self.ownerId]
		for pid in roleList:
			who = getRole(pid)
			if who:
				yield who
	
	def isValid(self):
		'''是否有效
		'''
		return 1
	
	def transString(self, content, pid=0):
		'''转化字符串
		'''
		who = None
		if pid:
			who = getRole(pid)

		# 目标npc、场景
		npcObj = self.getTargetNpc()
		if npcObj:
			if "$target" in content:
				content = content.replace("$target", "#C01{}#n".format(npcObj.name))
			if "$scene" in content:
				scObj = scene.getScene(npcObj.sceneId)
				if scObj:
					content = content.replace("$scene", "#C03{}#n".format(scObj.name))
		
		# 目标物品
		propsNeeded = self.getPropsNeeded()
		if propsNeeded:
			if "$props" in content:
				propsObjList = []
				for propsNo, amount in propsNeeded.iteritems():
					propsObjList.append(self.getPropsName(propsNo, amount))
				if propsObjList:
					content = content.replace("$props", "、".join(propsObjList))
					
# 		# 目标异兽
# 		petNeeded = self.getPetNeeded()
# 		if petNeeded:
# 			if "$pet" in content:
# 				petList = []
# 				for petIdx, amount in petNeeded.iteritems():
# 					petList.append(self.getPetName(petIdx, amount))
# 				if petList:
# 					content = content.replace("$pet", "、".join(petList))
					
		# 暗雷
		anleiList = self.getAnlei()
		if anleiList:
			if "$scene" in content:
				sceneList = []
				for d in anleiList:
					for sceneId in d["sceneList"]:
						scObj = scene.getScene(sceneId)
						if scObj:
							sceneList.append("#C02{}#n".format(scObj.name))
				if sceneList:
					content = content.replace("$scene", "、".join(sceneList))
		
		if "$quality" in content:
			content = content.replace("$quality", "#C04%s#n"%self.fetch("propsQu", 0))
		if "$process" in content:
			content = content.replace("$process", "#C04$process#n")
		return template.Template.transString(self, content, pid)
	
	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		return Npc(self)
	
	def addTempNpc(self, npcIdx, who=None):
		'''增加临时npc(不存盘),用于暗雷等
		'''
		npcObj = self.createNpc(npcIdx, who)
		self.tmpNpcList[npcObj.idx] = npcObj
		return npcObj
	
	def addNpcIdle(self, npcIdx, typeFlag="npc", who=None):
		'''增加闲人npc
		'''
		npcObj = self.addNpc(npcIdx, typeFlag, who)
		npcObj.npcType = TASK_NPC_TYPE_IDLE
		return npcObj
	
	def addNpcProps(self, npcIdx, typeFlag="npc", who=None):
		'''增加闲人npc
		'''
		npcObj = self.addNpc(npcIdx, typeFlag, who)
		npcObj.npcType = TASK_NPC_TYPE_PROPS
		return npcObj
	
	def onRemoveNpc(self, npcObj):
		'''移除npc时
		'''
		self.eventList.pop(npcObj.idx, None)
		self.markDirty()
		
	def getScriptHandler(self, script):
		for pattern, handler in gScriptHandlerList.iteritems():
			m = re.match(pattern, script)
			if not m:
				continue
			
			args = []
			for arg in m.groups():
				if isInteger(arg):
					arg = int(arg)
				elif isFloat(arg):
					arg = float(arg)
				args.append(arg)
			return handler, args

		return template.Template.getScriptHandler(self, script)
		
	def bindEvent(self, npcIdx, eventIdx):
		'''给npc绑定事件
		临时npc绑定的是idx
		'''
		template.Template.bindEvent(self, npcIdx, eventIdx)
		if hasattr(self, "markDirty"):  # 保存
			self.markDirty()
			
	def getTaskNpcList(self):
		'''任务npc
		'''
		npcList = {}
		for lst in self.npcList.itervalues():
			for npcObj in lst:
				npcList[npcObj.id] = npcObj
		return npcList
	
	def getSceneNpcList(self):
		'''任务相关的场景npc
		'''
		npcList = {}
		for npcIdx in self.eventList:
			npcObj = self.getNpcByIdx(npcIdx)
			if npcObj:
				if not isinstance(npcObj, Npc): # 非固定的场景npc(如活动npc)
					npcList[npcObj.id] = npcObj
			else:
				npcObj = npc.getNpcByIdx(npcIdx) # 固定的场景npc
				if npcObj:
					npcList[npcObj.id] = npcObj
				
		return npcList
	
	def getTargetNpc(self):
		'''目标npc
		'''
		for npcIdx in self.eventList:
			if self.isTempNpc(npcIdx):
				npcObj = self.getNpcByIdx(npcIdx)
				npcType = getattr(npcObj, "npcType", TASK_NPC_TYPE_NORMAL)
				if npcType == TASK_NPC_TYPE_IDLE: # 任务npc中的闲人不能作为任务目标
					continue
				return npcObj
			else:
				return npc.getNpcByIdx(npcIdx)
		
		return None
	
	def getGoodsNpc(self):
		'''寻物对应的商店npc
		只找还缺物品的npc
		'''
		import shop.defines
		who = self.getOwnerObj()
		for propsNo, amount in self.getPropsNeeded().iteritems():
			hasAmount = who.propsCtn.getPropsAmountByNos(propsNo)[0]
			if hasAmount < amount:
				npcObj = shop.defines.getNpcByPropsNo(propsNo)
				if not npcObj:
					npcObj = trade.getNpcByPropsNo(propsNo)
				return npcObj
		return None
	
	def quest(self, who, npcObj):
		if not self.getEventInfoByNpc(npcObj): # 没有关联事件
			return
		if not self.validDoEventScript(who, npcObj, "点击"):
			return
		
		script = self.getEventScript(who, npcObj, "点击")
		if not script:
			return
		
		self.doScript(who, npcObj, script)

		if self.targetType == TASK_TARGET_TYPE_NPC_MULTI:  # 寻多人任务
			if len(self.eventList) == 1:
				self.doEventScript(who, npcObj, "成功")
			else:
				if self.getNpcById(npcObj.id) and npcObj.npcType == TASK_NPC_TYPE_NORMAL: # 任务中的正常npc
					self.removeNpc(npcObj)
				else:
					self.bindEvent(npcObj.idx, 0)
				task.service.refreshTask(who, self)
				self.goAhead(who)
				
	def getValByName(self, attrName, who=None):
		'''根据属性名获取属性值
		'''
		if attrName in ("title", "intro", "detail"):
			func = getattr(self, "get%s" % toTitle(attrName))
			return func(who)
		return getValByName(self, attrName)
				
	def attrChange(self, *attrNameList):
		for who in self.getRoleList():
			task.service.rpcTaskChange(who, self, *attrNameList)
				
	def refresh(self):
		'''刷新任务
		'''
		for who in self.getRoleList():
			task.service.rpcTaskAdd(who, self)
	
	def abort(self, who):
		'''放弃任务
		'''
		task.removeTask(who, self.id)
		
		import listener
		listener.doListen("放弃任务", who, taskId=self.id, taskType=self.parentId)
		
	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 1

	def validDoEventScript(self, who, npcObj, key):
		if key in ("点击", "回复"):
			if who.inTeam() and not who.getTeamObj().isLeader(who.id):
				return 0
		return template.Template.validDoEventScript(self, who, npcObj, key)
	
	def goAhead(self, who):
		'''前往
		'''
		if self.isDone(): # 完成的任务会找npc回复
			self.doScript(who, None, "GNpc")
			return

		if self.targetType in (TASK_TARGET_TYPE_NPC, TASK_TARGET_TYPE_NPC_MULTI, TASK_TARGET_TYPE_COLLECT): # 寻人任务、采集任务
			self.doScript(who, None, "GNpc")
		elif self.targetType == TASK_TARGET_TYPE_ITEM: # 寻物任务
			npcObj = self.getGoodsNpc()
			if not npcObj:
				return
			if scene.isNearBy(who, npcObj, 10):
				self.doScript(who, None, "GGUI")
			else:
				self.doScript(who, None, "GGNpc")
		elif self.targetType == TASK_TARGET_TYPE_FIGHT: # 巡逻战斗
			self.doScript(who, None, "GWalk")
		else:
			if self.goAheadScript:
				self.doScript(who, None, self.goAheadScript)
				
	def autoGoAhead(self, who):
		'''自动前往
		'''
		import myGreenlet
		myGreenlet.cGreenlet.spawn(self._autoGoAhead, who.id)
		
	def _autoGoAhead(self, roleId):
		who = getRole(roleId)
		if not who:
			return
		task.goAhead(roleId, self.id)
		
	def popPetUI(self, who, npcObj):
		'''弹出上交宠物界面
		'''
		petNeeded = self.getPetNeeded()
		petIdxList = petNeeded.keys()
		
		petIdList = []
		for petObj in who.petCtn.getAllValues():
			if petObj.idx in petIdxList:
				petIdList.append(petObj.id)

		message.popPetUI(who, functor(self.responsePopPetUI, npcObj.id), "任务异兽选择", petIdList)
		
	def responsePopPetUI(self, who, petList, npcId):
		npcObj = getNpc(npcId)
		if npcObj:
			npcObj = npcObj.this()
		else:
			return
		
		petNeeded = self.getPetNeeded()
		petIdxList = petNeeded.keys()
		
		petList = []
		for petId in petList:
			petObj = who.petCtn.getItem(petId)
			if not petObj:
				message.tips(who, "你身上没有此异兽")
				return
			if petObj.idx not in petIdxList:
# 				message.tips(who, "不是所需的异兽")
				self.doEventScript(who, npcObj, "失败")
				return
			if who.petCtn.getFighter() == petObj:
				message.tips(who, "参战的异兽不能上交")
				return
			petList.append(petObj)
			
		if len(petList) != sum(petNeeded.values()):
			message.tips(who, "上交的数量不对")
			return
		
		if self.checkTakePet(who, npcObj, petList):
			for petObj in petList:
				who.petCtn.removeItem(petObj)
				writeLog("pet/lost", "%d %d %s %d at %s" % (who.id, petObj.id, petObj.idx, petObj.level, self.name))
			self.doEventScript(who, npcObj, "成功")
				
	def checkTakePet(self, who, npcObj, petList):
		'''检查上交的宠物
		'''
		return 1

	def popPropsUI(self, who, npcObj):
		'''弹出上交物品界面
		'''
		if not self.hasAllNeededProps(who):
			self.notCompleteTakeProps(who, npcObj)
			return

		propsNeeded = self.getPropsNeeded()
		propsNoListNeeded = propsNeeded.keys()
		
		propsObjList = list(who.propsCtn.getPropsGroupByNo(*propsNoListNeeded))
		propsObjList = props.tidy.sortList(propsObjList)
		propsIdList = [propsObj.id for propsObj in propsObjList]
		message.popPropsUI(who, functor(self.responsePopPropsUI, npcObj.id) , "任务物品选择", propsIdList)
	
	def responsePopPropsUI(self, who, propsList, npcId):
		npcObj = getNpc(npcId)
		if npcObj:
			npcObj = npcObj.this()
		else:
			return
		
		propsNeeded = self.getPropsNeeded()
		propsNoListNeeded = propsNeeded.keys()
		
		propsObjList = []
		propsNoListTmp = {}
		for propsId, amount in propsList.iteritems():
			propsObj = who.propsCtn.getItem(propsId)
			if not propsObj:
				message.tips(who, "你身上没有此物品")
				return
			if propsObj.idx not in propsNoListNeeded:
# 				message.tips(who, "上交的物品不对")
				self.notCompleteTakeProps(who, npcObj)
				return
			if amount > propsObj.stack():
				message.tips(who, "上交的数量不对")
				return
			propsObjList.append(propsObj)
			propsNoListTmp[propsObj.idx] = propsNoListTmp.get(propsObj.idx, 0) + amount
		
		if propsNoListTmp != propsNeeded:
			message.tips(who, "上交的数量不对")
			return
		
		if self.checkTakeProps(who, npcObj, propsObjList):
			for propsObj in propsObjList:
				amount = propsList[propsObj.id]
				who.propsCtn.addStack(propsObj, -amount)
			self.completeTakeProps(who, npcObj, propsObjList)
		else:
			self.notCompleteTakeProps(who, npcObj, propsObjList)
			
	def completeTakeProps(self, who, npcObj, propsObjList=None):
		'''上交物品成功
		'''
		self.doEventScript(who, npcObj, "成功")
		
	def notCompleteTakeProps(self, who, npcObj, propsObjList=None):
		'''上交物品失败
		'''
		self.doEventScript(who, npcObj, "失败")
				
	def checkTakeProps(self, who, npcObj, propsObjList):
		'''检查上交的物品
		'''
		return 1
	
	def hasAllNeededProps(self, who):
		'''是否有任务所需的全部物品
		'''
		for propsNo, amount in self.getPropsNeeded().iteritems():
			hasAmount = who.propsCtn.getPropsAmountByNos(propsNo)[0]
			if hasAmount < amount:
				return False
		return True
	
	def setAnlei(self, who, npcObj, npcIdx, eventIdx, sceneList):
		'''设置暗雷
		'''
		data = {}
		data["npcIdx"] = npcIdx
		data["eventIdx"] = eventIdx
		data["sceneList"] = sceneList

		anleiList = self.getAnlei()
		anleiList.append(data)
		self.set("anleiList", anleiList)
		
		self.onTriggerWar = functor(self.triggerWar)  # 挂上触发暗雷函数
		
	def getAnlei(self):
		return self.fetch("anleiList", [])
	
	def getAnleiSceneList(self):
		'''获取暗雷场景
		'''
		sceneList = []
		for data in self.getAnlei():
			sceneList.extend(data["sceneList"])
		return sceneList
	
	def isAnleiScene(self, who):
		'''是否在暗雷场景
		'''
		if who.sceneId in self.getAnleiSceneList():
			return 1
		return 0
	
	def triggerWar(self, who):
		'''触发暗雷
		'''
		sceneId = who.sceneId
		for data in self.getAnlei():
			if sceneId in data["sceneList"]:
				npcObj = self.addTempNpc(data["npcIdx"], who)
				npcObj.eventIdx = data["eventIdx"]
				self.quest(who, npcObj)
				return 1
		return 0

	def customTriggerRatio(self, who):
		'''触发暗雷
		'''
		subTime = getSecond() - who.triggerWarTime
		if subTime < 5:
			return False

		ratio = (subTime - 5) * 20 / 100
		if rand(100) < ratio:
			return True
			
		return False

	def setCallNpc(self, who, npcObj, npcList, eventIdx):
		'''设置寻找npc
		'''
		for npcIdx in npcList:
			self.bindEvent(npcIdx, eventIdx)
	
	def setPropsNeeded(self, who, npcObj, propsNo, amount):
		'''设置所需物品
		'''
		propsNoList = self.getPropsNeeded()
		propsNoList[propsNo] = amount
		self.set("propsNoList", propsNoList)
		
	def getPropsNeeded(self):
		'''所需物品
		'''
		return self.fetch("propsNoList", {})
	
	def getPropsName(self, propsNo, amount):
		propsObj = props.getCacheProps(propsNo)
		name = propsObj.name
		if amount > 1:
			name = "#C01%sx%d#n" % (name, amount)
		else:
			name = "#C01%s#n" % name
		return name
	
	def getPetName(self, petIdx, amount):
		name = pet.getPetName(petIdx)
		if amount > 1:
			name = "#C01%sx%d#n" % (name, amount)
		else:
			name = "#C01%s#n" % name
		return name
		
	def setPetNeeded(self, who, npcObj, peIdx, amount):
		'''设置所需宠物
		'''
		petList = self.getPetNeeded()
		petList[peIdx] = amount
		self.set("petList", petList)
		
	def getPetNeeded(self):
		'''所需宠物
		'''
		return self.fetch("petList", {})
	
	def pickProps(self, who, npcObj, propsNo, amount, ti=5):
		'''采集物品
		'''
		propsNeeded = self.getPropsNeeded()
		if propsNo not in propsNeeded:
			if propsNo == 0:  # 默认为任务所需物品
				propsNo = propsNeeded.keys()[0]
			else:
				return

		amountNeeded = propsNeeded[propsNo]
		if sum(who.propsCtn.getPropsAmountByNos(propsNo)) >= amountNeeded: # 数量足够了，不需要继续
			self.doEventScript(who, npcObj, "失败")
			return

		npcId = npcObj.id
		title = "采集中..."
		icon = 10002
		ti = 1
		brk = True
		message.progressBar(who, functor(self.responsePickProps, propsNo, amount, npcId), title, icon, ti, brk)

	def responsePickProps(self, who, isDone, propsNo, amount, npcId):
		if not isDone: # 中断了
			return

		npcObj = getNpc(npcId)
		if npcObj:
			npcObj = npcObj.this()
		else:
			return
		
		propsNeeded = self.getPropsNeeded()
		amountNeeded = propsNeeded[propsNo]
		amountHave = sum(who.propsCtn.getPropsAmountByNos(propsNo))
		if amountHave >= amountNeeded:
			return
		if amountHave + amount > amountNeeded:
			amount = amountNeeded - amountHave
		#launch.launchForTask(who, propsNo, amount, False, self.name)
		self.launchProps(who, int(propsNo), amount, False)
		self.doEventScript(who, npcObj, "成功")
				
	def giveNextTask(self, who, npcObj, taskId, **kwargs):
		'''给予下个任务
		'''
		self.log("%d next task %d at %d" % (who.id, taskId, self.id))
		taskObj = task.newTask(who, npcObj, taskId, **kwargs)
		if hasattr(self, "onGiveNextTask"):
			self.onGiveNextTask(who, npcObj, taskObj)
		return taskObj
	
	def giveTaskProps(self, who, npcObj, propsNo, amount):
		propsNo = int(propsNo)
		if not props.getCacheProps(propsNo).isTaskProps():
			raise Exception("任务初始化脚本时不能给予非任务物品")
		#launch.launchForTask(who, propsNo, amount, False, self.name)
		self.launchProps(who, int(propsNo), amount, False)
		
	def takePropsNeeded(self, who, npcObj):
		'''收取任务物品
		'''
		propsNeeded = self.getPropsNeeded()
		for propsNo, amount in propsNeeded.iteritems():
			if amount > sum(who.propsCtn.getPropsAmountByNos(propsNo)):
				self.notCompleteTakeProps(who, npcObj)
				return
			
		for propsNo, amount in propsNeeded.iteritems():
			who.propsCtn.subPropsByNo(propsNo, amount, self.name)
		
		self.completeTakeProps(who, npcObj)

	def getValueByVarName(self, varName, who):
		if varName == "QU":	#上交物品品质
			return getattr(self, "propsQuality", 0)
		return template.Template.getValueByVarName(self, varName, who)
			
	def storyPlay(self, who, npcObj, storyId, eventIdx=0):
		'''播放客户端剧情
		'''
		if who.inStory():
			return

		storyNpcId = 0
		if npcObj:
			storyNpcId = npcObj.id
			
		storyInfo = {
			"storyId": storyId,
			"storyEventIdx": eventIdx,
			"storyNpcId": storyNpcId,
		}
		self.set("storyInfo", storyInfo)
			
		teamObj = who.inTeam()
		if teamObj and teamObj.isLeader(who.id):
			roleList = teamObj.getInTeamList()
		else:
			roleList = [who.id]

		for roleId in roleList:
			roleObj = getRole(roleId)
			if roleObj:
				task.service.storyPlay(roleObj, self, storyId)

	def checkStoryPlay(self, roleObj):
		storyInfo = self.fetch("storyInfo")
		if not storyInfo:
			return
		if self.getOwnerObj() is not roleObj:
			return
		
		storyId = storyInfo["storyId"]
		task.service.storyPlay(roleObj, self, storyId)
		
	def responseProgressBar(self, who, isDone, npcId):
		'''进度条回应的处理
		'''
		npcObj = getNpc(npcId)
		if npcObj:
			npcObj = npcObj.this()
		else:
			return

		if isDone:
			self.completeProgressBar(who, npcObj)
		else:
			self.notCompleteProgressBar(who, npcObj)
		
	def completeProgressBar(self, who, npcObj):
		'''进度条成功
		'''
		if self.targetType == TASK_TARGET_TYPE_COLLECT: # 采集任务
			if len(self.eventList) == 1:
				self.doEventScript(who, npcObj, "成功")
			else:
				self.removeNpc(npcObj)
				task.service.refreshTask(who, self)
				self.goAhead(who)
				
	def notCompleteProgressBar(self, who, npcObj):
		'''进度条中断
		'''
		self.doEventScript(who, npcObj, "失败")


class TeamTask(Task):
	'''组队任务
	'''
	
	def __init__(self, _id):
		super(TeamTask, self).__init__(_id)
		self.roleList = []  # 任务中的玩家
		self.leaveList = []  # 离开任务的玩家
		self.team = None  # 队伍
		
	@property
	def ownerId(self):
		if self.team:
			return self.team.leader
		return 0
	
	@ownerId.setter
	def ownerId(self, ownerId):
		pass
		
	def markDirty(self):  # 不存盘
		pass
	
	def setRoleList(self, roleList):
		self.roleList = roleList[:]
		
	def setLeaveList(self, leaveList):
		self.leaveList = leaveList[:]
		
	def getRoleList(self):
		for pid in self.roleList:
			who = getRole(pid)
			if who:
				yield who
	
	def abort(self, who):
		'''放弃任务
		'''
		message.tips(who, "组队任务不可放弃")
	
	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 0
		
	def onReEnter(self, who, mode):
		'''重新进入任务
		'''
		pid = who.id
		if pid in self.roleList:
			return
# 		self.leaveList.remove(pid)
		self.roleList.append(pid)
		task.service.rpcTaskAdd(who, self)
		
		import activity.center
		activity.center.refreshTaskNpc(who)
	
	def onLeave(self, pid, mode):
		'''离开任务
		'''
		if pid not in self.roleList:
			return
# 		self.leaveList.append(pid)
		self.roleList.remove(pid)
		import activity.center
		who = getRole(pid)
		if who:
			task.service.rpcTaskDel(who, self)
			activity.center.refreshTaskNpc(who)


import npc.object

class Npc(npc.object.NpcBase):
	'''任务npc
	'''
	
	def __init__(self, gameObj):
		npc.object.NpcBase.__init__(self)
		self.game = weakref.proxy(gameObj)
		self.npcType = TASK_NPC_TYPE_NORMAL # 任务npc类型
		self.typeFlag = "npc"

	def save(self):
		data = {}
		data["name"] = self.name
		data["shape"] = self.shape
		data["shapeParts"] = self.shapeParts
		data["colors"] = self.getColors()
		data["idx"] = self.idx
		data["sceneId"] = self.sceneId
		data["x"] = self.x
		data["y"] = self.y
		data["d"] = self.d
		data["npcType"] = self.npcType
		data["title"] = self.title
		if self.action:
			data["action"] = self.action
		if hasattr(self, "school"):
			data["school"] = self.school
		if self.effectId:
			data["effectId"] = self.effectId
		return data
		
	def load(self, data):
		self.name = data["name"]
		self.shape = data["shape"]
		self.shapeParts = data.get("shapeParts", self.shapeParts)
		self.colors = data.get("colors", self.colors)
		self.idx = data["idx"]
		self.sceneId = data["sceneId"]
		self.x = data["x"]
		self.y = data["y"]
		self.d = data["d"]
		if "npcType" in data:
			self.npcType = data["npcType"]
		if "title" in data:
			self.title = data["title"]
		if "action" in data:
			self.action = data["action"]
		if "school" in data:
			self.school = data["school"]
		if "effectId" in data:
			self.effectId = data["effectId"]

#===============================================================================
# 脚本处理
#===============================================================================
def handleTakeProps(gameObj, who, npcObj, *args):
	'''收取任务物品
	'''
	gameObj.takePropsNeeded(who, npcObj)
	
def handleAnlei(gameObj, who, npcObj, npcIdxStr, eventIdxStr, sceneListStr):
	'''设置暗雷
	'''
	npcIdx = gameObj.transIdxByGroup(int(npcIdxStr))
	eventIdx = gameObj.transIdxByGroup(int(eventIdxStr))
	
	sceneList = []
	for sceneId in sceneListStr.split("&"):
		if sceneId == "guild":
			guildObj = who.getGuildObj()
			sceneId = guildObj.scene.id
		else:
			sceneId = gameObj.transIdxByGroup(int(sceneId))
		sceneList.append(sceneId)
	
	gameObj.setAnlei(who, npcObj, npcIdx, eventIdx, sceneList)

def handleCall(gameObj, who, npcObj, *args):
	'''设置寻找npc
	'''
	npcList = gameObj.getGroupInfo(int(args[0]))
	eventIdx = gameObj.transIdxByGroup(int(args[1]))
	count = int(args[2])
	npcList = shuffleList(npcList, count)
	gameObj.setCallNpc(who, npcObj, npcList, eventIdx)
	
def handleGiveNextTask(gameObj, who, npcObj, taskId):
	'''给予下个任务
	'''
	gameObj.giveNextTask(who, npcObj, taskId)
	
def handleGiveNextCustomTask(gameObj, who, npcObj, taskId, eventIdx):
	'''给予下个任务(自定义初始化)
	'''
	eventIdx = gameObj.transIdxByGroup(eventIdx)
	info = gameObj.getEventInfo(eventIdx)
	initScript = info["点击"]
	gameObj.giveNextTask(who, npcObj, taskId, initScript=initScript)
	
def handleSetPropsNeeded(gameObj, who, npcObj, *args):
	'''设置所需物品
	'''
	propsNo, amount  = [int(arg) for arg in args]
	propsNo = gameObj.transIdxByGroup(propsNo)
	gameObj.setPropsNeeded(who, npcObj, propsNo, amount)
	
def handleSetPetNeeded(gameObj, who, npcObj, *args):
	'''设置所需宠物
	'''
	petIdx, amount  = [int(arg) for arg in args]
	petIdx = gameObj.transIdxByGroup(petIdx)
	gameObj.setPetNeeded(who, npcObj, petIdx, amount)
	
def handleGiveTaskProps(gameObj, who, npcObj, *args):
	'''给予任务物品
	'''
	propsNo, amount = [int(arg) for arg in args]
	gameObj.giveTaskProps(who, npcObj, propsNo, amount)

def handleAddNpcIdle(gameObj, who, npcObj, *args):
	'''增加闲人npc
	'''
	npcIdx = gameObj.transIdxByGroup(int(args[0]))
	return gameObj.addNpcIdle(npcIdx, who=who)

def handleAddNpcIdleAndBindEvent(gameObj, who, npcObj, *args):
	'''增加闲人npc并绑定事件
	'''
	npcIdx, eventIdx = args
	npcObjAdded = handleAddNpcIdle(gameObj, who, npcObj, npcIdx)
	npcIdx = str(npcObjAdded.idx)
	template.handleBindEvent(gameObj, who, npcObj, npcIdx, eventIdx)

def handleAddNpcProps(gameObj, who, npcObj, *args):
	'''增加地上物品npc
	'''
	npcIdx = gameObj.transIdxByGroup(int(args[0]))
	return gameObj.addNpcProps(npcIdx, who=who)
	
def handleAddNpcPropsAndBindEvent(gameObj, who, npcObj, *args):
	'''增加地上物品npc并绑定事件
	'''
	npcIdx, eventIdx = args
	npcObjAdded = handleAddNpcProps(gameObj, who, npcObj, npcIdx)
	npcIdx = str(npcObjAdded.idx)
	template.handleBindEvent(gameObj, who, npcObj, npcIdx, eventIdx)
	
def handleStoryPlay(gameObj, who, npcObj, storyId, eventIdx=0):
	'''播放客户端剧情
	'''
	storyId = int(storyId)
	eventIdx = int(eventIdx)
	gameObj.storyPlay(who, npcObj, storyId, eventIdx)

def goAheadNpc(taskObj, who, npcObj, *args):
	'''前往找Npc
	'''
	targetNpcObj = taskObj.getTargetNpc()
	
	sceneIdTarget = targetNpcObj.sceneId
	if who.sceneId != sceneIdTarget and getattr(taskObj, "canTransfer", True): # 不在目标场景，先传送过去
		if not scene.tryTransfer(who, sceneIdTarget, None, None):
			return

	msgObj = task_pb2.goAheadNpc()
	msgObj.taskId = taskObj.id
	msgObj.sceneId = sceneIdTarget
	msgObj.x = targetNpcObj.x
	msgObj.y = targetNpcObj.y
	msgObj.npcId = targetNpcObj.id
	who.endPoint.rpcTaskGoAheadNpc(msgObj)
	
def goAheadGoodsNpc(taskObj, who, npcObj, *args):
	'''前往找商店npc
	'''
	npcObj = taskObj.getGoodsNpc()
	if not npcObj:
		return
	
	sceneIdTarget = npcObj.sceneId
	if who.sceneId != sceneIdTarget: # 不在目标场景，先传送过去
		if not scene.tryTransfer(who, sceneIdTarget, None, None):
			return
	msgObj = task_pb2.goAheadPos()
	msgObj.taskId = taskObj.id
	msgObj.sceneId = sceneIdTarget
	msgObj.x = npcObj.x
	msgObj.y = npcObj.y
	msgObj.npcId = npcObj.id
	who.endPoint.rpcTaskGoAheadPos(msgObj)
	
def goAheadGoodsUI(taskObj, who, npcObj, *args):
	'''打开商店界面
	'''
	import shop
	npcObj = taskObj.getGoodsNpc()
	if not npcObj:
		return
	if npcObj.kind == "商店":
		shop.openShop(who, npcObj.idx, taskObj.id)
	elif npcObj.kind == "交易":
		trade.openTradeCenter(who, taskObj)
	
def goAheadWalk(taskObj, who, npcObj, *args):
	'''巡逻
	'''
	sceneList = taskObj.getAnleiSceneList()
	if sceneList:
		scene.walkGuard(who, sceneList[0])

def setQuality(taskObj, who, npcObj, *args):
	'''设置物品所需品质
	'''
	taskObj.setQuality(who, npcObj, args)

def doneEffect(taskObj, who, npcObj, *args):
	'''任务完成特效
	'''
	taskObj.doneEffect(who, npcObj, args)

def handleProgressBar(taskObj, who, npcObj, title, icon=0, ti=1, brk=1):
	'''进度条
	'''
	icon = int(icon)
	ti = int(ti)
	brk = int(brk)
	if brk:
		brk = True
	else:
		brk = False
	npcId = npcObj.id
	message.progressBar(who, functor(taskObj.responseProgressBar, npcId), title, icon, ti, brk)


# 脚本处理函数
gScriptHandlerList = {
	"TAKE": handleTakeProps,
	"ANLEI\((\S+),(\S+),(\S+)\)": handleAnlei,
	"CALL\((\S+),(\S+),(\S+)\)": handleCall,
	"T(\d+)": handleGiveNextTask,
	"T\((\d+),(\d+)\)": handleGiveNextCustomTask,
	"L\((\S+),(\S+)\)": handleSetPropsNeeded,
# 	"C\((\S+),(\S+)\)": handleSetPetNeeded,
	"I\((\S+),(\S+)\)": handleGiveTaskProps,
	"NI(\d+)": handleAddNpcIdle,
	"NIE\((\S+),(\S+)\)": handleAddNpcIdleAndBindEvent,
	"NP(\d+)": handleAddNpcProps,
	"NPE\((\S+),(\S+)\)": handleAddNpcPropsAndBindEvent,
	"GNpc": goAheadNpc,
	"GGNpc": goAheadGoodsNpc,
	"GGUI": goAheadGoodsUI,
	"GWalk": goAheadWalk,
	"QU(\d+)": setQuality,
	"STORY(\d+)": handleStoryPlay,
	"STORY\((\d+),(\d+)\)": handleStoryPlay,
	"DEFF":doneEffect,
	"PB\((\S+),(\S+),(\S+),(\S+)\)":handleProgressBar,
}

import types
from common import *
from scene.defines import *
from task.defines import *
import weakref
import message
import re
import timer
import random
import npc
import task
import scene
import props
import props.tidy
import task_pb2
import task.service
import pet
import launch
import endPoint
import trade