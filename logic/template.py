# -*- coding: utf-8 -*-
import shapePartScope

NpcDirList = [2, 4, 6, 8] # npc面向

class Template(object):
	'''任务、活动、副本等的模板
	'''
	
	chatInfo = {}  # 对白表
	
	rewardInfo = {}  # 普通奖励表
	rewardPropsInfo = {}  # 物品奖励表
	
	fightInfo = {}  # 战斗表
	ableInfo = {}  # 能力表
	lineupInfo = {} # 阵法表
	
	npcInfo = {}  # npc表
	sceneInfo = {}  # 场景表
	
	eventInfo = {}  # 事件表
	groupInfo = {}  # 分组表
	branchInfo = {}  # 分支脚本表
	configInfo = {}  # 配置表
	
	def __init__(self):
		self.npcList = {}  # npc对象列表
		self.eventList = {}  # npc对应事件
		self.sceneList = {} # 场景对象列表
		self.tmpReward = {} # 临时记录玩家奖励

	def getRefObj(self):
		'''关联对象
		'''
		return self
	
	@property
	def name(self):
		raise NotImplementedError("请在子类实现")
	
	@property
	def logName(self):
		raise NotImplementedError("请在子类实现")
	
	def log(self, content):
		writeLog(self.logName, content)
	
	def getChatInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().chatInfo
		return self.getRefObj().chatInfo[idx]
	
	def getRewardInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().rewardInfo
		return self.getRefObj().rewardInfo[idx]
	
	def getRewardPropsInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().rewardPropsInfo
		return self.getRefObj().rewardPropsInfo[idx]
	
	def getFightInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().fightInfo
		return self.getRefObj().fightInfo[idx]
	
	def getAbleInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().ableInfo
		return self.getRefObj().ableInfo[idx]
	
	def getLineupInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().lineupInfo
		return self.getRefObj().lineupInfo[idx]
	
	def getNpcInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().npcInfo
		return self.getRefObj().npcInfo[idx]
	
	def getSceneInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().sceneInfo
		return self.getRefObj().sceneInfo[idx]
	
	def getEventInfo(self, eventIdx):
		return self.getRefObj().eventInfo.get(eventIdx)

	def getEventInfoByNpc(self, npcObj):
		'''根据npc获取事件
		'''
		eventIdx = self.getEventIdxByNpc(npcObj)
		return self.getRefObj().eventInfo.get(eventIdx)
	
	def getEventIdxByNpc(self, npcObj):
		'''根据npc获取事件编号
		'''
		if not npcObj:
			return 0
		if hasattr(npcObj, "eventIdx"):  # 给npc自定义的事件id
			eventIdx = npcObj.eventIdx
		else:
			eventIdx = self.eventList.get(npcObj.idx, 0)
		return eventIdx
	
	def getText(self, chatIdx, pid=0):
		return self.transString(self.getChatInfo(chatIdx), pid)
	
	def getGroupInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().groupInfo
		return self.getRefObj().groupInfo.get(idx)
	
	def transIdxByGroup(self, idx):
		'''根据分组表转换
		如果不存在，而原值返回
		'''
		if isinstance(idx, str):
			if not idx.isdigit():
				return idx
			idx = int(idx)

		lst = self.getGroupInfo(idx)
		if lst:
			return lst[rand(len(lst))]
		return idx
	
	def getBranchInfo(self, idx=-1):
		if idx == -1:
			return self.getRefObj().branchInfo
		return self.getRefObj().branchInfo[idx]
	
	def getConfigInfo(self, key=None):
		if key is None:
			return self.getRefObj().configInfo
		return self.getRefObj().configInfo[key]
	
	def transString(self, content, pid=0):
		'''转化字符串
		'''
		who = None
		if pid:
			who = getRole(pid)
			if pid in self.tmpReward:
				if self.tmpReward[pid].get("物品") and "$lnkProps" in content:
					linkMsgList = self.tmpReward[pid]["物品"]
					content = content.replace("$lnkProps", "、".join(linkMsgList))

		if who:
			if "$roleName" in content:
				content = content.replace("$roleName", who.name)
			if "$roleLV" in content:
				content = content.replace("$roleLV", str(who.level))

		return content
	
	def inGame(self, who):
		'''是否在活动或任务中
		'''
		return 1
	
	def transCode(self, code, _type="", who=None):
		'''数值转化公共接口
		'''
		if isinstance(code, str): # 字符串公式
			if who:
				if "ALV" in code:
					teamObj = who.inTeam()
					if teamObj:
						level = teamObj.getAvgLV()
					else:
						level = who.level
					code = code.replace("ALV", str(level))
				elif "PLV" in code:
					petObj = who.getLastFightPet()
					petLv = petObj.level if petObj else 0
					code = code.replace("PLV", str(petLv))
				elif "LV" in code:
					code = code.replace("LV", str(who.level))
			return code
		if type(code) == types.FunctionType: #lambda函数，如:lambda LV:LV*20+100
			func = code
			params=[]
			for varName in func.func_code.co_varnames:
				varVal = self.getValueByVarName(varName, who)
				params.append(varVal)
			return func(*params)
		
		return code
	
	def getValueByVarName(self, varName, who):
		if who:
			if varName == "LV":
				return who.level
			if varName == "ALV":
				teamObj = who.inTeam()
				if teamObj:
					return teamObj.getAvgLV()
				return who.level
			if varName == "MLV":
				teamObj = who.inTeam()
				if teamObj:
					return teamObj.getMaxLV()
				return who.level
			if varName == "PLV":
				petObj = who.getLastFightPet()
				if petObj:
					return petObj.level
				return 0
			
		raise Exception,'策划填的变量{}无法解析.'.format(varName)


