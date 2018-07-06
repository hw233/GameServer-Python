# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
# 由于角色类文件太大,一部分玩家相关的代码转到这里来

if 'gbOnce' not in globals():
	gbOnce = True
	gsRoleId = set()

def existRole(iRoleId):  # 是否存在某个角色(在数据库中存在的也算)
	if iRoleId in gsRoleId:
		return True

	if resume.gKeeper.getObj(iRoleId):
		gsRoleId.add(iRoleId)
		return True

	if mail.mailBoxKeeper.getObj(iRoleId):
		gsRoleId.add(iRoleId)
		return True		

	# 先检查内存中有没有,没有再到数据库中查一下
	if factoryConcrete.lazyFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId):
		gsRoleId.add(iRoleId)
		return True
	return False

if 'giSequence' not in globals():
	giSequence = 0

def genSeq():  # 产生序号
	global giSequence
	giSequence += 1
	return giSequence

#----属性从哪里拿的标志----------------------------
ROLE_ATTR			 = genSeq()
FETCH_LAZY			 = genSeq()
FETCH_ACTIVE		 = genSeq()
FETCH_CYC_DAY		 = genSeq()
FETCH_CYC_WEEK		 = genSeq()
FETCH_CYC_MONTH		 = genSeq()
ACCOUNT = genSeq()
GLOBAL_FUNC			 = genSeq()
#--------------------------------
HERO = 1  # 要发送给主角,一般是在主角ui显示的属性
SERIALIZED1 = 2  # 广播全部看得到主角的其他玩家,且此属性是放在serialized1
# SERIALIZED2=4		#广播全部看得到主角的其他玩家,且此属性是放在serialized2
# SERIALIZED3=8		#广播全部看得到主角的其他玩家,且此属性是放在serialized3
# SERIALIZED4=16		#广播全部看得到主角的其他玩家,且此属性是放在serialized4
BROADCAST = ~HERO  # 需要广播

gdAttrInfo = {
	# 属性名:(属性来源,消息的域名,所在数据块)
	# 如果一个值可以用成员函数取也可以用成员变量取,就用成员变量
	'shape':(ROLE_ATTR, 'iShape', HERO | SERIALIZED1),
	'name':(ROLE_ATTR, 'sName', HERO | SERIALIZED1),
	"school":(ROLE_ATTR, 'iSchool', HERO),
	
	'level':(ROLE_ATTR, 'iLevel', HERO),
	'cash':(ROLE_ATTR, 'iCash', HERO),
	'diamond':(ROLE_ATTR, 'iDiamond', HERO), 	
	
	'exp':(ROLE_ATTR, 'iExp', HERO),
	'upNeedExp':(ROLE_ATTR, 'iUpNeedExp', HERO),
	
	'hp':(ROLE_ATTR, 'iHp', HERO),
	'hpMax':(ROLE_ATTR, 'iHpMax', HERO),
	
	'mp':(ROLE_ATTR, 'iMp', HERO),
	'mpMax':(ROLE_ATTR, 'iMpMax', HERO),
	
	'sp':(ROLE_ATTR, 'iSp', HERO),
	'spMax':(ROLE_ATTR, 'iSpMax', HERO),

	'point':(FETCH_LAZY, 'iPoint', HERO),  # 潜力点

	'con':(ROLE_ATTR, 'iCon', HERO),  # 体质
	'mag':(ROLE_ATTR, 'iMag', HERO),  # 魔力
	'str':(ROLE_ATTR, 'iStr', HERO),  # 力量
	'res':(ROLE_ATTR, 'iRes', HERO),  # 耐力
	'spi':(ROLE_ATTR, 'iSpi', HERO),  # 精神
	'dex':(ROLE_ATTR, 'iDex', HERO),  # 敏捷

	'phyDam':(ROLE_ATTR, 'iPhyDam', HERO),  # 物理伤害
	'magDam':(ROLE_ATTR, 'iMagDam', HERO),  # 法术伤害
	'phyDef':(ROLE_ATTR, 'iPhyDef', HERO),  # 物理防御
	'magDef':(ROLE_ATTR, 'iMagDef', HERO),  # 法术防御

	'phyCrit':(ROLE_ATTR, 'iPhyCrit', HERO),  # 物理暴击
	'magCrit':(ROLE_ATTR, 'iMagCrit', HERO),  # 法术暴击
	'phyReCrit':(ROLE_ATTR, 'iPhyReCrit', HERO),  # 物理抗暴
	'magReCrit':(ROLE_ATTR, 'iMagReCrit', HERO),  # 法术抗暴


	'huoli':(ROLE_ATTR, 'iHuoLi', HERO),  # 活力
	'huoliMax':(ROLE_ATTR, 'iHuoLiMax', HERO),  # 活力上限

	'spe':(ROLE_ATTR, 'iSpe', HERO),  # 速度
	'cure':(ROLE_ATTR, 'iCure', HERO),  # 治疗强度

	
	# 'voucher':(ROLE_ATTR,'iVoucher',HERO),


	# 'title':(ROLE_ATTR,'sTitle',HERO),

	# 'guildId':(ROLE_ATTR,'iGuild',HERO),
	# 'guildName':(ROLE_ATTR,'sGuildName',HERO),
	# 'guildTitle':(ROLE_ATTR,'sGuildTitle',HERO),	

}


