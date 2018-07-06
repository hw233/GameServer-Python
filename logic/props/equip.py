#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import props.object
import equipData
import c

import sysConfigData

#装备
class cProps(props.object.cProps):

	tTemp=('base','add','gem','five','score','life', 'spEffect', 'spSkill', 'isMake')

	MSG_DETAIL=props.object.cProps.MSG_DETAIL+tTemp #详细界面所要补充发送的
	MSG_ALL = props.object.cProps.MSG_FIRST + MSG_DETAIL

	def __init__(self,iNo):
		props.object.cProps.__init__(self,iNo)
		self.dFinalAttr={}
		self.dGems={}  #{孔号:[宝石编号,数量],孔号:[宝石编号,数量]}
		
	@property
	def kind(self):
		return ITEM_EQUIP

	def maxStack(self):#override 装备最大叠加数量都是1
		return 1

	def save(self):#override
		dData=props.object.cProps.save(self)
		if self.dGems:
			dData['gems']=self.dGems
		return dData

	def load(self,dData):#override
		props.object.cProps.load(self,dData)
		self.dGems=dData.pop('gems',{})

	def addGem(self,iHole,iGemNo,iAmount):#增加宝石
		lInfo=self.dGems.setdefault(iHole,[iGemNo,0])
		lInfo[1]=lInfo[1]+iAmount
		self.markDirty()

	def removeGem(self,iHole):#移除宝石
		self.markDirty()
		return self.dGems.pop(iHole,[0,0]) #返回 宝石编号,数量

	def getGemInfo(self,iHole):
		return self.dGems.get(iHole,[0,0])

	@property
	def level(self):
		return self.getConfig("等级")

	def getWearLevel(self):
		'''穿着等级
		'''
		if self.fetch("spEffect") == 3902: #简易
			return max(0,self.level - 5)
		return self.level

	def getGemRatio(self):
		'''宝石效果加成
		'''
		if self.fetch("spEffect") == 3901: #宝石强化
			return 1.1
		return 1
	
	def getScore(self):  #评分
		return grade.gradeEquip(self)

	def isRare(self):  #是否珍品
		score = rareEquipScoreData.getScore(self.level,dEquipPos[self.wearPos()])
		if not score :
			return False
		return grade.gradeEquipBase(self) >= score

	def gems(self):
		return self.dGems

	def onBorn(self,*tArgs,**dArgs):#override
		props.object.cProps.onBorn(self,*tArgs,**dArgs)
		#设置基础属性
		dBase = dArgs.get("baseAttr")
		if not dBase:
			dBase = creatBaseAttr(self.iNo)
		self.set("baseAttr",dBase)
		# dMakeInfo = dArgs.get("makeInfo")
		# if dMakeInfo:
		# 	self.set("makeInfo",dMakeInfo)
		# 	dAdd = creatAddAttr(self.iNo)
		# 	self.set("addAttr",dAdd)
		dAdd = dArgs.get("addAttr")
		if dAdd:
			self.set("addAttr", dAdd)

		#设置耐久度
		self.set("life",self.maxLife())

		#设置五行
		if dArgs.get("fiveEl"):
			self.fiveEl = dArgs["fiveEl"]

		spEffect = dArgs.get("spEffect", 0)
		if spEffect:
			self.set("spEffect", spEffect)
		spSkill = dArgs.get("spSkill", 0)
		if spSkill:
			self.set("spSkill", spSkill)
		self.set("isMake", dArgs.get("isMake", 0))

	#计算装备最终属性 #目前发现没有地方在调用,估计是历史代码
	# def calcAttr(self):
	# 	#基础属性+强化属性+升星属性
	# 	iEhLv=self.enhanceLv()
	# 	iStarLv=self.starLv()
	# 	dAttr=self.calcAttrSpecial(iEhLv,iStarLv,self.dGems)
	# 	for iKey,iValue in dAttr.iteritems():
	# 		self.dFinalAttr[iKey]=iValue

	def toLogStr(self):#override 写到log里的给客服看的
		return ''

	def enhanceLv(self):#强化等级
		return self.fetch('ehLv',0)

	def starLv(self):#升星等级
		return self.fetch('star',0)

	def detail(self):#override
		return ''

	def getConfig(self,sKey,uDefault=0):#override
		return equipData.getConfig(self.no(),sKey,uDefault)

	def getAttr(self,sKey,uDefault=0):#获取装备属性
		return self.dFinalAttr.get(sKey,0)

	def school(self):#穿着要求职业
		return self.getConfig("门派",0)

	def gender(self):#穿着要求性别
		return self.getConfig("性别",0)

	def wearPos(self):#装备孔位置
		return self.getConfig('部位',0)

	def maxLife(self):#最大耐久
		return self.getConfig('耐久度',0)
	
	def getShapePart(self):
		'''套装部位
		'''
		return self.getConfig("套装", None)
	
	@property
	def fiveEl(self):
		'''五行
		'''
		return self.fetch("five", 0)
	
	@fiveEl.setter
	def fiveEl(self, fiveEl):
		self.set("five", fiveEl)

	def hole(self):
		return 8
		# return sysConfigData.gdData.get('dEquipHole',{}).get('exps',{}).get(self.color(),0)

	def resetAttr(self,who):
		self.dFinalAttr.clear()#重置属性
		if oPackage.getPropsPos(self)==self.wearPos():
			who.reCalcAttr()

	def resetHoles(self):
		#self.dGems.clear()
		self.markDirty()
		
	def getBaseAttrMsg(self):#获得基础属性信息
		lst = []
		dBase = self.fetch("baseAttr")
		for sKey in lAttrByOrder:
			iValue = dBase.get(sKey)
			if not iValue:
				continue
			msg = props_pb2.attrMsg()
			msg.name = dAttrType[sKey]
			msg.sValue = str(iValue)
			lst.append(msg)
		return lst

	def getAddAttrMsg(self):#获得附加属性信息
		lst = []
		dAdd = self.fetch("addAttr")
		if not dAdd:
			return lst
		for sKey in lAttrByOrder:
			iValue = dAdd.get(sKey)
			if not iValue:
				continue
			msg = props_pb2.attrMsg()
			msg.name = dAttrType[sKey]
			msg.sValue = str(iValue)
			lst.append(msg)
		return lst

	def getGemAttrMsg(self):#获得宝石属性信息
		lst = []
		for i in xrange(1, 3):
			iNo, iAmount = self.dGems.get(i, [0, 0])
			if iNo==0 or iAmount==0:
				continue
			msg = props_pb2.gemAttrMsg()
			msg.gemNo = iNo
			iGemLevel=int(round(math.log(iAmount,2)))+1#根据宝石数量算出宝石等级
			oTemplate = props.getCacheProps(iNo)
			dEffect = oTemplate.getEffect()
			#策划暂时一个宝石只有一个效果
			sKey = dEffect.keys()[0]
			iValue=int(dEffect.values()[0]*iGemLevel*self.getGemRatio())
			attrMsg = props_pb2.attrMsg()
			attrMsg.name = dAttrType[sKey]
			attrMsg.sValue = "{}".format(iValue)
			msg.attr.CopyFrom(attrMsg)
			msg.gemLv = iGemLevel
			msg.gemHole = i
			lst.append(msg)
		return lst

	def getCommonMsg(self,*tArgs):#override 分两次发送,第一次只发icon与叠加数量,第二次详细信息需要客户端再次请求
		msg=props_pb2.equipMsg()
		lNotFill=[]
		for arg in tArgs:
			if arg=='base':
				baseInfo = self.getBaseAttrMsg()
				msg.baseAttr.extend(baseInfo)
			elif arg=='add':
				addInfo = self.getAddAttrMsg()
				if addInfo:
					msg.addAttr.extend(addInfo)
			elif arg=='gem':
				gemInfo = self.getGemAttrMsg()
				if gemInfo:
					msg.gemAttr.extend(gemInfo)
				else:
					msg.bClearGem = True
			elif arg=='five':
				if self.fiveEl:
					msg.fiveAttr = self.fiveEl
			elif arg=='life':
				msg.life = self.fetch("life")
			elif arg=='score':
				msg.score = self.getScore()
			elif arg=='spEffect':
				msg.spEffect = self.fetch("spEffect")
			elif arg=='spSkill':
				msg.spSkill = self.fetch("spSkill")
			elif arg=='isMake':
				msg.isMake = self.fetch("isMake")
			else:
				lNotFill.append(arg)

		msg.baseSerialized=props.object.cProps.getCommonMsg(self,*lNotFill).SerializeToString()
		return msg

	def setTreasureShopMsg(self , oMsg):
		'''设置摆摊信息
		'''
		oMsg.props.CopyFrom(self.getMsg4Package(None,*self.MSG_ALL))

	def onRemoveFromContainer(self,oPackage):#从容器上删除之时
		who=role.gKeeper.getObj(self.ownerId)
		if who and c.WEAR_EQUIP_POS_START<=oPackage.getPropsPos(self)<=c.WEAR_EQUIP_POS_STOP:
			who.reCalcAttr()

	def setup(self, who, isLogin=False):
		if not self.isWear():
			return

		if self.isWearValid(): # 已生效的,给玩家加效果
			self.addEffect(who)
		
		if not isLogin:
			shapePart = self.getShapePart()
			if shapePart != None:
				who.setShapeParts(SHAPE_PART_TYPE_WEAPON, shapePart)

	def cancelSetup(self, who):
		if not self.isWear():
			return

		if self.isWearValid(): # 已生效的,从玩家移除效果
			self.removeEffect(who)
		
		shapePart = self.getShapePart()
		if shapePart != None:
			who.setShapeParts(SHAPE_PART_TYPE_WEAPON, 1)

	def addApply(self, who):
		sFlag = 'equip{}'.format(self.id)
		for sKey,iValue in self.fetch("baseAttr").iteritems():
			who.addApply(sKey,iValue,sFlag)
		for sKey,iValue in self.fetch("addAttr",{}).iteritems():
			who.addApply(sKey,iValue,sFlag)

		for iHole,[iGemNo,iAmount] in self.dGems.iteritems():
			iGemLevel=int(round(math.log(iAmount,2)))+1#根据宝石数量算出宝石等级
			dEffect=props.getCacheProps(iGemNo).getEffect()
			for sKey,sValue in dEffect.iteritems():#策划暂时一个宝石只有一个效果
				iValue=int(sValue*iGemLevel*self.getGemRatio())
				who.addApply(sKey,iValue,sFlag)
			
	def removeApply(self, who):
		who.removeApplyByFlag('equip{}'.format(self.id))

	def refreshApply(self, who):
		'''刷新装备的属性与角色的绑定
		'''
		if not self.isWearValid(): # 已失效
			return
		self.removeEffect(who)
		self.addEffect(who)
		who.reCalcAttr()
		rank.updateEquipScoreRank(who, self)

	def decompose(self, who):
		'''分解
		'''
		if self.level >= 50:
			message(who, "该装备#C04≥50级#n，不能分解")
			return
		cash = self.getConfig("回收价格", 0)
		name = self.getConfig("名称", "")
		content = "分解#C07{}#n获得#IS#n#C07{}#n？\nQ取消\nQ分解".format(name, cash)
		message.confirmBoxNew(who, functor(self.responseDecompose, cash), content)
		
	def responseDecompose(self, who, yes, cash):
		if not yes:
			return
		who.addCash(cash, "装备分解",None)
		who.propsCtn.removeItem(self)
		message.tips(who, "分解成功，获得#IS#n#C02{}#n".format(cash))
		
	def isWear(self):
		'''是否已装上
		'''
		return self.fetch("wear")
	
	def setWear(self, isWear):
		'''设置装上或卸下
		'''
		if isWear:
			self.set("wear", 1)
		else:
			self.delete("wear")
			
	def isWearValid(self):
		'''是否已生效
		'''
		if self.fetch("invalid"):
			return 0
		return 1
	
	def setWearValid(self, isValid):
		'''设置生效或失效
		'''
		if isValid:
			self.delete("invalid")
		else:
			self.set("invalid", 1)

	def doWear(self,who, bGemReplace=False):#穿装备
		if not who.propsCtn.getItem(self.id):
			return
		if who.level<self.getWearLevel():
			who.endPoint.rpcTips('等级不足，无法装备')
			return
		if self.school() not in (0,who.school) or self.gender() not in (0,who.gender):
			who.endPoint.rpcTips('门派或性别不符合，无法穿戴')
			return
		if not self.getLife():
			who.endPoint.rpcTips('装备已无耐久，无法穿戴')
			return
		
		oEquipFork = props.fork(self)
		oEquipFork.setWear(True)
		iWearPos = self.wearPos()
		oWearEquip = who.equipCtn.getEquipByWearPos(iWearPos)
		#有装备的话就替换位置
		if oWearEquip:
			if bGemReplace:
				dGems = copy.deepcopy(oWearEquip.gems())
				oWearEquip.dGems = {}
				oEquipFork.dGems = dGems

			who.propsCtn.removeItem(self)
			who.equipCtn.removeItem(oWearEquip)
			oWearEquipFork = props.fork(oWearEquip)
			oWearEquipFork.setWear(False)
			who.propsCtn.addItem(oWearEquipFork)
			rank.removeEquipScoreRank(who, oWearEquipFork)
			who.equipCtn.addItem(oEquipFork)
			if oWearEquipFork.level < 40:
				self.autoDecompose(who, oWearEquipFork)
		else:
			who.propsCtn.removeItem(self)
			who.equipCtn.addItem(oEquipFork)

		who.endPoint.rpcTips('装备成功')

		who.reCalcAttr()#重新计算人物属性
		state.checkRepairState(who)
		rank.updateEquipScoreRank(who, oEquipFork)
		
		import listener
		listener.doListen("穿装备", who, propsNo=oEquipFork.no(), propsId=oEquipFork.id)

	def autoDecompose(self, who, equip):
			cash = equip.getConfig("回收价格", 0)
			name = equip.getConfig("名称", "")
			who.addCash(cash, "装备分解",None)
			who.propsCtn.removeItem(equip)
			message.tips(who, "已自动分解低于40级的装备")
			message.tips(who, "分解成功，获得#IS#n#C02{}#n".format(cash))

		# def responseDecompose(self, who, yes, cash):
		# if not yes:
		# 	return
		# who.addCash(cash, "装备分解",None)
		# who.propsCtn.removeItem(self)
		# message.tips(who, "分解成功，获得#IS#n#C02{}#n".format(cash))

	def doDoff(self,who):#卸装备
		if not who.equipCtn.getItem(self.id):
			return
		if not who.propsCtn.leftCapacity():
			who.endPoint.rpcTips('背包已满，无法卸下装备')
			return

		oEquipFork = props.fork(self)
		oEquipFork.setWear(False)
		who.equipCtn.removeItem(self)
		who.propsCtn.addItem(oEquipFork)

		who.reCalcAttr()
		state.checkRepairState(who)
		rank.removeEquipScoreRank(who, oEquipFork)

	def shortcut(self,who):#快捷使用
		if who.level<self.getWearLevel() or self.school() not in (0,who.school) or self.gender() not in (0,who.gender):
			return False
		oEquip = who.equipCtn.getEquipByWearPos(self.wearPos())
		if not oEquip:
			return True
		return self.getScore() > oEquip.getScore()

	def getAddon(self):
		#附加状态
		addon = props.object.cProps.getAddon(self)
		if self.fetch("life")<=self.maxLife()*20/100:
			addon |= ADDON_REPAIRED
		if self.isRare():
			addon |= ADDON_RARE
		return addon

	#用于在包裹内排序
	def compareAtSameType(self,oItem):#override,排序比较函数,如果self要比itemobj排得要前,返回负值
		tWeight=(1,2,3,4,5,6,7,8,9)#各种类型装备的权重表,在此表中越靠前的,则在包裹栏里也越靠前
		iUnDefine=len(tWeight)#未定义的,坐后面
		try:
			idx1=tWeight.index(self.wearPos())
		except Exception:
			idx1=iUnDefine
		try:
			idx2=tWeight.index(oItem.wearPos())
		except Exception:
			idx2=iUnDefine
		if idx1!=idx2:
			return idx1-idx2
		elif idx1==iUnDefine and idx2==iUnDefine:#两个都未定义
			return 0
		if self.level!=oItem.level:
			return -(self.level-oItem.level)
		return -(self.enhanceLv()-oItem.enhanceLv())#强化等级从大到小

	#===================
	#装备耐久
	def getLife(self):
		return self.fetch("life", 0)

	#扣装备耐久
	def addLife(self, iAdd=0):
		life = self.fetch("life", 0) + iAdd
		if life < 0:
			life = 0
		self.set("life", life)
		
		#更新给客户端
		who = getRole(self.ownerId)
		if who:
			if self.isWear():
				who.endPoint.rpcModEquip(self.getMsg4Item(who.equipCtn,"life","addon"))
			else:
				who.endPoint.rpcModProps(self.getMsg4Package(who.propsCtn,'life','addon'))
		
		self.checkWearStatus()

	#恢复耐久
	def recoverLife(self):
		iAddLife = self.maxLife() - self.getLife()
		self.addLife(iAddLife)

	def addEffect(self, who):
		'''绑定装备效果到角色上
		'''
		self.addApply(who)
		skillIdList = self.getSkillList()
		if skillIdList:
			who.addEquipSkill(self.id, *skillIdList)

	def removeEffect(self, who):
		'''移除装备绑定在角色上的效果
		'''
		self.removeApply(who)
		skillIdList = self.getSkillList()
		if skillIdList:
			who.removeEquipSkill(self.id)

	def checkWearStatus(self):
		'''检查装备状态
		'''
		who = getRole(self.ownerId)
		if self.getLife() == 0:
			if self.isWearValid(): # 生效的装备要失效
				self.setWearValid(False)
				if self.isWear():
					self.removeEffect(who)
					who.reCalcAttr()
		else:
			if not self.isWearValid(): # 失效的装备要生效
				self.setWearValid(True)
				if self.isWear():
					self.addEffect(who)
					who.reCalcAttr()
					
		if self.isWear():
			state.checkRepairState(who)

	#增加战斗场数
	def addFightCnt(self, iCnt=1):
		self.add("fightCnt", iCnt)

	def getFightCnt(self):
		return self.fetch("fightCnt", 0)

	#重置战斗场数
	def setFightCnt(self, iCnt):
		self.set("fightCnt", iCnt)

	#修理价格 = (最大耐久 - 当前耐久)/最大耐久 * 出售价格 * 100
	def lifeRepairPrice(self):
		iMax = self.maxLife()
		iSell = self.getConfig("出售价格", 0)
		return int((iMax - self.getLife()) * iSell * 100/ iMax )
	#装备耐久
	#============================

	def getSkillList(self):
		'''获取装备的特技特效
		'''
		lSesks = []
		spEffect = self.fetch("spEffect")
		if spEffect:
			lSesks.append(spEffect)
		spSkill = self.fetch("spSkill")
		if spSkill:
			lSesks.append(spSkill)
		return lSesks