#===============================================================================
# 奖励相关
#===============================================================================
	
	def reward(self, who, rwdIdx, npcObj=None):
		'''奖励
		'''
		self.tmpReward[who.id] = {}
		self.initTmpReward(who.id)

		if not self.validReward(who, rwdIdx, npcObj):
			return

		self.log("%d reward %d" % (who.id, rwdIdx))
		info = self.getRewardInfo(rwdIdx)
		rewardList=[]
		for _type in info.iterkeys():
			if _type in ("传闻",):
				continue
			if _type == "经验":
				rewardList.insert(0,_type)
			else:
				rewardList.append(_type)
				
		for _type in rewardList:
			val = info[_type]
			if not val:
				continue
			val = self.transCodeForReward(val, _type, who)
			self.rewardByType(who, val, _type)
			
		if info.get("传闻"):
			scriptStr = info["传闻"]
			if scriptStr.isdigit():
				scriptStr = "SM{}".format(scriptStr)
			self.doScript(who, None, scriptStr)
		
	def validReward(self, who, rwdIdx, npcObj):
		'''检查是否可奖励
		'''
		return True
		
	def rewardTeam(self, who, rwdIdx, npcObj=None):
		'''奖励队伍
		'''
		teamObj = who.getTeamObj()
		if teamObj:
			lst = teamObj.getInTeamList()
		else:
			lst = [who.id]

		for pid in lst:
			obj = getRole(pid)
			if obj:
				self.reward(obj, rwdIdx, npcObj)
				
	def transCodeForReward(self, code, _type="", who=None):
		'''转化奖励
		'''
		return self.transCode(code, _type, who)
	
	def rewardByType(self, who, val, _type):
		'''根据类型奖励
		'''
		roleId = who.id
		self.initTmpReward(roleId)

		if isinstance(val, str):
			if "," in val:
				val = [int(s) for s in val.split(",")]
			else:
				val = int(eval(val))
		elif isinstance(val, float):
			val = int(val)
			
		if _type == "经验":
			self.rewardExp(who, val)
		elif _type == "宠物经验":
			self.rewardPetExp(who, val)
		elif _type == "银币":
			self.rewardCash(who, val)

		elif _type == "物品":
			if isinstance(val, list):
				rwdIdxList = val
			else:
				rwdIdxList = [val,]
			for rwdIdx in rwdIdxList:
				self.rewardProps(who, rwdIdx)
		elif _type == "宠物":
			self.rewardPet(who, val)
			self.tmpReward[roleId][_type].append(val)
		elif _type == "活跃点":
			who.addActPoint(val, self.name)
	
	def rewardProps(self, who, rwdIdx, total=0):
		'''奖励物品
		'''
		infoList = self.getRewardPropsInfo(rwdIdx)
		info = self.randRightInfo(infoList, total=total)
		if not info:
			return

		propsNo, args, kwargs = misc.parseItemInfo(info["物品"])
		amount = int(self.transCodeForReward(info["数量"], "数量", who))
		binded = info.get("绑定", 0)
		propsNo = str(self.transIdxByGroup(propsNo))
		if not hasattr(self, "customRewardProps") or not self.customRewardProps(who, propsNo, amount, binded, *args, **kwargs):
			self.launchProps(who, int(propsNo), amount, binded)
		
		if info.get("传闻"):
			scriptStr = info["传闻"]
			if scriptStr.isdigit():
				scriptStr = "SM{}".format(scriptStr)
			self.doScript(who, None, scriptStr)
			
	def randRightInfo(self, infoList, total=0):
		'''随机有权重的数据
		'''
		idx = chooseKey(infoList, total=total, key="权重")
		if idx is None:
			return None

		info = infoList[idx]
		if info.get("物品", None) in ("", "0",):
			return None

		return info
			
	def launchProps(self, who, propsNo, amount, binded):
		roleId = who.id
		self.initTmpReward(roleId)

		lastRewardProps = None
		propsList = self.createProps(propsNo, amount, binded)
		for propsObj in propsList:
			launch.launchProps(who, propsObj, self.name)
			if not propsObj.isVirtual():
				lastRewardProps = propsObj
			
		if lastRewardProps:
			linkMsg = lastRewardProps.getHyperLink()
			msg = "获得{}".format(linkMsg)
			if amount > 1:
				linkMsg = "{}×{}".format(linkMsg, amount)
				msg = "{}#C02×{}#n".format(msg, amount)
			self.tmpReward[roleId]["物品"].append(linkMsg)
			message.message(who, msg)
			
	def createProps(self, propsNo, amount, binded):
		propsList = []
		while amount > 0:
			stack = amount
			propsObj = props.new(propsNo)
			if propsObj.isVirtual(): # 虚拟物品
				propsObj.setValue(stack)
				propsList.append(propsObj)
				break

			stackMax = propsObj.maxStack()
			if stack > stackMax:
				stack = stackMax
			propsObj.setStack(stack)
			amount -= stack
			if binded and not propsObj.isBind():
				propsObj.bind()
			propsList.append(propsObj)
			
		return propsList

	def rewardExp(self, who, val):
		'''奖励角色经验
		'''
		roleId = who.id
		who.rewardExp(val, self.name)
		self.tmpReward[roleId]["经验"].append(val)

	def rewardCash(self, who, val):
		'''奖励银币
		'''
		roleId = who.id
		who.rewardCash(val, self.name)
		self.tmpReward[roleId]["银币"].append(val)

	def rewardPetExp(self, who, val):
		'''奖励宠物经验
		'''
		roleId = who.id
		petObj = who.getLastFightPet()
		if petObj:
			petObj.rewardExp(val, self.name)
		self.tmpReward[roleId]["宠物经验"].append(val)

	def rewardPet(self, who, petId):
		petObj = pet.new(petId, 1)
		if petObj:
			pet.addPet(who, petObj)
			
	def initTmpReward(self, roleId):
		'''初始化临时奖励信息
		'''
		if roleId not in self.tmpReward:
			self.tmpReward[roleId] = {}
		for _type in ("经验", "宠物经验", "银币", "物品", "宠物", "活跃点"):
			if _type not in self.tmpReward[roleId]:
				self.tmpReward[roleId][_type] = []
				
	def rewardByMail(self, roleId, rwdIdx, title, content):
		'''邮件奖励
		'''
		import resume
		roleObj = getRole(roleId)
		if not roleObj:
			roleObj = resume.getResume(roleId)
			if not roleObj:
				return

		infoList = self.getRewardPropsInfo(rwdIdx)
		if infoList[0]["权重"] != 1000: # 需要计算权重
			info = self.randRightInfo(infoList)
			if not info:
				return
			infoList = [info,]
		
		propsList = []
		for info in infoList:
			amount = int(self.transCodeForReward(info["数量"], "数量", roleObj))
			binded = info.get("绑定", 0)
			propsNo = self.transIdxByGroup(info["物品"])
			propsList.extend(self.createProps(propsNo, amount, binded))
		
		import mail
		mail.sendSysMail(roleId, title, content, propsList)
		