# 需要广播的属性
gBroadcastList = (
	"name", "level", "shape", "shapeParts", "colors",
	"addon", "guildId", "guildName", "title", "titleEffect",
	"rideShape", "rideShapePart", "rideColors", "action",
)

# 刷新某几个属性到主角的客户端,刷新主角的ui
# 广播通知周围玩家主角属性发生了变化
# 置空主角序列化好的msg数据,使得再次使用时再次序列化.
def attrChange(who, *attrNameList):
	'''主角属性改变
	'''
	pid = who.id
	ep = mainService.getEndPointByRoleId(pid)
	if not ep:
		return
	
	roleAttr = {"roleId": pid} # 发送给主角
	broadcastList = {} # 广播
	for attrName in attrNameList:
		attrVal = who.getValByName(attrName)
		roleAttr[attrName] = attrVal
		if attrName in gBroadcastList:
			broadcastList[attrName] = attrVal
		
	ep.rpcAvatarAttrChange(**roleAttr)
	if broadcastList:
		scene.broadcastEttChange(who, broadcastList)
		
def broadcastAttrChange(who, *attrNameList):
	'''广播属性改变
	'''
	attrList = {}
	for attrName in attrNameList:
		attrVal = who.getValByName(attrName)
		attrList[attrName] = attrVal
	scene.broadcastEttChange(who, attrList)
	
def getEntityEnter(who):  # 实体进入视野
	entityEnter = scene_pb2.entityEnter()
	entityEnter.iEttId = who.iRoleId
	entityEnter.iEttType = who.ettType()
	entityEnter.sSerializedEtt = getSerializedEtt(who)
	entityEnter.iX = who.x
	entityEnter.iY = who.y
	entityEnter.iSceneId = who.sceneId
	return entityEnter

# def getEntityChange(who, roleInfo): # 改变实体属性
# 	who.sSerialized1 = None # 清缓存
# 	entityChange = scene_pb2.entityChange()
# 	entityChange.iEttId = who.iRoleId
# 	entityChange.iEttType = who.ettType()
# 	entityChange.sSerializedEtt = roleInfo.SerializeToString()
# 	return entityChange

def getEntityRoleInfo():
	'''实体的玩家消息体
	'''
	return scene_pb2.roleInfo()

def getSerializedEtt(who):  # 实体消息体的玩家信息部分
	if who.sSerialized1 is None:
		roleInfo = getEntityRoleInfo()
		roleInfo.shape = who.shape
		roleInfo.shapeParts.extend(who.shapeParts)
		roleInfo.colors.extend(who.getColors())
		roleInfo.name = who.name
		roleInfo.level = who.level
		roleInfo.school = who.school
		roleInfo.guildName = who.getGuildName()
		roleInfo.guildId = who.getGuildId()
		teamObj = who.getTeamObj()
		roleInfo.teamId = 0 if not teamObj else teamObj.id
		roleInfo.addon = who.getAddon()
		roleInfo.teamState = who.getTeamState()
		roleInfo.title = who.title()
		roleInfo.titleEffect = who.titleEffect()
		roleInfo.action = who.action
		rideObj = who.rideCtn.getRindCurrent()
		if rideObj:
			roleInfo.rideShape = rideObj.shape
			roleInfo.rideShapePart.extend(rideObj.shapeParts) #= rideObj.shapeParts
			roleInfo.rideColors.extend(rideObj.getColors())# = rideObj.getColors()
		else:
			roleInfo.rideShape = 0
		who.sSerialized1 = roleInfo.SerializeToString()
	return who.sSerialized1


