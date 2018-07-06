# -*- coding: utf-8 -*-
import npc.object

gAttrList = (
	"hp", "mp", "sp",
	"phyDam", "magDam", "phyDef", "magDef", "spe", "cure", 
	"phyCrit", "magCrit", "phyReCrit", "magReCrit",
)

class cNpc(npc.object.NpcBase):
	
	def __init__(self):
		npc.object.NpcBase.__init__(self)
		self.name = "战斗Npc"
		
		self.gameObj = GameObj()
		self.initMonster()
		self.monsterCnt = 2
		self.lineupObj = 0 # 阵法对象
		
	def initMonster(self):
		self.monsterBoss = war.monster.Monster()
		self.monsterBoss.setup()
		self.monsterBoss.name = "主怪"
		self.monsterBoss.shape = self.shape
		self.monsterBoss.shapeParts = self.shapeParts
		self.monsterBoss.monsterIdx = 0
		self.monsterBoss.monsterType = MONSTER_TYPE_BOSS
		
		self.monsterNormal = war.monster.Monster()
		self.monsterNormal.setup()
		self.monsterNormal.name = "帮凶"
		self.monsterNormal.shape = self.shape
		self.monsterNormal.shapeParts = self.shapeParts
		self.monsterNormal.monsterIdx = 1
		self.monsterNormal.monsterType = MONSTER_TYPE_NORMAL
	
	def doLook(self, who):
		content = '''我可以为你做点什么呢?
Q俺要单挑
Q俺要群殴
Q设置怪物属性
Q设置怪物数量
Q查看怪物信息
Q设置怪物阵法
Q设置我的属性
Q设置我的阵法'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.fightOne(who)
		elif selectNo == 2:
			self.fightMore(who)
		elif selectNo == 3:
			self.setupMonster(who)
		elif selectNo == 4:
			self.setMonsterCount(who)
		elif selectNo == 5:
			self.showInfo(who)
		elif selectNo == 6:
			self.setupLineupForMonster(who)
		elif selectNo == 7:
			self.setupRole(who)
		elif selectNo == 8:
			self.setupLineupForRole(who)
			
	def fightOne(self, who):
		if who.inWar():
			message.tips(who, "你已在战斗中")
			return
		
		war.warctrl.createCommonWar(who, gameObj=self.gameObj, npcObj=self)
		
	def fightMore(self, who):
		if who.inWar():
			message.tips(who, "你已在战斗中")
			return
		
		who.tmpFightMore = True
		war.warctrl.createCommonWar(who, gameObj=self.gameObj, npcObj=self)
		del who.tmpFightMore
		
	def setupMonster(self, who):
		content = '''这里可以设置主怪和小怪的各种属性
