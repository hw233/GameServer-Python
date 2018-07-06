#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import role_pb2
import endPoint
import universal.public_pb2

def handleLock(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		import role.roleConfig
		if role.roleConfig.isLock(who):
			who.endPoint.rpcSecurityUnlock()
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			raise
	return newFunc

#角色服务
class cService(role_pb2.terminal2main):	
	@endPoint.result
	@handleLock
	def rpcResetPoint(self,ep,who,reqMsg):return rpcResetPoint(who,reqMsg)#洗属性点

	@endPoint.result
	@handleLock
	def rpcConfirmResetPoint(self,ep,who,reqMsg):return rpcConfirmResetPoint(who,reqMsg)#确认加点方案

	@endPoint.result
	def rpcReqCalculator(self,ep,who,reqMsg):return rpcReqCalculator(who,reqMsg)#请求属性计算器

	@endPoint.result
	def rpcSwitchScheme(self,ep,who,reqMsg):return rpcSwitchScheme(who,reqMsg)#请求属性计算器

	@endPoint.result
	def rpcSchemeInfo(self,ep,who,reqMsg):return rpcSchemeInfo(who,reqMsg)#查看某个方案的分配方案

	@endPoint.result
	def rpcReqAttrPoint(self,ep,who,reqMsg):return rpcReqAttrPoint(who,reqMsg)#更新分配点数

	@endPoint.result
	def rpcResetName(self, ep, who, reqMsg):return rpcResetName(who, reqMsg)

	@endPoint.result
	def rpcSecurityLockOperate(self, ep, who, reqMsg):return rpcSecurityLockOperate(who, reqMsg)

	@endPoint.result
	def rpcWork(self, ep, who, reqMsg):return rpcWork(who, reqMsg)

	@endPoint.result
	def rpcRoleInfoGet(self, ep, who, reqMsg):return rpcRoleInfoGet(who, reqMsg)
	

def rpcReqAttrPoint(who, reqMsg):#更新分配点数
	oMsg = role_pb2.attrPointInfo()
	attrPointMsg(who, oMsg)
	who.endPoint.rpcRespAttrPointInfo(oMsg)

def attrPointMsg(who, oMsg, oScheme=None, bCurScheme=True):
	oMsg.pointSchemeNo = who.schemeCtn.getCurSchemeNo()
	#当前正在使用的方案
	curScheme = who.schemeCtn.getScheme()
	#绿色
	oMsg.con=who.con-curScheme.fetch('con',0)
	oMsg.mag=who.mag-curScheme.fetch('mag',0)
	oMsg.str=who.str-curScheme.fetch('str',0)
	oMsg.res=who.res-curScheme.fetch('res',0)
	oMsg.spi=who.spi-curScheme.fetch('spi',0)
	oMsg.dex=who.dex-curScheme.fetch('dex',0)

	if not oScheme and bCurScheme:
		oScheme=curScheme

	#print '=======oMsg.mag==========',oMsg.mag,who.mag,oScheme.fetch('mag',0)
	#分配的：橙色
	oMsg.conAllot=oScheme.fetch('con',0) if oScheme else 0
	oMsg.magAllot=oScheme.fetch('mag',0) if oScheme else 0
	oMsg.strAllot=oScheme.fetch('str',0) if oScheme else 0
	oMsg.resAllot=oScheme.fetch('res',0) if oScheme else 0
	oMsg.spiAllot=oScheme.fetch('spi',0) if oScheme else 0
	oMsg.dexAllot=oScheme.fetch('dex',0) if oScheme else 0

	oMsg.pointScheme=oScheme.fetch('point',0) if oScheme else who.level*5


#查看加点方案
def rpcSchemeInfo(who,reqMsg):
	iScheNo=reqMsg.iValue
	ep=who.endPoint
	if not 1<=iScheNo<=3:
		print '方案不能为{}'.format(iScheNo)
		return universal.public_pb2.fail()
	if iScheNo==2 and who.level<40:
		ep.rpcTips('40级解锁第2套加点方案')
		return universal.public_pb2.fail()
	if iScheNo==3 and who.level<90:
		ep.rpcTips('90级解锁第3套加点方案')
		return universal.public_pb2.fail()

	oMsg=role_pb2.attrPointInfo()
	oMsg.pointSchemeNo=iScheNo
	oScheme=who.schemeCtn.getScheme(iScheNo)
	
	if not oScheme:
		oMsg.pointScheme=who.level*5
	else:
		# oMsg.conScheme=oScheme.fetch('con',0)
		# oMsg.magScheme=oScheme.fetch('mag',0)
		# oMsg.strScheme=oScheme.fetch('str',0)
		# oMsg.resScheme=oScheme.fetch('res',0)
		# oMsg.spiScheme=oScheme.fetch('spi',0)
		# oMsg.dexScheme=oScheme.fetch('dex',0)
		oMsg.pointScheme=oScheme.fetch('point',0)
	
	attrPointMsg(who, oMsg, oScheme, bCurScheme=False)
	ep.rpcRespAttrPointInfo(oMsg)
	


#开启加点方案
def rpcSwitchScheme(who,reqMsg):
	print 'role.service.rpcSwitchScheme'
	ep=who.endPoint
	iScheNo=reqMsg.iValue
	if not 1<=iScheNo<=3:
		print '方案不能为{}'.format(iScheNo)
		return False
	if iScheNo==2 and who.level<40:
		ep.rpcTips('40级解锁第2套加点方案')
		return False
	if iScheNo==3 and who.level<90:
		ep.rpcTips('90级解锁第3套加点方案')
		return False
	who.schemeCtn.switchScheme(iScheNo,who.level)
	who.attrChange('point', "pointScheme")
	who.reCalcAttr()
	
	oMsg = role_pb2.attrPointInfo()
	attrPointMsg(who, oMsg)
	who.endPoint.rpcRespAttrPointInfo(oMsg)


def _calAppendAttr(who, attr):
	school = who.school
	level = who.level
	val = who.applyMgr.query(attr)
	val += role.defines.getSchoolApply(school, attr) * level  # 门派额外附加
	return max(0, int(val))

def rpcReqCalculator(who,reqMsg):#请求属性计算器
	msg=role_pb2.attrPointInfo()
	msg.pointSchemeNo = who.schemeCtn.getCurSchemeNo()
	#气血附加
	msg.hpAppend = _calAppendAttr(who, "hpMax")
	#魔法附加		
	msg.mpAppend = _calAppendAttr(who, "mpMax")	
	#物理伤害附加
	msg.phyDamAppend = _calAppendAttr(who, "phyDam")
	#法术伤害附加
	msg.magAppend = _calAppendAttr(who, "magDam")
	#物理防御附加	
	msg.phyDefAppend = _calAppendAttr(who, "phyDef")
	#法术防御附加
	msg.magDefAppend = _calAppendAttr(who, "magDef")
	#速度附加	
	msg.speAppend = _calAppendAttr(who, "spe")
	#治疗强度附加
	msg.cureAppend = _calAppendAttr(who, "cure")

	oScheme=who.schemeCtn.getScheme()
	msg.pointScheme = oScheme.fetch("point")

	#oMsg = msg.curAttrPoint.add()
	#attrPointMsg(who, oMsg)

	who.endPoint.rpcRespAttrPointInfo(msg)
	# msg.hpMaxCalc.iCon=iCon
	# msg.hpMaxCalc.iMag=iMag
	# msg.hpMaxCalc.iStr=iStr
	# msg.hpMaxCalc.iRes=iRes
	# msg.hpMaxCalc.iSpi=iSpi
	# msg.hpMaxCalc.iDex=iDex
	# iCon=who.applyMgr.query('con')
	# iMag=who.applyMgr.query('mag')
	# iStr=who.applyMgr.query('str')
	# iRes=who.applyMgr.query('res')
	# iSpi=who.applyMgr.query('spi')
	# iDex=who.applyMgr.query('dex')

	# iConRatio=who.applyMgr.query('conRatio')
	# iMagRatio=who.applyMgr.query('magRatio')
	# iStrRatio=who.applyMgr.query('strRatio')
	# iResRatio=who.applyMgr.query('resRatio')
	# iSpiRatio=who.applyMgr.query('spiRatio')
	# iDexRatio=who.applyMgr.query('dexRatio')

	# iSchool=who.school
	# iLevel=who.level
	# oScheme=who.schemeCtn.getScheme()

	# fBase=100.0
	# msg=role_pb2.attrCalculator()
	# msg.iCurScheme=who.schemeCtn.getCurSchemeNo()#当前正在使用的方案编号

	# msg.hpMaxCalc.iAddend=who.applyMgr.query('hpMax') + int(role.defines.getSchoolApply(iSchool, 'hpMax') * iLevel)
	# msg.hpMaxCalc.fFactor=(who.applyMgr.query('hpMaxRatio')+1000.0)/1000.0
	# msg.hpMaxCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (con*8+50+iAddend)*factor end'

	# msg.mpMaxCalc.iAddend=who.applyMgr.query('mpMax') + int(role.defines.getSchoolApply(iSchool, 'mpMax') * iLevel)
	# msg.mpMaxCalc.fFactor=(who.applyMgr.query('mpMaxRatio')+1000.0)/1000.0
	# msg.mpMaxCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (mag*1+level*5+200+iAddend)*factor end'

	# msg.phyDamCalc.iAddend=who.applyMgr.query('phyDam') + int(role.defines.getSchoolApply(iSchool, 'phyDam') * iLevel)
	# msg.phyDamCalc.fFactor=(who.applyMgr.query('phyDamRatio')+fBase)/fBase
	# msg.phyDamCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (str*1+20+level*1+iAddend)*factor end'

	# msg.magDamCalc.iAddend=who.applyMgr.query('magDam') + int(role.defines.getSchoolApply(iSchool, 'magDam') * iLevel)
	# msg.magDamCalc.fFactor=(who.applyMgr.query('magDamRatio')+fBase)/fBase
	# msg.magDamCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (mag*1+20+level*1+iAddend)*factor end'

	# msg.phyDefCalc.iAddend=who.applyMgr.query('phyDef') + int(role.defines.getSchoolApply(iSchool, 'phyDef') * iLevel)
	# msg.phyDefCalc.fFactor=(who.applyMgr.query('phyDefRatio')+fBase)/fBase
	# msg.phyDefCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (res*2+iAddend)*factor end'

	# msg.magDefCalc.iAddend=who.applyMgr.query('magDef') + int(role.defines.getSchoolApply(iSchool, 'magDef') * iLevel)
	# msg.magDefCalc.fFactor=(who.applyMgr.query('magDefRatio')+fBase)/fBase
	# msg.magDefCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (spi*2+iAddend)*factor end'		

	# msg.speCalc.iAddend=who.applyMgr.query('spe') + int(role.defines.getSchoolApply(iSchool, 'spe') * iLevel)
	# msg.speCalc.fFactor=(who.applyMgr.query('speRatio')+fBase)/fBase
	# msg.speCalc.sExpression='function(con,mag,str,res,spi,dex,level,iAddend,factor)return (con*0.2+mag*0.2+str*0.2+res*0.2+spi*0.2+dex*1.5+iAddend)*factor end'

	# msg.conBase=who.con-oScheme.fetch('con',0)
	# msg.magBase=who.mag-oScheme.fetch('mag',0)
	# msg.strBase=who.str-oScheme.fetch('str',0)
	# msg.resBase=who.res-oScheme.fetch('res',0)
	# msg.spiBase=who.spi-oScheme.fetch('spi',0)
	# msg.dexBase=who.dex-oScheme.fetch('dex',0)

	# who.endPoint.rpcRespCalculator(msg)

def rpcResetPoint(who,reqMsg):#洗属性点
	print 'role.service.rpcResetPoint'
	#iScheNo=who.schemeCtn.getCurSchemeNo() #第几套方案
	iLv=40
	if who.level<iLv:
		message.tips(who, '#C04{}级#n开启#C04洗点#n功能'.format(iLv))
		return False

	sAttr = reqMsg.attr
	#print '=======rpcResetPoint=======',sAttr
	oScheme=who.schemeCtn.getScheme()
	if not oScheme:
		return

	if sAttr == "all":#重置所有属性
		propsNo = 202011#propsMap[sAttr]
		if sum(who.propsCtn.getPropsAmountByNos(propsNo)) <= 0:
			message.tips(who, '没有重置道具')
			return

		pointSum = 0
		for sAttr in role.defines.baseAttrList:
			pointSum += oScheme.fetch(sAttr,0)
			oScheme.set(sAttr, 0)

		if pointSum <= 0:
			message.tips(who, '可重置点数为0')
			return

		who.propsCtn.subPropsByNo(propsNo, 1, "洗点")
		oScheme.add('point',pointSum)

	else:
		propsMap = {
			"con":202012, 
			"mag":202014,
			"str":202013,
			"res":202015,
			"spi":202016,
			"dex":202017,
			#"all":202011
		}
		if sAttr not in propsMap.keys():
			return
		
		propsNo = propsMap[sAttr]
		if sum(who.propsCtn.getPropsAmountByNos(propsNo)) <= 0:
			message.tips(who, '没有重置道具')
			return
		#print "===oScheme.fetch(sAttr,0)= ", oScheme.fetch(sAttr,0)
		if oScheme.fetch(sAttr,0) <= 0:
			message.tips(who, '该属性可重置点数为0')
			return

		who.propsCtn.subPropsByNo(propsNo, 1, "洗点")
		point = min(2, oScheme.fetch(sAttr,0))
		oScheme.add(sAttr, -point)
		oScheme.add('point',point)
	who.reCalcAttr()
	who.attrChange('point',)

	oMsg = role_pb2.attrPointInfo()
	attrPointMsg(who, oMsg)
	who.endPoint.rpcRespAttrPointInfo(oMsg)
	
	
def rpcConfirmResetPoint(who,reqMsg):#确定加点
	print 'role.service.rpcConfirmResetPoint'
	iScheNo=reqMsg.pointSchemeNo #第几套方案
	iCon=reqMsg.con
	iMag=reqMsg.mag
	iStr=reqMsg.str
	iRes=reqMsg.res
	iSpi=reqMsg.spi
	iDex=reqMsg.dex
	oScheme=who.schemeCtn.getScheme(iScheNo)
	iSum=iCon+iMag+iStr+iRes+iSpi+iDex

	if iSum==0 or iCon<0 or iMag<0 or iStr<0 or iRes<0 or iSpi<0 or iDex<0:
		return False

	oScheme=who.schemeCtn.getScheme(iScheNo)
	if iSum>oScheme.fetch('point'):
		message.tips(who, '潜力点不足')
		return False

	oScheme.add('con',iCon)
	oScheme.add('mag',iMag)
	oScheme.add('str',iStr)
	oScheme.add('res',iRes)
	oScheme.add('spi',iSpi)
	oScheme.add('dex',iDex)

	oScheme.add('point',-iSum)
	who.reCalcAttr()

	who.attrChange('point', 'pointScheme')

	oMsg = role_pb2.attrPointInfo()
	attrPointMsg(who, oMsg)
	who.endPoint.rpcRespAttrPointInfo(oMsg)

def rpcResetName(who, reqMsg):
	'''角色改名
	'''
	roleId = reqMsg.roleId
	propsId = reqMsg.propsId
	mode = reqMsg.mode
	nameNew = reqMsg.name
	if roleId != who.id or mode != 1:
		return
	propsObj = who.propsCtn.getItem(propsId)
	if not propsObj:
		message.tips(who, "你身上没有此物品")
		return
	propsNo = propsObj.no()
	if propsNo not in (202040, 202041):
		message.tips(who, "改名道具不足")
		return
	iLen = common.calLen(nameNew)
	if iLen > 6:
		message.tips(who, "名字不能大于#C046个#n字，改名失败，请重新输入")
		return
	elif iLen < 2:
		message.tips(who, "名字不能少于#C042个#n字")
		return
	if trie.fliter(nameNew) != nameNew or u.isInvalidText(nameNew):
		message.tips(who, "名字不符合规定，改名失败，请重新输入")
		return
	nameOld = who.name
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oMsg = oCenterEP.rpcUpdateName(roleId, nameNew, nameOld)
	if bFail:
		message.tips(who, "中心服无回应，改名失败")
		return
	elif not oMsg.bValue:
		message.tips(who, "此名字已有玩家使用")
		return
	who = common.getRole(roleId)
	if not who:
		return
	propsName = propsObj.name
	who.propsCtn.addStack(propsObj, -1)
	common.writeLog("role/rename", "%d %d(%d) %s->%s" % (who.id, propsNo, propsId, nameOld, nameNew))
	who.name = nameNew
	who.attrChange("name")
	# TODO 通知好友
	message.tips(who, "你已成功改名！")
	rpcReNameNotify(who, 0, 2)
	if propsNo == 202041:
		message.sysMessage("#C01{}#n使用{}将昵称修改为#C01{}#n".format(nameOld, propsObj.getHyperLink(), nameNew))
	rank.roleChangeInfo(who)
	guild.updateMemberInfo(who)

def rpcWork(who, reqMsg):
	if who.huoli < 100 :
		message.tips(who, "活力不足，无法打工" )
		return
	who.addHuoli(-100,"打工赚钱")
	who.rewardTradeCash(100,"打工赚钱","你辛苦打工获得了#IG#n#C02100#n")

def rpcRoleInfoGet(who, reqMsg):
	roleId = reqMsg.roleId
	roleObj = getRole(roleId)
	info = {}
	if roleObj:
		info["shape"] = roleObj.shape
		info["name"] = roleObj.name
		info["level"] = roleObj.level
		info["addon"] = roleObj.getAddon()
		info["school"] = roleObj.school
		info["online"] = True
		teamObj = roleObj.getTeamObj()
		if teamObj:
			info["teamId"] = teamObj.id
			info["teamMemberNum"] = len(teamObj.getOnlineList())
		guildObj = roleObj.getGuildObj()
		if guildObj:
			info["guildId"] = guildObj.id
			info["guildName"] = guildObj.name
	else:
		resumeObj = resume.getResume(roleId)
		if resumeObj:
			info["shape"] = resumeObj.shape
			info["name"] = resumeObj.name
			info["level"] = resumeObj.level
			info["school"] = resumeObj.school
			info["online"] = False
			if resumeObj.guildId:
				info["guildId"] = resumeObj.guildId
				info["guildName"] = resumeObj.guildName
		else:
			oFriend = who.friendCtn.getFriend(roleId)
			if oFriend:
				info["shape"] = oFriend.shape
				info["name"] = oFriend.name
				info["level"] = oFriend.level
				info["school"] = oFriend.school
				info["online"] = oFriend.isOnline()
	
	roleInfo = role_pb2.roleInfoRes()
	roleInfo.roleId = roleId
	roleInfo.clientTag = reqMsg.clientTag
	for attrName, attrVal in info.iteritems():
		setattr(roleInfo, attrName, attrVal)

	who.endPoint.rpcRoleInfoSend(roleInfo)

def rpcReNameNotify(who, propsId, mode):
	'''角色改名通知
	'''
	msg = role_pb2.resetName()
	msg.roleId = who.id
	msg.propsId = propsId
	msg.mode = mode
	who.endPoint.rpcReNameNotify(msg)

def rpcSecurityLockOperate(who, reqMsg):
	'''安全锁相关操作
	'''
	iOp = reqMsg.iOp
	if not iOp:
		return
	oArgs = reqMsg.opArgs
	bResult = role.roleConfig.handleSecurityLock(who, iOp, oArgs)
	rpcSecurityLockOperateRes(who, iOp, bResult)
	rpcSecurityLockMsg(who)

def rpcSecurityLockMsg(who):
	'''下发安全锁状态
	'''
	msg = role_pb2.lockMsg()
	msg.iLock = role.roleConfig.getLockStatus(who)
	iApplyTime, iEndTime = role.roleConfig.getForceUnlockTime(who)
	if iApplyTime:
		msg.iApplyTime = iApplyTime
		msg.iEndTime = iEndTime
	who.endPoint.rpcSecurityLockMsg(msg)

def rpcSecurityLockOperateRes(who, iOp, bResult):
	'''下发安全锁操作结果
	'''
	msg = role_pb2.lockOperate()
	msg.iOp = iOp
	msg.bRes = bResult
	who.endPoint.rpcSecurityLockOperateRes(msg)


from common import *
import config
import role.defines
import message
import role_pb2

import role
import c
import u
import rank
import log
import resume
# import misc
# import gevent
# import timeU
import common
import trie
import client4center
import role.roleConfig
import guild