def makeAttrInitMsg(who):  # 生成初始化角色属性msg
	msg = {}
	
	msg["roleId"] = who.id
	msg["zoneId"] = config.ZONE_ID
	msg["zoneNo"] = config.ZONE_NO
	msg["zoneName"] = misc.zoneName()  # 在pc端时,显示到标题栏
	msg["name"] = who.name
	
	msg["level"] = who.level
	msg["exp"] = who.exp
	msg["expNext"] = who.expNext
	
	msg["cash"] = who.cash
	msg["tradeCash"] = who.tradeCash
	msg["moneyCash"] = who.moneyCash
	
	msg["hp"] = who.hp
	msg["hpMax"] = who.hpMax
	msg["mp"] = who.mp
	msg["mpMax"] = who.mpMax
	
	msg["con"] = who.con
	msg["mag"] = who.mag
	msg["str"] = who.str
	msg["res"] = who.res
	msg["spi"] = who.spi
	msg["dex"] = who.dex
	
	msg["phyDam"] = who.phyDam
	msg["magDam"] = who.magDam
	msg["phyDef"] = who.phyDef
	msg["magDef"] = who.magDef
	
	msg["spe"] = who.spe  # 速度
	msg["cure"] = who.cure  # 治疗强度

	msg["phyCrit"] = who.phyCrit
	msg["magCrit"] = who.magCrit
	msg["phyReCrit"] = who.phyReCrit
	msg["magReCrit"] = who.magReCrit
	msg["sealHit"] = who.sealHit
	msg["reSealHit"] = who.reSealHit

	msg["sp"] = who.sp  # 愤怒
	msg["spMax"] = who.spMax  # 愤怒上限

	msg["huoli"] = who.huoli  # 活力
	msg["huoliMax"] = who.huoliMax  # 活力上限

	msg["point"] = who.point
	msg["school"] = who.school
	msg["shape"] = who.shape
	msg["shapeParts"] = who.shapeParts
	msg["colors"] = who.getColors()

	msg['reserveHp'] = who.reserveHp  # 储备生命
	msg['reserveMp'] = who.reserveMp  # 储备真气
	
# 	msg["autoFight"] = who.isAutoFight()
# 	msg["defaultPerform"] = who.getDefaultPerform()
	
	msg["addon"] = who.getAddon() # 附加状态
	
	msg["capacity"] = who.getCapacity()
	msg["fightPower"] = who.fightPower

	msg["pointScheme"] = who.getPointScheme()

	msg["demonPoint"] = who.fetch("demonPoint")
	msg["schoolPoint"] = who.fetch("schoolPoint")
	msg["guildPoint"] = who.fetch("guildPoint")
	msg["holidayPoint"] = who.fetch("holidayPoint")
	msg["masterPoint"] = who.fetch("masterPoint")
	msg["pkPoint"] = who.fetch("pkPoint")
	msg["helpPoint"] = who.fetch("helpPoint")
	msg["gender"] = who.gender
	msg["title"] = who.title()
	msg["titleEffect"] = who.titleEffect()
	msg["guildId"] = who.getGuildId()
	msg["guildName"] = who.getGuildName()
	msg["flowerPoint"] = who.getFlowerPoint()
	msg["tougheningExp"] = who.getTougheningExp()
	rideObj = who.rideCtn.getRindCurrent()
	if rideObj: 
		msg["rideShape"] = rideObj.shape
		msg["rideShapePart"] = rideObj.shapeParts
		msg["rideColors"] = rideObj.getColors()
	
	return msg

def send(iRoleId, sPacket):
	ep = mainService.getEndPointByRoleId(iRoleId)
	if ep:		
		ep.send(sPacket)

# 如果在循环中调用此函数,并且sMethodName,tArgs,dArgs参数总是相同的,做法错误.
# 应改用下面的broadcastByIds广播函数,避免重复序列化消息	
# def rpcCall(iRoleId,sMethodName,*tArgs,**dArgs):
# 	ep=mainService.getEndPointByRoleId(iRoleId)
# 	if not ep:
# 		return
# 	func=getattr(ep,sMethodName)
# 	return func(*tArgs,**dArgs)

def worldBroadcast(sMethodName, oMsg):  # 世界广播(只序列化一次消息)
	sPacket = endPoint.makePacket(sMethodName, oMsg)
	for iUid, ep in mainService.gRoleIdMapEndPoint.getAll().iteritems():
		ep.send(sPacket)

def broadcastByIds(itIds, sMethodName, oMsg):  # 根据id进行组播(只序列化一次消息)
	sPacket = endPoint.makePacket(sMethodName, oMsg)
	for iUid in itIds:
		ep = mainService.getEndPointByRoleId(iUid)
		if not ep:
			continue
		ep.send(sPacket)		

import copy
import weakref
import types
import gevent
import factoryConcrete
import log
import block.blockLazy
import endPoint
import role_pb2
import common_pb2
import scene
import misc
import role
import u
import mainService
import resume
import mail
import config
import scene_pb2
import ride.service
import rideData
import template