#===============================================================================
# 战斗相关	
#===============================================================================

	def newWar(self, who, fightIdx=None):
		'''新建战斗
		'''
		return None
	
	def fight(self, who, npcObj, fightIdx):
		'''战斗
		'''
		if who.inWar():
			return None
		if not self.validFight(who, npcObj, fightIdx):
			return None
		
		fightList = self.getFightInfo(fightIdx)
		return war.warctrl.createCommonWar(who, fightIdx, fightList, self.getAbleInfo(), self.getLineupInfo(), self, npcObj)
	
	def validFight(self, who, npcObj, fightIdx):
		return 1
	
	def fightSingle(self, who, npcObj, fightIdx):
		'''独占式战斗，用于活动npc
		'''
		warObj = self.fight(who, npcObj, fightIdx)
		if warObj:
			npcObj.enterWar(warObj)
		return warObj
	
	def transAbleInfo(self, who, fightIdx, ableInfo, npcObj=None):
		'''转化怪物能力表数据
		'''
		result = {}
		for _type, code in ableInfo.iteritems():
			result[_type] = self.transCodeForFight(code, _type, who)
		return result
	
	def transCodeForFight(self, code, _type="", who=None):
		'''转化战斗数据
		'''
		return self.transCode(code, _type, who)


#===============================================================================
# npc相关
#===============================================================================
	def addNpc(self, npcIdx, typeFlag="npc", who=None):
		'''增加npc
		'''
		npcObj = self.createNpc(npcIdx, who)
		npcObj.typeFlag = typeFlag
		if typeFlag not in self.npcList:
			self.npcList[typeFlag] = []
		self.npcList[typeFlag].append(npcObj)
		return npcObj

	def createNpc(self, npcIdx, who=None):
		'''创建Npc
		'''
		if not self.isTempNpc(npcIdx):
			raise Exception("创建临时npc时，使用了非法的编号:%d" % npcIdx)
		
		info = copy.deepcopy(self.getNpcInfo(npcIdx))
		info = self.transNpcInfo(npcIdx, info, who)
		name = info["名称"]
		shape = info["造型"]
		shapeParts = info["造型部位"]
		
		npcObj = self.newNpc(npcIdx, name, shape, who)
		npcObj.name = name
		npcObj.shape = shape
		npcObj.shapeParts = shapeParts
		if info.get("染色"):
			npcObj.colors = info["染色"]
		if info.get("动作"):
			npcObj.action = info["动作"]
		if info.get("特效"):
			npcObj.effectId = info["特效"]
		npcObj.idx = npcIdx
		self.lastNewNpcId = npcObj.id

		sceneId, x, y, d = info["位置"]
		npcObj.sceneId = self.transSceneId(sceneId)
		if x == 0 or y == 0:
			x, y = scene.randSpace(sceneId)
		if d == 0:
			d = NpcDirList[rand(len(NpcDirList))]
		npcObj.x = x
		npcObj.y = y
		npcObj.d = d
		
		if info.get("称谓"):
			npcObj.title = info["称谓"]
		return npcObj
		
	def transNpcInfo(self, npcIdx, info, who=None):
		'''转化Npc信息
		'''
		shape, shapeParts = transShapeStr(info["造型"], who)
		info["造型"] = shape
		info["造型部位"] = shapeParts
		
		if info.get("染色"):
			colors = transColorsStr(info["染色"], who)
			info["染色"] = colors
		
		name = info["名称"]