Q设置主怪等级
Q设置主怪战斗属性
Q设置主怪技能
Q设置主怪五行
Q设置小怪等级
Q设置小怪战斗属性
Q设置小怪技能
Q设置小怪五行
Q初始化怪物'''
		message.selectBoxNew(who, self.responseSetupMonster, content, self)
		
	def responseSetupMonster(self, who, selectNo):
		if selectNo == 1:
			self.setLevel(who)
		elif selectNo == 2:
			self.setAttrList(who)
		elif selectNo == 3:
			self.setSkill(who)
		elif selectNo == 4:
			self.setFiveEl(who)
		elif selectNo == 5:
			self.setLevel(who, isBoss=False)
		elif selectNo == 6:
			self.setAttrList(who, isBoss=False)
		elif selectNo == 7:
			self.setSkill(who, isBoss=False)
		elif selectNo == 8:
			self.setFiveEl(who, isBoss=False)
		elif selectNo == 9:
			self.initMonster()
			message.tips(who, "初始化成功")
		
	def setLevel(self, who, isBoss=True, errMsg=""):
		msg = "请输入怪物等级:"
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetLevel, isBoss), "设置怪物等级", msg, TYPE_LIMIT_INT, 3)
		
	def responseSetLevel(self, who, responseVal, isBoss):
		if not responseVal.isdigit():
			self.setLevel(who, isBoss, "格式不对")
			return
		
		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal
		
		level = int(responseVal)
		monsterObj.level = level
		monsterObj.setup()
		message.tips(who, "设置怪物等级为%s" % responseVal)
		
		if self.lineupObj:
			self.lineupObj.eyeObj.level = level
		
	def setAttrList(self, who, isBoss=True, errMsg=""):
		attrDescList = []
		for idx, attrName in enumerate(gAttrList):
			attrDesc = role.defines.getAttrDesc(attrName)
			attrDescList.append("%s.%s" % (idx + 1, attrDesc))
		msg = "请输入怪物属性(以逗号隔开)\n#C02%s#n\n格式:序号1=属性值1,序号2=属性值2" % ",".join(attrDescList)
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetAttrList, isBoss), "设置怪物属性", msg)
		
	def responseSetAttrList(self, who, responseVal, isBoss):
		attrList = {}
		for v in responseVal.split(","):
			m = re.match("(\d+)=(\d+)", v)
			if not m:
				self.setAttrList(who, isBoss, "格式不对")
				return
			
			attrIdx = int(m.group(1))
			attrVal = int(m.group(2))
			if not (0 < attrIdx <= len(gAttrList)):
				self.setAttrList(who, isBoss, "没有%d的序号" % attrIdx)
				return
			if attrVal < 0 or attrVal >= 2**32/2-1:
				self.setAttrList(who, isBoss, "非法的属性值:%s" % v)
				return
			attrList[attrIdx] = attrVal

		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal

		for attrIdx, attrVal in attrList.items():
			attrName = gAttrList[attrIdx - 1]
			attrName = "%sBase" % attrName
			if hasattr(monsterObj, attrName):
				setattr(monsterObj, attrName, attrVal)

		monsterObj.setup()
		message.tips(who, "属性设置成功")
	
	def setSkill(self, who, isBoss=True, errMsg=""):
		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal
		
		skillList = []
		for skillId, skillObj in monsterObj.skillList.iteritems():
			skillList.append("%s%s" % (skillObj.name, skillId))
		if skillList:
			skillMsg = "现在技能[%s]\n" % ",".join(skillList)
		else:
			skillMsg = ""
			
		msg = "%s请输入怪物技能，多个技能以逗号隔开:" % skillMsg
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetSkill, isBoss), "设置怪物技能", msg)
		
	def responseSetSkill(self, who, responseVal, isBoss):
		skillList = {}
		for v in responseVal.split(","):
			skillId, level = self.splitSkillStr(v)
			if not skillId:
				self.setSkill(who, isBoss, "格式错误")
				return
			skillList[skillId] = level

		if not skillList:
			self.setSkill(who, isBoss, "格式错误")
			return
		
		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal
		
# 		monsterObj.skillList = {}
		for skillId, level in skillList.iteritems():
			monsterObj.setSkill(skillId, level)
		monsterObj.setup()
		message.tips(who, "技能设置成功")
		
	def setFiveEl(self, who, isBoss=True):
		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal
		
		fiveElMsg = ""
		if monsterObj.fiveElAttack:
			fiveElAttackDesc = perform.defines.getFiveElDesc(monsterObj.fiveElAttack)
			fiveElDefendDesc = perform.defines.getFiveElDesc(monsterObj.fiveElDefend)
			fiveElMsg = "现在五行为[%s,%s]," % (fiveElAttackDesc, fiveElDefendDesc)
		
		msg = "%s请选择新的五行:" % fiveElMsg
		selectList = []
		for val, desc in perform.defines.fiveElVal2Desc.iteritems():
			msg += "\nQ" + desc
			selectList.append(val)
		
		msg += "\nQ没有"
		selectList.append(0)
		message.selectBoxNew(who, functor(self.responseSetFiveEl, selectList, isBoss), msg, self)
		
	def responseSetFiveEl(self, who, selectNo, selectList, isBoss):
		if selectNo > len(selectList):
			return
		
		fiveEl = selectList[selectNo-1]
		if isBoss:
			monsterObj = self.monsterBoss
		else:
			monsterObj = self.monsterNormal
		monsterObj.fiveElAttack = fiveEl
		monsterObj.fiveElDefend = fiveEl
		
		if fiveEl == 0:
			message.tips(who, "删除了怪物的五行")
			return
		fiveElDesc = perform.defines.getFiveElDesc(fiveEl)
		message.tips(who, "设置怪物五行为[%s,%s]" % (fiveElDesc, fiveElDesc))
			
	def setMonsterCount(self, who, errMsg=""):
		msg = "请输入怪物数量，至少2个:"
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, self.responsesetMonsterCount, "设置怪物数量", msg, limitType=TYPE_LIMIT_INT)
		
	def responsesetMonsterCount(self, who, responseVal):
		if not responseVal.isdigit():
			self.setMonsterCount(who, "格式不对")
			return

		monsterCnt = int(responseVal)
		if monsterCnt < 2:
			self.setMonsterCount(who, "怪物数量需要≥2")
			return
		
		self.monsterCnt = monsterCnt
		message.tips(who, "成功设置怪物数量为%d个" % monsterCnt)
		
	def showInfo(self, who):
		txtList = []
		
		for monsterObj in (self.monsterBoss, self.monsterNormal):
			tmpList = []
			tmpList.append("%s\n等级%d" % (monsterObj.name, monsterObj.level))
			for attrName in gAttrList:
				if not hasattr(monsterObj, attrName):
					continue
				tmpList.append("%s%d" % (role.defines.getAttrDesc(attrName), getattr(monsterObj, attrName)))
			
			skList = []
			for skillId, skillObj in monsterObj.getSkillList().iteritems():
				skList.append("%s/%d" % (skillObj.name, skillId))
			tmpList.append("技能(%s)" % ",".join(skList))
			txtList.append(",".join(tmpList))
		
		self.say(who, "\n".join(txtList))
		
	def setupLineupForMonster(self, who):
		if self.lineupObj:
			msgList = []
			msgList.append("%s,等级%s" % (self.lineupObj.name, self.lineupObj.level))
			eyeObj = self.lineupObj.getEyeObj()
			if eyeObj:
				skillList = [str(skillId) for skillId in eyeObj.fetch("skillList", [])]
				skillInfo = ",".join(skillList)
				msgList.append("%s,阵眼技能[%s]" % (eyeObj.name, skillInfo))
			msg = ",".join(msgList)
		else:
			msg = "无阵"
		msg = "当前%s，请输入阵法\n格式:1=阵法,2=阵法等级,3=阵眼被动技能,4=阵眼主动技能\n多个技能用|分隔" % msg
		message.inputBox(who, self.responseSetLineupForMonster, "设置阵法", msg)
		
	def responseSetLineupForMonster(self, who, responseVal):
		lst = []
		for k, v in re.findall("(\d+)\=([^\=,]+)", responseVal):
			lst.append((int(k), v))
		
		if not lst:
			message.tips(who, "格式不对")
			return
			
		lst.sort()

		for k, v in lst:
			if k == 1:
				self.lineupObj = lineup.createLineup(int(v))
				eyeObj = lineup.createEyeByNo(int(v), 0)
				eyeObj.level = self.monsterBoss.level
				self.lineupObj.eyeObj = eyeObj
			elif k == 2:
				if not self.lineupObj:
					message.tips(who, "要先设置阵法，才能设置阵法等级")
					return
				self.lineupObj.level = int(v)
			elif k in (3, 4):
				if not self.lineupObj:
					message.tips(who, "要先设置阵法，才能设置阵眼技能")
					return
				
				skillIdList = [int(s) for s in v.split("|")]
				if not skillIdList:
					message.tips(who, "阵眼技能格式错误")
					return
				if k == 4 and len(skillIdList) != 1:
					message.tips(who, "阵眼只能设置一个主动技能")
					return
				
				eyeObj = self.lineupObj.getEyeObj()
				skillList = eyeObj.fetch("skillList", [])
				if k == 3:
					skillList = skillList[:1]
					skillList.extend(skillIdList)
				else:
					if skillList:
						skillList[0] = skillIdList[0]
					else:
						skillList.append(skillIdList[0])
				
				eyeObj.set("skillList", skillList)
				eyeObj.generateSkillList()
				
		self.monsterBoss.setLineupObj(self.lineupObj)
		
		msgList = []
		msgList.append("%s,等级%s" % (self.lineupObj.name, self.lineupObj.level))
		eyeObj = self.lineupObj.getEyeObj()
		if eyeObj:
			skillList = [str(skillId) for skillId in eyeObj.fetch("skillList", [])]
			skillInfo = ",".join(skillList)
			msgList.append("%s,阵眼技能[%s]" % (eyeObj.name, skillInfo))
		msg = ",".join(msgList)
		self.say(who, "设置成功：%s" % msg)
		
	def setupRole(self, who):
		content = '''这里可以设置自己的属性