#=============================================================================
#属性生成
#=============================================================================
def creatAddAttr(iNo):#生成附加属性
	iAdd = equipData.getConfig(iNo,"附加属性",0)
	if not iAdd:
		return
	dAdd  = {}
	iRand = rand(1,100)
	lAttr = role.defines.baseAttrList
	if iRand<=80:
		sType  = lAttr[rand(len(lAttr))]
		iValue = iAdd * rand(50,100) / 100
		dAdd[sType] = max(iValue,1)
	else:
		lType = random.sample(lAttr,2)
		for sType in lType:
			iValue = iAdd * rand(35,70) / 100
			dAdd[sType] = max(iValue,1)

	return dAdd

def creatBaseAttr(iNo,iType=0):#生成基础属性
	dRang = {
		0:(80,90),
		1:(90,110),
		2:(95,115),
	}
	iMin,iMax = dRang[iType]

	dBase = {}
	for sType,sValue in  role.defines.attrDescList.iteritems():
		iValue = equipData.getConfig(iNo,sValue,0)
		if not iValue:
			continue
		iValue = iValue * rand(iMin,iMax) / 100
		dBase[sType] = iValue

	iAttack = equipData.getConfig(iNo,"攻击力",0)
	if iAttack:
		iAttack = iAttack * rand(iMin,iMax) / 100
		dBase["phyDam"] = dBase["magDam"] = max(iAttack,1)
		dBase["cure"] = max(iAttack/2,1)

	return dBase