# 		if "$pet" in name:
# 			name = name.replace("$pet", pet.getPetName(shape))
		info["名称"] = name

		if "$mypos" in info["位置"]:
			sceneId, x, y, d =  who.sceneId, who.x, who.y, 0
		else:
			posList = info["位置"].split("|")
			pos = posList[rand(len(posList))]
			m = re.match("(\S+),(\S+),(\S+),(\S+)", pos)
			sceneId = m.group(1)
			if sceneId == "guild":
				guildObj = who.getGuildObj()
				sceneId = guildObj.scene.id
			else:
				sceneId = int(sceneId)
			x = int(m.group(2))
			y = int(m.group(3))
			d = int(m.group(4))
		info["位置"] = [sceneId, x, y, d]
		
		return info
	
	def transSceneId(self, sceneId):
		'''转化场景Id
		'''
		if hasattr(self.getRefObj(), "getSceneByIdx"):
			sceneObj = self.getRefObj().getSceneByIdx(sceneId)
			if sceneObj:
				return sceneObj.id
		return sceneId

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		raise NotImplementedError("请在子类实现")
	
	def removeNpc(self, npcObj):
		'''移除npc
		'''
		typeFlag = npcObj.typeFlag
		npcList = self.npcList.get(typeFlag, [])
		if npcObj not in npcList:
			return

		npcList.remove(npcObj)
		if len(npcList) == 0:
			del self.npcList[typeFlag]
		else:
			self.npcList[typeFlag] = npcList
		self.onRemoveNpc(npcObj)

	def removeNpcByTypeFlag(self, typeFlag):
		'''根据类型标识移除npc
		'''
		npcList = self.npcList.pop(typeFlag, [])
		for npcObj  in npcList:
			self.onRemoveNpc(npcObj)

	def onRemoveNpc(self, npcObj):
		'''移除npc时
		'''
		pass
	
	def getNpcByIdx(self, npcIdx):
		'''根据npc导表编号获取npc
		'''
		for lst in self.npcList.itervalues():
			for npcObj in lst:
				if npcObj.idx == npcIdx:
					return npcObj
		return None
	
	def getNpcById(self, npcId):
		'''根据npc的id获取npc
		'''
		for lst in self.npcList.itervalues():
			for npcObj in lst:
				if npcObj.id == npcId:
					return npcObj
		return None
	
	def getNpcListByType(self, typeFlag):
		'''根据类型标识获取npc列表
		'''
		return self.npcList.get(typeFlag, [])
	
	def bindEvent(self, npcIdx, eventIdx):
		'''给npc绑定事件
		临时npc绑定的是idx
		'''
		if npcIdx == 0:  # 当前npc
			npcObj = self.getCurrentNpc()
			if not npcObj:
				raise Exception("绑定事件时，找不到当前npc")
			npcIdx = npcObj.idx
		elif npcIdx == 1: # 最新创建的npc
			npcObj = self.getLastNewNpc()
			if not npcObj:
				raise Exception("绑定事件时，找不到最新创建的npc")
			npcIdx = npcObj.idx

		if eventIdx:
			if self.isTempNpc(npcIdx) and not self.getNpcByIdx(npcIdx):
				raise Exception("绑定事件时，使用了非法的临时npc编号:%d" % npcIdx)
			self.eventList[npcIdx] = eventIdx
		else:
			if npcIdx in self.eventList:
				del self.eventList[npcIdx]
			
	def isTempNpc(self, npcIdx):
		'''是否临时npc
		'''
		return npcIdx < 10000