Q设置等级
Q设置门派
Q设置战斗属性
Q设置技能
Q增加修炼技能修炼点'''
		
		message.selectBoxNew(who, self.responseSetupRole, content, self)
		
	def responseSetupRole(self, who, selectNo):
		if selectNo == 1:
			self.setRoleLevel(who)
		elif selectNo == 2:
			self.setRoleSchool(who)
		elif selectNo == 3:
			self.setRoleAttrList(who)
		elif selectNo == 4:
			self.setRoleSkill(who)
		elif selectNo == 5:
			self.addSkillPoint(who)
			
	def setRoleLevel(self, who, errMsg=""):
		msg = "请输入你的新等级:"
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetRoleLevel), "设置等级", msg, TYPE_LIMIT_INT, 3)
		
	def responseSetRoleLevel(self, who, responseVal):
		if not responseVal.isdigit():
			self.setRoleLevel(who, "格式不对")
			return
		
		level = int(responseVal)
		if who.level >= level:
			message.dialog(who, "降级会导致玩家数据不准确，最好建新号测试，一定要降级的话请用指令[$set level X]来修改")
			return
		level = max(level - who.level,0)
		if not level:
			return
		for i in xrange(level):
			who.exp += who.expNext
			who.upLevel()
		import openLevel
		openLevel.checkExpRatio(who)
		# who.set("level", level)
		# who.attrChange("level")
		message.tips(who, "你的等级设置为%s" % level)
		self.resetSchoolSkill(who)
				
	def resetSchoolSkill(self, who):
		skillList = skillSchData.getOpenSchSkill(who.school, who.level)
		
		delList = []
		for skId, skObj in who.skillCtn.getAllItems():
			if hasattr(skObj, "school"):
				if skObj.school != who.school:
					delList.append(skId)
				elif skId not in skillList:
					delList.append(skId)
		
		for skId in delList:
			who.setSkill(skId, 0)

		for skId in skillList:
			who.setSkill(skId, who.level)
		
		who.reCalcAttr()
		
	def setRoleSchool(self, who, errMsg=""):
		selList = []
		msg = "请选择你的新门派:"
		for schoolId, schoolName in role.defines.schoolList.items():
			selList.append(schoolId)
			msg += "\nQ%s" % schoolName
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.selectBoxNew(who, functor(self.responseSetRoleSchool, selList), msg, self)
		
	def responseSetRoleSchool(self, who, selectNo, selList):
		if not (0 < selectNo <= len(selList)):
			return
		schoolId = selList[selectNo - 1]
		who.school = schoolId
		message.tips(who, "你的门派设置为%s" % role.defines.schoolList[schoolId])
		self.resetSchoolSkill(who)
		
	def setRoleAttrList(self, who, errMsg=""):
		attrDescList = []
		for idx, attrName in enumerate(gAttrList):
			attrDesc = role.defines.getAttrDesc(attrName)
			attrDescList.append("%s.%s" % (idx + 1, attrDesc))
		msg = "请输入属性(以逗号隔开)\n#C02%s#n\n格式:序号1=属性值1,序号2=属性值2" % ",".join(attrDescList)
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetRoleAttrList), "设置属性", msg)
		
	def responseSetRoleAttrList(self, who, responseVal):
		attrList = {}
		for v in responseVal.split(","):
			m = re.match("(\d+)=(\d+)", v)
			if not m:
				self.setRoleAttrList(who, "格式不对")
				return
			
			attrIdx = int(m.group(1))
			attrVal = int(m.group(2))
			if not (0 < attrIdx <= len(gAttrList)):
				self.setRoleAttrList(who, "没有%d的序号" % attrIdx)
				return
				
			attrList[attrIdx] = attrVal

		refreshList = []
		for attrIdx, attrVal in attrList.items():
			attrName = gAttrList[attrIdx - 1]
			if hasattr(who, attrName):
				setattr(who, attrName, attrVal)
				refreshList.append(attrName)
				if attrName in ("hp", "mp",):
					attrName = attrName + "Max"
					setattr(who, attrName, attrVal)
					refreshList.append(attrName)

		message.tips(who, "属性设置成功")
		if refreshList:
			who.attrChange(*refreshList)
		
	def setRoleSkill(self, who, errMsg=""):
		skillList = []
		for skillObj in who.skillCtn.getAllValues():
			if skillObj.id / 100 == who.school:
				continue
			skillList.append("%s%s" % (skillObj.name, skillObj.id))
		
		if skillList:
			skillMsg = "现有技能[%s]\n" % ",".join(skillList)
		else:
			skillMsg = ""
			
		msg = "%s请输入技能，多个技能以逗号隔开:\n格式:技能编号1,技能编号2" % skillMsg
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseSetRoleSkill), "设置技能", msg)
		
	def responseSetRoleSkill(self, who, responseVal):
		skillList = {}
		for v in responseVal.split(","):
			skillId, level = self.splitSkillStr(v)
			if not skillId:
				self.setRoleSkill(who, "格式不对")
				return
			skillList[skillId] = level

		if not skillList:
			self.setRoleSkill(who, "格式错误")
			return

		for skillId, level in skillList.items():
			who.setSkill(skillId, level)
		
		who.reCalcAttr()
		message.tips(who, "技能设置成功")
		
	def splitSkillStr(self, skillStr):
		'''分离技能字符串
		'''
		m = re.match("(\d+)=(\d+)", skillStr)
		if m:
			skillId = int(m.group(1))
			level = int(m.group(2))
			return skillId, level
		
		m = re.match("(\d+)", skillStr)
		if m:
			skillId = int(m.group(1))
			level = 1
			return skillId, level
		
		return None, None
		
	def addSkillPoint(self, who, errMsg=""):
		msg = "请输入要增加修炼技能的修炼点，多个技能以逗号隔开:\n格式:技能编号1=修炼点1,技能编号2=修炼点1..."
		if errMsg:
			msg = "%s!\n%s" % (errMsg, msg)
		message.inputBox(who, functor(self.responseaddSkillPoint), "设置修炼技能", msg)
		
	def responseaddSkillPoint(self, who, responseVal):
		skillPointList = {}
		for v in responseVal.split(","):
			m = re.match("(\d+)=(\d+)", v)
			if not m:
				self.addSkillPoint(who, "格式不对")
				return
			skillId = int(m.group(1))
			point = int(m.group(2))
			skillPointList[skillId] = point

		if not skillPointList:
			self.setRoleSkillPoint(who, "格式错误")
			return

		for skillId, point in skillPointList.items():
			who.skillCtn.addPracticePoint(skillId, point)
		
		who.reCalcAttr()
		message.tips(who, "修炼点增加成功")
		
	def setupLineupForRole(self, who):
		lineupObj = who.buddyCtn.getCurrentLineup()
		if lineupObj:
			msgList = []
			msgList.append("%s,等级%s" % (lineupObj.name, lineupObj.level))
			eyeObj = lineupObj.getEyeObj()
			if eyeObj:
				skillList = [str(skillId) for skillId in eyeObj.fetch("skillList", [])]
				skillInfo = ",".join(skillList)
				msgList.append("%s,阵眼技能[%s]" % (eyeObj.name, skillInfo))
			msg = ",".join(msgList)
		else:
			msg = "无阵"
		msg = "当前%s，请输入阵法\n格式:1=阵法,2=阵法等级,3=阵眼被动技能,4=阵眼主动技能\n多个技能用|分隔" % msg
		message.inputBox(who, self.responseSetLineupForRole, "设置阵法", msg)
		
	def responseSetLineupForRole(self, who, responseVal):
		lst = []
		for k, v in re.findall("(\d+)\=([^\=,]+)", responseVal):
			lst.append((int(k), v))
		
		if not lst:
			message.tips(who, "格式不对")
			return
			
		lst.sort()
		lineupObj = who.buddyCtn.getCurrentLineup()

		for k, v in lst:
			if k == 1:
				lineupId = int(v)
				lineupObj = who.lineupCtn.getItem(lineupId)
				if not lineupObj:
					eyeNo = int(v)
					lineupObj = who.lineupCtn.setLevel(lineupId, 1)
					eyeObj = lineup.addEye(who, eyeNo)
					lineupObj.setEyeObj(eyeObj)
				who.buddyCtn.setLineup(who.buddyCtn.currentIdx, lineupId)
				who.endPoint.rpcBattleMod(who.buddyCtn.currentIdx, lineupId)
			elif k == 2:
				if not lineupObj:
					message.tips(who, "要先设置阵法，才能设置阵法等级")
					return
				who.lineupCtn.setLevel(lineupObj.id, int(v))
			elif k in (3, 4):
				if not lineupObj:
					message.tips(who, "要先设置阵法，才能设置阵眼技能")
					return
				
				skillIdList = [int(s) for s in v.split("|")]
				if not skillIdList:
					message.tips(who, "阵眼技能格式错误")
					return
				if k == 4 and len(skillIdList) != 1:
					message.tips(who, "阵眼只能设置一个主动技能")
					return
				
				eyeObj = lineupObj.getEyeObj()
				skillList = eyeObj.fetch("skillList", [])
				if k == 3:
					skillList = skillList[:1]
					skillList.extend(skillIdList)
				else:
					if skillList:
						skillList[0] = skillIdList[0]
					else:
						skillList.append(skillIdList[0])
				
				eyeObj.set("skillList", skillList)
				eyeObj.generateSkillList()
				lineup.service.rpcEyeMod(who, eyeObj, "skillList")
		
		msgList = []
		msgList.append("%s,等级%s" % (lineupObj.name, lineupObj.level))
		eyeObj = lineupObj.getEyeObj()
		if eyeObj:
			skillList = [str(skillId) for skillId in eyeObj.fetch("skillList", [])]
			skillInfo = ",".join(skillList)
			msgList.append("%s,阵眼技能[%s]" % (eyeObj.name, skillInfo))
		msg = ",".join(msgList)
		self.say(who, "设置成功：%s" % msg)
	

class GameObj(object):
	'''玩法对象
	'''
	
	def newWar(self, who, fightIdx):
		warObj = war.object.War(WAR_COMMON)
		warObj.onWarEnd = functor(onWarEnd, who.id)
		return warObj

	def customCreateMonsterList(self, who, fightIdx, fightList, ableData, lineupData, npcObj):
		monsterList = {
			MONSTER_TYPE_NORMAL: [], # 普通怪
			MONSTER_TYPE_BOSS: [], # 主怪
			MONSTER_TYPE_FRIEND: [], # 友军怪
		}
		
		monsterList[MONSTER_TYPE_BOSS].append(npcObj.monsterBoss)
		if hasattr(who, "tmpFightMore"):
			for i in xrange(1, npcObj.monsterCnt):
				monsterObj = copyMonster(npcObj.monsterNormal)
				monsterObj.name = "帮凶%d" % i
				monsterObj.monsterIdx = i
				monsterObj.monsterType = MONSTER_TYPE_NORMAL
				monsterList[MONSTER_TYPE_NORMAL].append(monsterObj)
		return monsterList
		
		
def onWarEnd(warObj, pid):
	npcObj = warObj.gameNpc
	who = getRole(pid)
	if not who or not npcObj:
		return
# 	war.failBox(who, npcObj)


def copyMonster(monsterObj):
	monsterObjNew = war.monster.Monster()
	for attrName in gAttrList:
		attrName = "%sBase" % attrName
		if hasattr(monsterObjNew, attrName):
			setattr(monsterObjNew, attrName, getattr(monsterObj, attrName))
	
	for skId in monsterObj.skillList:
		monsterObjNew.setSkill(skId, 1)
	
	monsterObjNew.level = monsterObj.level
	monsterObjNew.fiveElAttack = monsterObj.fiveElAttack
	monsterObjNew.fiveElDefend = monsterObj.fiveElDefend
	monsterObjNew.setup()
	return monsterObjNew

from common import *
from war.defines import *
from qanda.defines import *
import war.monster
import message
import role.defines
import skill
import skill.upgrade
import war
import re
import skillSchData
import lineup
import perform.defines