def creatFive():#生成五行属性
	lst = range(1,7)
	return lst[rand(len(lst))]

def sendEquipForNewbie(who):
	dEquip = {
		1111:[100000,101000,101200,101400,101500,101600],
		1121:[100050,101100,101300,101400,101500,101600],
		1211:[100100,101000,101200,101400,101500,101600],
		1221:[100150,101100,101300,101400,101500,101600],
		1311:[100200,101000,101200,101400,101500,101600],
		1321:[100250,101100,101300,101400,101500,101600],
		1411:[100300,101000,101200,101400,101500,101600],
		1421:[100350,101100,101300,101400,101500,101600],
		1511:[100400,101000,101200,101400,101500,101600],
		1521:[100450,101100,101300,101400,101500,101600],
		1611:[100500,101000,101200,101400,101500,101600],
		1621:[100550,101100,101300,101400,101500,101600],

	}

	lEquip = dEquip.get(who.shape,[])
	for iEquip in lEquip:
		oEquip = props.new(iEquip)
		fiveEl = equipMake.make.creatFive(oEquip)
		if fiveEl:
			oEquip.fiveEl = fiveEl
		oEquip.setWear(True)
		who.equipCtn.addItem(oEquip)
		rank.updateEquipScoreRank(who, oEquip)
	who.reCalcAttr(False)

lAttrByOrder = ["con","mag","str","res","spi","dex","phyDam","magDam","cure","phyDef","magDef","hpMax","mpMax","spe", "sealHit", "reSealHit"]

import copy
from props.defines import *
from role.defines import *
from common import *
import mainService
import role
import log
import misc
import u
import event
import props_pb2
import random
import ujson
import block.parameter
import propsData

import endPoint

import math
import resume
import factory
import sysConfigData
import findSort
import role.defines
import message
import state

import gem
import grade
import equipMake.make
import rank
import rareEquipScoreData



#装备对象(equip.cProps)存盘数据说明
##################dData##############
#enhanceLv(整型):强化等级
#gems:成员属性dGemholds,key=宝石孔代号,value=(宝石编号,宝石等级)

if 'gdCacheProps' not in globals():
	gdCacheProps={}

def getCacheProps(iNo,*tArgs,**dArgs):#
	obj=gdCacheProps.get(iNo)
	if obj:
		return obj
	gdCacheProps[iNo]=props.getCacheProps(iNo,*tArgs,**dArgs)
	return gdCacheProps[iNo]
	