#===============================================================================
# 场景相关
#===============================================================================

	def createScene(self, sceneIdx):
		'''创建虚拟场景
		'''
		info = self.getSceneInfo(sceneIdx)
		sceneObj = scene.new("活动", 0, info["名称"], info["资源"], info.get("小地图资源", 0))
		sceneObj.idx = sceneIdx
		return sceneObj
	
	def addScene(self, sceneIdx, typeFlag="scene"):
		'''增加场景
		'''
		sceneObj = self.createScene(sceneIdx)
		sceneObj.typeFlag = typeFlag
		if typeFlag not in self.sceneList:
			self.sceneList[typeFlag] = []
		self.sceneList[typeFlag].append(sceneObj)
		return sceneObj
	
	def removeScene(self, sceneObj):
		'''移除场景
		'''
		typeFlag = sceneObj.typeFlag
		sceneList = self.sceneList.get(typeFlag)
		if not sceneList:
			return
		if sceneObj not in sceneList:
			return
		sceneList.remove(sceneObj)
		if len(sceneList) == 0:
			del self.sceneList[typeFlag]
		else:
			self.sceneList[typeFlag] = sceneList
		self.onRemoveScene(sceneObj)
		
	def removeSceneByTypeFlag(self, typeFlag):
		'''根据类型标识移除场景
		'''
		sceneList = self.sceneList.pop(typeFlag, [])
		for sceneObj in sceneList:
			self.onRemoveScene(sceneObj)
			
	def removeSceneAll(self):
		'''移除全部场景
		'''
		sceneList = self.sceneList
		self.sceneList = {}
		for typeFlag in sceneList:
			for sceneObj in sceneList[typeFlag]:
				self.onRemoveScene(sceneObj)
			
	def onRemoveScene(self, sceneObj):
		'''移除场景时
		'''
		sceneObj.release()
		
	def getSceneByIdx(self, sceneIdx):
		'''根据场景导表编号获取场景
		'''
		for sceneList in self.sceneList.itervalues():
			for sceneObj in sceneList:
				if sceneObj.idx == sceneIdx:
					return sceneObj
				
		return None
	
	def getSceneListByType(self, typeFlag):
		'''根据类型标识获取场景列表
		'''
		return self.sceneList.get(typeFlag, [])
	
#===============================================================================
# 战斗相关
#===============================================================================
	def onWarWin(self, warObj, npcObj, w):
		'''战斗胜利时
		'''
		who = getRole(w.id)
		if who and npcObj:
			self.doEventScript(who, npcObj, "成功")
	
	def onWarFail(self, warObj, npcObj, w):
		'''战斗失败时
		'''
		who = getRole(w.id)
		if who and npcObj:
			self.doEventScript(who, npcObj, "失败")
	
	def onEscaped(self, warObj, npcObj, w):
		'''逃跑成功时
		'''
		self.onWarFail(warObj, npcObj, w)
	
	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利
		'''
		for w in warriorList:
			if not w.isRole():
				continue
			who = getRole(w.id)
			if not who:
				continue
			if not self.inGame(who):
				continue

			self.onWarWin(warObj, npcObj, w)
			break
	
	def warFail(self, warObj, npcObj, warriorList):
		'''战斗失败
		'''
		for w in warriorList:
			if w.isRole():
				self.onWarFail(warObj, npcObj, w)

	def beforeWarEnd(self, warObj, npcObj):
		'''战斗结束前
		'''
		pass
	
	def warEnd(self, warObj, npcObj):
		'''战斗结束
		'''
		pass
	
	def onAddWarrior(self, w):
		'''增加战士时
		'''
		pass
	
#===============================================================================
# 脚本相关
#===============================================================================
	def getCurrentNpc(self):
		'''获取当前npc
		'''
		if hasattr(self, "currentNpcId"):
			return getNpc(self.currentNpcId)
		return None
	
	def getLastNewNpc(self):
		'''获取最新创建的npc
		'''
		if hasattr(self, "lastNewNpcId"):
			return getNpc(self.lastNewNpcId)
		return None

	def doScript(self, who, npcObj, scripts):
		'''解释脚本
		'''
		if not self.inGame(who):
			return
		if npcObj:
			npcObj = npcObj.this()
		for script in re.findall("[\w\$]+\([^()]+\)|[\w\$]+", scripts):
			self.executeScript(who, npcObj, script)

	def executeScript(self, who, npcObj, script):
		'''执行脚本
		'''
		if npcObj:
			self.currentNpcId = npcObj.id
		handler, args = self.getScriptHandler(script)
		if handler:
			handler(self, who, npcObj, *args)
		else:
			raise Exception("无法解释的脚本:%s" % script)
		
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

		return None, None
	
	def getEventScript(self, who, npcObj, key):
		'''事件脚本
		'''
		info = self.getEventInfoByNpc(npcObj)
		if info:
			return info.get(key)
		return None
		
	def doEventScript(self, who, npcObj, key):
		'''解释事件脚本
		'''
		if not self.validDoEventScript(who, npcObj, key):
			return
		script = self.getEventScript(who, npcObj, key)
		if not script:
			return
		self.doScript(who, npcObj, script)
	
	def validDoEventScript(self, who, npcObj, key):
		return 1
	
	def validAnswerEventScript(self, who, npcObj, optionNo):
		return 1
			
	def missionDone(self, who, npcObj):
		'''完成
		'''
		if hasattr(self, "onMissionDone"):
			self.onMissionDone(who, npcObj)
	
	def missionFail(self, who, npcObj):
		'''失败
		'''
		if hasattr(self, "onMissionFail"):
			self.onMissionFail(who, npcObj)
			
	def popPetUI(self, who, npcObj):
		'''弹出上交宠物界面
		'''
		raise NotImplementedError("请在子类实现")
	
	def popPropsUI(self, who, npcObj):
		'''弹出上交物品界面
		'''
		raise NotImplementedError("请在子类实现")
	
	def transfer(self, who, sceneId, x=0, y=0):
		'''传送到指定场景
		'''
		sceneId = self.transSceneId(sceneId)
		scene.doTransfer(who, sceneId, x, y)
	
	def customEvent(self, who, npcObj, eventName, *args):
		'''自定义事件
		'''
		pass
	
	def branchScript(self, who, npcObj, branchIdx, flag):
		'''分支脚本
		'''
		condition = self.getBranchCondition(who, npcObj, branchIdx, flag)
		for info in self.getBranchInfo(branchIdx):
			if info["条件"] == condition:
				self.doScript(who, npcObj, info["脚本"])
				return
			
	def getBranchCondition(self, who, npcObj, branchIdx, flag):
		if flag == "lv":
			return who.level
		if flag ==  "school":
			return who.school
		if flag == "team":
			teamObj = who.getTeamObj()
			if not teamObj:
				return 1
			return teamObj.inTeamSize
		if flag == "gender":
			return who.gender
		return 0

def transLevelStr(who, levelStr, npcObj=None):
	'''转换含有等级通配符字符串
	'''
	for lvName in re.findall("(\w*LV)", levelStr):
		lv = transLevel(who, lvName, npcObj)
		levelStr = re.sub(r"\b%s\b" % lvName, str(lv), levelStr)
	return levelStr
	
def transLevel(who, levelName, npcObj=None):
	'''转换等级通配符
	'''
	if levelName == "ALV":
		return who.getTeamObj().getAvgLV() if who.inTeam() else who.level
	if levelName == "MLV":
		return who.getTeamObj().getMaxLV() if who.inTeam() else who.level
	if levelName == "LV":
		return who.level
	return who.level

def transShapeStr(shapeStr, who=None, npcObj=None):
	'''转换造型字符串
	'''
	shapeParts = [0, 1, 0, 0, 0, 0]
	if isinstance(shapeStr, int):
		shape = shapeStr
	else:
		shapeList = shapeStr.split("|")
		shapeStr = shapeList[rand(len(shapeList))]
		
		m = re.match("(\S+)\((\S+)\)", shapeStr)
		if m:
			shape = int(m.group(1))
			shapeParts = []
			for shapepartType, shapePart in enumerate(m.group(2).split(",")):
				if shapePart == "R":
					shapePart = shapePartScope.getShapePartByRand(shape, shapepartType)
				else:
					shapePart = int(shapePart)
				shapeParts.append(shapePart)
		elif shapeStr == "$npc" and npcObj:
			shape = npcObj.shape
			shapeParts = npcObj.shapeParts
		else:
			shape = int(shapeStr)

	return shape, shapeParts

def transColorsStr(colorStr, who=None, npcObj=None):
	'''转换染色字符串
	'''
	colors = [0, 0, 0, 0, 0, 0]
	if colorStr == "$npc":
		if npcObj:
			colors = npcObj.getColors()
	else:
		colors = [int(s) for s in colorStr.split(",")]
	return colors


#===============================================================================
# 脚本处理
#===============================================================================
def handleDone(gameObj, who, npcObj, *args):
	'''完成
	'''
	gameObj.missionDone(who, npcObj)
	
def handleFail(gameObj, who, npcObj, *args):
	'''失败
	'''
	gameObj.missionFail(who, npcObj)

def handleSet(gameObj, who, npcObj, key, val):
	'''设置值
	'''
	if val.isdigit():
		val = int(val)
	gameObj.set(key, val)
	
def handleAdd(gameObj, who, npcObj, key, val):
	'''设置值
	'''
	if val.isdigit():
		val = int(val)
	gameObj.add(key, val)
	
def handlePopPet(gameObj, who, npcObj, *args):
	'''弹出上交宠物界面
	'''
	gameObj.popPetUI(who, npcObj)
	
def handlePopProps(gameObj, who, npcObj, *args):
	'''弹出上交物品界面
	'''
	gameObj.popPropsUI(who, npcObj)

def handleTransfer(gameObj, who, npcObj, *args):
	'''传送
	'''
	sceneId, x, y = [int(arg) for arg in args]
	gameObj.transfer(who, sceneId, x, y)
	
def handleRemoveNpc(gameObj, who, npcObj, *args):
	'''移除npc
	'''
	gameObj.removeNpc(npcObj)
	
def handlePickProps(gameObj, who, npcObj, *args):
	'''采集物品
	'''
	args = [int(arg) for arg in args]
	gameObj.pickProps(who, npcObj, *args)
		
def handleNpcSay(gameObj, who, npcObj, chatIdxStr):
	'''npc对话框
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	npcObj.say(who, gameObj.getText(chatIdx, who.id))

def handleTeamNpcSay(gameObj, who, npcObj, chatIdxStr):
	'''队伍的npc对话框
	'''
	if who.inTeam():
		pidList = who.getTeamObj().getInTeamList()
	else:
		pidList = [who.id]
		
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	for pid in pidList:
		who = getRole(pid)
		if who:
			npcObj.say(who, gameObj.getText(chatIdx, pid))
			
def handleDialog(gameObj, who, npcObj, chatIdxStr):
	'''对白框
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.dialog(who, gameObj.getText(chatIdx, who.id))
	
def handleTeamDialog(gameObj, who, npcObj, chatIdxStr):
	'''队伍的对白框
	'''
	if who.inTeam():
		pidList = who.getTeamObj().getInTeamList()
	else:
		pidList = [who.id]
		
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	for pid in pidList:
		who = getRole(pid)
		if who:
			message.dialog(who, gameObj.getText(chatIdx, pid))
	
def handleSelectBox(gameObj, who, npcObj, chatIdxStr):
	'''选择框
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	msg = gameObj.getText(chatIdx, who.id)
	gameObjRef = weakref.ref(gameObj)
	message.selectBoxNew(who, functor(responseSelectBox, npcObj.id, gameObjRef), msg, npcObj)
	
def responseSelectBox(who, selectNo, npcId, gameObjRef):
	npcObj = getNpc(npcId)
	if npcObj:
		npcObj = npcObj.this()
	else:
		return

	gameObj = gameObjRef()
	if not gameObj:
		return
	
	if not gameObj.validDoEventScript(who, npcObj, "回复"):
		return
	script = gameObj.getEventScript(who, npcObj, "回复")
	if not script:
		return

	for option in script.split(";"):
		optionNo, script = option.split(":")
		if int(optionNo) == selectNo:
			if gameObj.validAnswerEventScript(who, npcObj, optionNo):
				gameObj.doScript(who, npcObj, script)
			return
		
def handleConfirmBox(gameObj, who, npcObj, chatIdxStr):
	'''确认框
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	msg = gameObj.getText(chatIdx, who.id)
	gameObjRef = weakref.ref(gameObj)
	message.confirmBoxNew(who, functor(responseConfirmBox, npcObj.id, gameObjRef), msg)

def responseConfirmBox(self, who, yes, npcId, gameObjRef):
	npcObj = getNpc(npcId)
	if npcObj:
		npcObj = npcObj.this()
	else:
		return

	gameObj = gameObjRef()
	if not gameObj:
		return
	if not gameObj.validDoEventScript(who, npcObj, "回复"):
		return
	script = gameObj.getEventScript(who, npcObj, "回复")
	if not script:
		return
	
	if yes:
		selectNo = 2
	else:
		selectNo = 1

	for option in script.split(";"):
		optionNo, script = option.split(":")
		if int(optionNo) == selectNo:
			if gameObj.validAnswerEventScript(who, npcObj, optionNo):
				gameObj.doScript(who, npcObj, script)
			return
		
def handleTips(gameObj, who, npcObj, chatIdxStr):
	'''透明提示
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.tips(who, gameObj.getText(chatIdx, who.id))
	
def handleTeamTips(gameObj, who, npcObj, chatIdxStr):
	'''队伍透明提示
	'''
	if who.inTeam():
		pidList = who.getTeamObj().getInTeamList()
	else:
		pidList = [who.id]
		
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	for pid in pidList:
		message.tips(pid, gameObj.getText(chatIdx, who.id))
		
def handleMessage(gameObj, who, npcObj, chatIdxStr):
	'''信息提示
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.message(who, gameObj.getText(chatIdx, who.id))
	
def handleTeamMessage(gameObj, who, npcObj, chatIdxStr):
	'''队伍提示
	'''
	if who.inTeam():
		pidList = who.getTeamObj().getInTeamList()
	else:
		pidList = [who.id]
		
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	for pid in pidList:
		message.message(pid, gameObj.getText(chatIdx, who.id))
		
def handleTipsMessage(gameObj, who, npcObj, chatIdxStr):
	'''信息提示
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	txt = gameObj.getText(chatIdx, who.id)
	message.tips(who, txt)
	message.message(who, txt)
		
def handleSysMessage(gameObj, who, npcObj, chatIdxStr):
	'''系统传闻
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.sysMessage(gameObj.getText(chatIdx, who.id))
	
def handleSysAnnounce(gameObj, who, npcObj, chatIdxStr):
	'''系统公告
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.sysAnnounce(gameObj.getText(chatIdx, who.id))
	
def handleSysMessageRoll(gameObj, who, npcObj, chatIdxStr):
	'''系统传闻且滚动
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.sysMessageRoll(gameObj.getText(chatIdx, who.id))
	
def handleSysAnnounceRoll(gameObj, who, npcObj, chatIdxStr):
	'''系统公告且滚动
	'''
	chatIdx = gameObj.transIdxByGroup(int(chatIdxStr))
	message.sysAnnounceRoll(gameObj.getText(chatIdx, who.id))
		
def handleFight(gameObj, who, npcObj, fightIdxStr):
	'''战斗
	'''
	fightIdx = gameObj.transIdxByGroup(int(fightIdxStr))
	gameObj.fight(who, npcObj, fightIdx)
	
def handleSingleFight(gameObj, who, npcObj, fightIdxStr):
	'''独占式战斗
	'''
	fightIdx = gameObj.transIdxByGroup(int(fightIdxStr))
	gameObj.fightSingle(who, npcObj, fightIdx)
	
def handleCustomEvent(gameObj, who, npcObj, eventName):
	'''自定义事件
	'''
	args = []
	m = re.match("(\S+)\((\S+)\)", eventName)
	if m:
		eventName = m.group(1)
		for arg in m.group(2).split(","):
			if isInteger(arg):
				arg = int(arg)
			elif isFloat(arg):
				arg = float(arg)
			args.append(arg)
	gameObj.customEvent(who, npcObj, eventName, *args)
	
def handleReward(gameObj, who, npcObj, rwdIdxStr):
	'''奖励
	'''
	rwdIdx = gameObj.transIdxByGroup(int(rwdIdxStr))
	gameObj.reward(who, rwdIdx, npcObj)
	
def handleRewardTeam(gameObj, who, npcObj, rwdIdxStr):
	'''奖励队伍
	'''
	rwdIdx = gameObj.transIdxByGroup(int(rwdIdxStr))
	gameObj.rewardTeam(who, rwdIdx, npcObj)
	
def handleAddNpc(gameObj, who, npcObj, npcStr):
	'''增加npc
	'''
	npcIdx = gameObj.transIdxByGroup(int(npcStr))
	return gameObj.addNpc(npcIdx, who=who)
	
def handleBindEvent(gameObj, who, npcObj, npcIdx, eventIdx):
	'''绑定事件
	'''
	if isinstance(npcIdx, str):
		npcList = npcIdx.split("|")
		npcIdx = npcList[rand(len(npcList))]
	if npcIdx == "master":
		npcObj = npc.defines.getSchoolMaster(who.school)
		npcIdx = npcObj.idx
	else:
		npcIdx = gameObj.transIdxByGroup(int(npcIdx))
	
	if isinstance(eventIdx, str):
		eventList = eventIdx.split("|")
		eventIdx = eventList[rand(len(eventList))]
		eventIdx = int(eventIdx)
	eventIdx = gameObj.transIdxByGroup(eventIdx)

	gameObj.bindEvent(npcIdx, eventIdx)
	return npcIdx
	
def handleBranchScript(gameObj, who, npcObj, branchIdxStr, flag):
	'''分支脚本
	'''
	branchIdx = int(branchIdxStr)
	gameObj.branchScript(who, npcObj, branchIdx, flag)
	
def handleAddNpcAndBindEvent(gameObj, who, npcObj, npcIdx, eventIdx):
	'''增加npc并绑定事件
	'''
	npcObjAdded = handleAddNpc(gameObj, who, npcObj, npcIdx)
	npcStr = str(npcObjAdded.idx)
	handleBindEvent(gameObj, who, npcObj, npcStr, eventIdx)
	
def handleNpcLook(gameObj, who, npcObj, *args):
	'''点击场景npc
	'''
	if hasattr(npcObj, "doLook"):
		npcObj.doLook(who)
		
def handleBindAndTriggerEvent(gameObj, who, npcObj, eventIdx):
	'''给当前npc绑定事件，并触发
	'''
	if isinstance(eventIdx, str):
		eventList = eventIdx.split("|")
		eventIdx = eventList[rand(len(eventList))]
		eventIdx = int(eventIdx)
	eventIdx = gameObj.transIdxByGroup(eventIdx)
	gameObj.bindEvent(npcObj.idx, eventIdx)
	gameObj.doEventScript(who, npcObj, "点击")


# 脚本处理函数
gScriptHandlerList = {
	"DONE": handleDone,
	"FAIL": handleFail,
	"SET\((\S+),(\S+)\)": handleSet,
	"ADD\((\S+),(\S+)\)": handleAdd,
	"POPP": handlePopPet,
	"POPI": handlePopProps,
	"TRANS\((\S+),(\S+),(\S+)\)": handleTransfer,
	"REMOVE": handleRemoveNpc,
	"PICK\((\S+),(\S+),(\S+)\)": handlePickProps,
	"PICK\((\S+),(\S+)\)": handlePickProps,
	"D(\d+)": handleNpcSay,
	"TD(\d+)": handleTeamNpcSay,
	"DL(\d+)": handleDialog,
	"TDL(\d+)": handleTeamDialog,
	"SB(\d+)": handleSelectBox,
	"CB(\d+)": handleConfirmBox,
	"TP(\d+)": handleTips,
	"TTP(\d+)": handleTeamTips,
	"M(\d+)": handleMessage,
	"TM(\d+)": handleTeamMessage,
	"TPM(\d+)": handleTipsMessage,
	"SM(\d+)": handleSysMessage,
	"SA(\d+)": handleSysAnnounce,
	"RSM(\d+)": handleSysMessageRoll,
	"RSA(\d+)": handleSysAnnounceRoll,
	"F(\d+)": handleFight,
	"SF(\d+)": handleSingleFight,
	"\$(\S+)": handleCustomEvent,
	"R(\d+)": handleReward,
	"TR(\d+)": handleRewardTeam,
	"N(\d+)": handleAddNpc,
	"E\((\S+),(\S+)\)": handleBindEvent,
	"B\((\S+),(\S+)\)": handleBranchScript,
	"NE\((\S+),(\S+)\)": handleAddNpcAndBindEvent,
	"LOOK": handleNpcLook,
	"TE(\S+)": handleBindAndTriggerEvent, # 给当前npc绑定事件，并触发
}

	
from common import *
from war.defines import *
import npc.defines
import role.defines
import copy
import pet
import misc
import launch
import war
import scene
import re
import message
import npc
import gevent
import pet
import types
import props
import weakref