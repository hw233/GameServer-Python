# -*- coding: utf-8 -*-
'''帮派系统
'''
def init():
	'''初始化公会数据
	'''
	import productKeeper
	import factoryConcrete
	import db4ms
	import timerEvent
	import role
	global gGuildKeeper
	global gGuildName
	gGuildKeeper = productKeeper.cProductkeeper(factoryConcrete.guildFtr)
	gGuildName = set()

	rs = db4ms.gConnectionPool.query(GUILD_SQL)
	for data in rs.rows:
		guildId = data[0]
		guildObj = gGuildKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, guildId)
		gGuildName.add(guildObj.name)
	timerEvent.geNewWeek += onNewWeek
	timerEvent.geNewDay += onNewDay
	timerEvent.geNewHour += onNewHour
	timerEvent.geNewMinu += onNewMinu
	role.geOffLine += roleOffLine
	
def getGuildList():
	'''获取全部帮派列表
	'''
	return gGuildKeeper.getIterValues()

def onNewWeek(year, month, day, hour, wday):
	for guildObj in gGuildKeeper.getIterValues():
		guildObj.onNewWeek()

def onNewDay(year, month,day, hour, wday):
	for guildObj in gGuildKeeper.getValues():
		guildObj.onNewDay(year, month, day, hour, wday)

def onNewHour(year, month, day, hour, wday):
	now = getSecond()
	for guildObj in gGuildKeeper.getIterValues():
		guildObj.onNewHour(now)

def onNewMinu():
	for guildObj in gGuildKeeper.getIterValues():
		guildObj.onNewMinu()

def roleOffLine(who):
	updateMemberInfo(who, False)

def getGuild(guildId):
	'''获取帮派
	'''
	return gGuildKeeper.getObj(guildId)

def newGuild(guildId, guildName, guildTenet, chairmanId):
	'''创建帮派
	'''
	guildObj = gGuildKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY, guildId, name=guildName, tenet=guildTenet, chairmanId=chairmanId)
	gGuildName.add(guildObj.name)
	return guildObj

def dismissGuild(guildId):
	'''解散帮派
	'''
	oGuild = getGuild(guildId)
	if not oGuild:
		return
	gGuildName.discard(oGuild.name)
	oGuild.dismiss()
	gGuildKeeper.removeObj(oGuild.id)

def newMember(who, job):
	'''创建成员
	'''
	memberObj = guild.object.Member(who.id)
	memberObj.updateInfo(who)
	memberObj.setJob(job)
	return memberObj

def newMemberByData(memberData):
	'''根据数据创建成员，用于离线入帮
	'''
	roleId = memberData["roleId"]
	memberObj = guild.object.Member(roleId)
	memberObj.set("name", memberData["name"])
	memberObj.set("level", memberData["level"])
	memberObj.set("school", memberData["school"])
	memberObj.set("shape", memberData["shape"])
	# memberObj.set("shapeParts", memberData["shapeParts"])
	# memberObj.set("colors",memberData["colors"])
	return memberObj

def updateMemberInfo(who, isLogin=True):
	'''更新成员信息
	'''
	guildId = who.getGuildId()
	if not guildId:
		return
	
	guildObj = getGuild(guildId)
	if not guildObj:
		return
	
	memberObj = guildObj.getMember(who.id)
	if memberObj:
		memberObj.updateInfo(who, guildObj)
		memberObj.setLogin(isLogin, guildObj)
	
	

def onUpLevel(who):
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if not oMember:
		return
	if oGuild.checkCanUpdate(oMember,getSecond()):
		oMember.setJob(GUILD_JOB_COMMON)

def onQuitGuild(who):
	'''退出帮派后续处理逻辑
	'''
	taskObj = task.hasTask(who, 30201)
	if taskObj:
		task.removeTask(who, taskObj.id)
	actObj = activity.getActivity("guildMaze")
	if actObj.getRoleInfoByKey(who.id, "inGame") == 1:
		actObj.leaveScene(who)


from common import *
from guild.defines import *
import factory
import guild.object
import task
import activity

'''
import block
import pst
import misc
import cycleData
import sceneMng

NO_GUILD_ID=0#没有加入公会时候的公会id
GUILD_LIMIT_LV = 12	#公会限制等级
GUILD_COST_DIAMOND = 1000 	#创建公会消耗 GUILD_COST_DIAMOND 钻石
INIT_EGSIGN = 77 	#默认会徽
MAX_MEMBERS = 10
MAX_SENIOR	= 2
LOG_AMOUNT = 8	#最大日志数量
LOG_COLOR = 9	#日志颜色
MAX_WORK_TIME = 5	#每日打工次数

MSG_BRIEF = ('id', 'name', 'ensign', 'notice')
MSG_DETAIL = MSG_BRIEF + ('members','log','apply')
MSG_SEARCH = MSG_BRIEF + ('fight', )

class cGuildCycDay(cycleData.cCycDay):
	pass 

class cScene(sceneMng.cTempScene):
	def hasPass(self):
		return False

class cGuild(pst.cEasyPersist, block.cBlock):
	def __init__(self, iGuildId):
		pst.cEasyPersist.__init__(self,self._dirtyEventHandler)
		block.cBlock.__init__(self,'公会数据块',iGuildId)
		self.iGuildId = iGuildId

		self.sName = ''				#名字
		self.iEnsign = INIT_EGSIGN	#会徽
		self.iOwnerId = 0			#会长ID
		self.lMemberIds = []		#会员IDS
		self.lSeniorIds = []		#公会长老ID列表 [ID]
		self.iFightAbility = 0		#公会最低战力
		self.sNotice = ''			#公会宣言
		self.level = 1				#公会等级
		self.iExp = 0				#公会经验
		self.sApplyJoinSet = set()	#申请加入公会的角色ID
		self.lLogList = []			#公会日志
		self.dLuckStone = {}		#幸运石属性{角色ID:幸运石数量}
		self.iForceSetPe = 0		#强制设置会长
		self.dAddStamp = {}			#加入时间戳
		self.sEnsign = set()		#已拥有的会徽集合
		self.day = cGuildCycDay(2, self._dirtyEventHandler)	#天周期数据

		#缓存属性数据,避免重复加载resume
		self.dMemberAttrs = {}		#成员属性  {roleId : {'name':名字, 'vip':vip等级, 'fight':战力, 'active':活跃度, 'lv':等级, "school":职业} }
		self.dApplyAttrs =	{}		#申请加入角色属性
		self.dMemberProtoMsg = {}	#序列化好的成员信息  guild_pb2.member
		self.bHasSort = False	
		self.iStone = 0				#公会幸运石
		self.oScene = None 			#公会场景	
		self.iNewX = self.iNewY = self.iSceneId = 0	#公会场景信息(ID,bornX,bornY)
		self.lStoneRank = []		#幸运石排行
		self.bHasRank = False		
		self.lNpc = []			
		self.setIsStm(sql.GUILD_INSERT).setUdStm(sql.GUILD_UPDATE).setSlStm(sql.GUILD_SELECT).setDlStm(sql.GUILD_DELETE)

	def save(self):
		dData = pst.cEasyPersist.save(self)
		dData['id'] = self.iGuildId
		if self.iEnsign != INIT_EGSIGN:
			dData['ensign'] = self.iEnsign
		if self.sName:
			dData['name'] = self.sName
		if self.iOwnerId:
			dData['owner'] = self.ownerId
		if self.lSeniorIds:
			dData['senior']	= self.lSeniorIds	
		if self.lMemberIds:
			dData['members'] = self.lMemberIds
		if self.iFightAbility:
			dData['ft'] = self.iFightAbility
		if self.sNotice:
			dData['notice'] = self.sNotice
		if self.level != 1:
			dData['level'] = self.level
		if self.sApplyJoinSet:
			dData['apply'] = list(self.sApplyJoinSet)
		if self.lLogList:
			dData['log'] = self.lLogList
		if self.iForceSetPe:
			dData['fsp'] = self.iForceSetPe
		if self.iExp:
			dData['exp'] = self.iExp
		if self.dLuckStone:
			dData['stone'] = self.dLuckStone
		if self.dAddStamp:
			dData['stmp'] = self.dAddStamp
		if self.sEnsign:
			dData['has_ensign'] = list(self.sEnsign)
		dCycData = self.day.save()
		if dCycData:
			dData['cyc'] = dCycData
		return dData

	def load(self, dData):
		pst.cEasyPersist.load(self, dData)
		self.iGuildId = dData.pop('id', 0)
		self.iEnsign = dData.pop('ensign', INIT_EGSIGN)
		self.sName = dData.pop('name', '')
		self.ownerId = dData.pop('owner', 0)
		self.lSeniorIds = dData.pop('senior', [])
		self.lMemberIds = dData.pop('members', [])
		self.iFightAbility = dData.pop('ft', 0)
		self.sNotice = dData.pop('notice', '')
		self.level = dData.pop('level', 1)
		self.sApplyJoinSet = set(dData.pop('apply', []))
		self.lLogList = dData.pop('log', [])
		self.iForceSetPe = dData.pop('fsp', 0)
		self.iExp = dData.pop('exp', 0)
		self.dAddStamp = dData.pop('stmp', {})
		self.sEnsign = set(dData.pop('has_ensign', []))
		self.dLuckStone = dData.pop('stone', {})
		self.iStone = sum(self.dLuckStone.values())
		self.day.load(dData.pop('cyc', {}))

	def isFull(self):#是否满员
		return len(self.lMemberIds) >= MAX_MEMBERS

	def getTitle(self, iRoleId):
		return 'title'

	def updateMemberAttr(self, oRole):	#更新成员属性
		iRoleId = oRole.id
		if iRoleId not in self.lMemberIds and iRoleId not in self.sApplyJoinSet:
			return
		self.__setMemberAttr( iRoleId, self.dMemberAttrs if (iRoleId in self.lMemberIds) else self.dApplyAttrs )

	def __setMemberAttr(self, iRoleId, dData):
		dAttr = dData.setdefault(iRoleId, {})
		#直接拉取resume,除了启服其他情况oResume都是在内存中的
		oResume = factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)	
		if not oResume:
			self.__onResumeLose(iRoleId)
			return
		dAttr['name'] = oResume.name
		dAttr['level'] = oResume.level
		dAttr['school'] = oResume.school
		dAttr['fight'] = oResume.fightAbility()

		dAttr['active'] = oResume.weekActivite()	#活跃度
		self.__makeProtoMsg(iRoleId, dData, True)
		self.bHasSort = False

	def getColorName(self, sRoleName):
		return sRoleName

	def removeMember(self, iRoleId, bForce = False):#退出公会,玩家主动操作
		if iRoleId not in self.lMemberIds:
			return False
		if self.isPresident(iRoleId) and self.memberAmount()>=2:
			return False

		if self.isSenior(iRoleId):
			self.lSeniorIds.remove(iRoleId)
		self.lMemberIds.remove(iRoleId)
		dAttr = self.dMemberAttrs.pop(iRoleId, 0)
		self.dLuckStone.pop(iRoleId, 0)
		self.dMemberProtoMsg.pop(iRoleId, 0)
		self.dAddStamp.pop(iRoleId, 0)

		self.bHasSort = False
		self.bHasRank = False	
		if self.memberAmount() == 0:
			self._deleteFromDB()	#成员数为0解散公会
			return True
		sLogs = '{}{}了公会'.format(self.getColorName(dAttr.get('name', '')), '被踢出了' if bForce else '离开了')
		self.addLogs(sLogs)
		self.markDirty()
		return True

	def _deleteFromDB(self):	#解散公会
		self.markDirty()
		gGuildKeeper.removeObj(self.iGuildId)
		block.cBlock._deleteFromDB(self)
		
	def addMember(self, iRoleId):	#加入成员
		self.lMemberIds.append(iRoleId)
		self.dAddStamp[iRoleId] = timeU.getStamp()
		self.__setMemberAttr(iRoleId, self.dMemberAttrs)
		sRoleName = self.dMemberAttrs.get(iRoleId, {}).get('name', '')
		if not self.isPresident(iRoleId):
			self.addLogs('{}加入了公会'.format(self.getColorName(sRoleName)))	#
		self.markDirty()
		oRole = role.gKeeper.getObj(iRoleId)
		if oRole:
			oRole.lazy.delete('ap_join')	#
			oRole.setGuildId(self.iGuildId)	#设置玩家关联公会
	
	def npcList(self):
		return self.lNpc

	def hasEnsign(self):
		return self.sEnsign

	def applyJoinSet(self):
		return copy.deepcopy(self.sApplyJoinSet)	#返回深拷贝

	def removeApplyJoinRole(self, iRoleId):
		if iRoleId not in self.sApplyJoinSet:
			return {}
		self.sApplyJoinSet.discard(iRoleId)
		self.dMemberProtoMsg.pop(iRoleId)
		return self.dApplyAttrs.pop(iRoleId, {})

	def clearApplyJoinRole(self):	#移除所有的入会申请
		sJoinSet = self.applyJoinSet()
		for iRoleId in sJoinSet:
			self.removeApplyJoinRole(iRoleId)	

	def addApplyJoinRole(self, oRole):
		iRoleId = oRole.id
		if iRoleId in self.sApplyJoinSet:
			return
		self.sApplyJoinSet.add(iRoleId)
		self.__setMemberAttr(iRoleId, self.dApplyAttrs)
		self.markDirty()

		#todo 向会长和长老们发送角色申请加入公会消息

		lApplyJoin = oRole.lazy.fetch('ap_join', [])	#ap_join  已经申请加入的公会ID
		lApplyJoin.append(self.iGuildId)
		oRole.lazy.set('ap_join', lApplyJoin)

	def changePosition(self, oRole,ep, iTargetRoleId, iTargetPosition):#oRole改变iRoleId的职位
		iRoleId, sTargetName = oRole.id, self.dMemberAttrs.get(iTargetRoleId, {}).get('name', '')
		if not self.isMember(iRoleId):
			ep.rpcTips('您不是公会成员,不能进行当前操作')
			return False
		if not self.isMember(iTargetRoleId):
			ep.rpcTips('对方不是公会成员,不能进行当前操作')
			return False
		iBasePosition = getGuildPosition(self, iTargetRoleId)
		if iTargetPosition == iBasePosition:
			ep.rpcTips('{}当前已是{},无需重新进行设置'.format(sTargetName, getStrGuildPosition(self, iTargetRoleId)))
			return False
		iPosition = getGuildPosition(self, iRoleId)	#
		if iPosition <= iTargetPosition and iPosition != guild_pb2.TYPE_CHAIRMAN:
			ep.rpcTips('权限不够,不能进行当前操作' )
			return False 
		if iTargetPosition == guild_pb2.TYPE_ELDER and len(self.lSeniorIds) == MAX_SENIOR:
			ep.rpcTips('长老最多只有{}名'.format(MAX_SENIOR) )
			return False
		dChangePosition = {	#下列四个函数不在进行权限检查,和正确性检查
			guild_pb2.TYPE_ELDER	:	'_setSenior',	#设置长老
			guild_pb2.TYPE_CHAIRMAN	:	'_setPresident',#设置会长
			guild_pb2.TYPE_MEM 		:	'_setMember',	#设为会员
			guild_pb2.TYPE_NOT_MEM	:	'_delMember',	#剔除会员	
		}	
		if iTargetPosition not in dChangePosition:
			ep.rpcTips('非法操作')
			return False
		if getattr(self, dChangePosition[iTargetPosition])(oRole, iTargetRoleId, iTargetPosition):
			self.dMemberProtoMsg.pop(iRoleId, None)
			self.dMemberProtoMsg.pop(iTargetRoleId, None)
			self.bHasSort = False
			self.markDirty()
			ep.rpcTips('操作成功')
			# if iBasePosition == guild_pb2.TYPE_ELDER:
			# 	self._setSenior(oRole, iRoleId, iBasePosition)	#设置为长老
			return True
		return False	

	def _setSenior(self, oRole, iTargetRoleId, iTargetPosition):#设置长老	
		self.lSeniorIds.append(iTargetRoleId)
		sName = self.dMemberAttrs.get(iTargetRoleId, {}).get('name', '')
		self.addLogs('{}被任命为长老'.format(self.getColorName(sName)))
		return True

	def _setPresident(self, oRole, iTargetRoleId, iTargetPosition):#设置会长
		iRoleId, sTargetName = oRole.id, self.dMemberAttrs.get(iTargetRoleId, {}).get('name', '')
		ep= mainService.getEndPointByRoleId(oRole.id)
		if not ep:
			return False
	 	bFail,uResponse=ep.rpcConfirmBox('设置会长','您确定将{}设置为会长?'.format(sTargetName),'Q_确定Q_取消')
		if bFail or uResponse.iValue != 0:
			return False	#操作超时
		if self.isSenior(iTargetRoleId):
			self.lSeniorIds.remove(iTargetRoleId)
		self.ownerId = iTargetRoleId
		return True

	def _setMember(self, oRole, iTargetRoleId, iTargetPosition):#设置会员
		if self.isSenior(iTargetRoleId):
			self.lSeniorIds.remove(iTargetRoleId)
		return True

	def _delMember(self, oRole, iTargetRoleId, iTargetPosition):#剔除会员
		iRoleId, sTargetName = oRole.id, self.dMemberAttrs.get(iTargetRoleId, {}).get('name', '')
		ep= mainService.getEndPointByRoleId(oRole.id)
		if not ep:
			return False
	 	bFail,uResponse = ep.rpcConfirmBox('踢出公会','您确定将{}踢出公会吗?'.format(sTargetName),'Q_确定Q_取消')
		if bFail or uResponse.iValue != 0:
			return False	#操作超时
		self.removeMember(iTargetRoleId, True)
		oTargetResume = resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iTargetRoleId)
		if not oTargetResume:
			raise Exception, '角色简要信息丢失,角色ID:{}'.format(iTargetRoleId)
		oTargetRole = role.gKeeper.getObj(iTargetRoleId)
		if oTargetRole:
			deleteRoleGuildId(oTargetRole, self.name, timeU.getStamp())
		else:
			oTargetResume.addLoginCall(resume.DELETEGUILDID, self.name, timeU.getStamp())
		return True		

	def setPresident(self, iRoleId, sRoleName):	#设置会长
		if self.ownerId == iRoleId:
			return
		if self.iForceSetPe != 0:	#作用只准此函数被调用一次
			return 
		self.iForceSetPe = 1
		self.ownerId = iRoleId
		self.addLogs('{}创建了公会'.format(self.getColorName(sRoleName)))	#
		self.markDirty()

	def isPresident(self, iRoleId):	#是否是会长
		return self.ownerId == iRoleId
	
	@property
	def id(self):
		return self.iGuildId	
		
	def memberAmount(self):
		return len(self.lMemberIds)	
	
	def isMember(self, iRoleId):	#是否是公会成员
		return iRoleId in self.lMemberIds

	def isSenior(self, iRoleId):	#是否是长老
		return iRoleId in self.lSeniorIds

	def addLv(self):
		self.level += 1
		self.markDirty()

	def maxStone(self):
		return 90	#最大幸运石 90

	def roleStone(self, iRoleId):
		return self.dLuckStone.get(iRoleId, 0)	
			
	def addStone(self, iRoleId, iAdd):
		self.iStone += iAdd
		self.dLuckStone[iRoleId] = self.roleStone(iRoleId)+iAdd
		self.bHasRank = False
		#处理超过最大幸运石
		if self.iStone >= self.maxStone():
			self.iStone -= self.maxStone()
			self.dLuckStone[iRoleId] -= self.iStone
			self.__sendStoneAward(iRoleId)	#公会幸运石分红
			self.dLuckStone.clear()
			self.dLuckStone[iRoleId] = self.iStone
			self.bHasRank = False
			self.markDirty()

	def __sendStoneAward(self, iLastRoleId):	#todo 
		print u.trans2gbk('幸运石分红')
		lTempIds = copy.deepcopy(self.lMemberIds)
		lTempIds.sort(self.__stoneSort)
		sLastGold = '\n最后一击奖励由{}获得!'.format(self.getColorName(self.dMemberAttrs.get(iLastRoleId, {}).get('name', '')))
		for iIdx, iRoleId in enumerate(lTempIds):
			iLvGold = self.dMemberAttrs.get(iRoleId, {}).get('lv', 1) * 2000
			iRankGold = guildData.getRankAward(iIdx+1)
			iLastGold = 200000 if iLastRoleId == iRoleId else 0 
			iTotalGold = iLvGold + iRankGold + iLastGold
			# print u.trans2gbk('公会幸运石积满！全公会所有成员获得一次奖励！\n你获得{}元宝.{}'.format(iTotalGold, sLastGold))
			#todo 当角色不在内存时,有以下三种方式发放奖励
			#1.如果角色不在线那写入resume等角色在线在发放邮件奖励???   todo 其实代价更大
			#2.在公会中缓存本次需要发放的数据,等角色上线在发放奖励???	todo 会引起公会数据块存盘
			#3.此处直接拉取邮箱写入邮件数据???      是不是公会hold角色的邮箱呢???	todo 
			mail.sendSysMail(iRoleId, '公会幸运石分红!', '公会幸运石积满！全公会所有成员获得一次奖励！\n你获得{}元宝.{}'.format(iTotalGold, sLastGold), None, *[(c.GOLD, iTotalGold)])	#发放击杀奖励

	def exp(self):
		return self.iExp

	def addExp(self, iAdd):	#增加经验
		self.iExp += iAdd
		if self.level == guildData.getMaxLv():	#满级了
			self.iExp == min(self.iExp, self.getLvAddr('exp', 10000))
			return
		while True:	#升级处理
			iNeedExp = self.getLvAddr('exp', 10000)
			if self.iExp < iNeedExp:
				break
			self.iExp -= self.getLvAddr('exp', 10000)
			self.addLv()
		self.markDirty()

	def fightAbility(self):
		return self.iFightAbility

	def setFightAbility(self, iFightAbility):
		self.iFightAbility = iFightAbility

	def notice(self):
		return self.sNotice	
		
	def setNotice(self, sNotice):
		if sNotice == self.sNotice:
			return
		self.sNotice = sNotice
		self.markDirty()
		return self

	def logs(self):
		return self.lLogList

	def addLogs(self, sLog):
		if not sLog:
			return 
		self.lLogList.append(sLog)
		if len(self.lLogList) >= LOG_AMOUNT:
			self.lLogList.pop(0)
		self.markDirty()

	@property
	def name(self):	#名字
		return self.sName
	
	@name.setter
	def name(self, name):
		if self.sName == name:
			return
		self.sName = name
		self.markDirty()

	def ensign(self):	#会徽
		return self.iEnsign

	def setEnsign(self, iEnsign):
		if self.iEnsign == iEnsign:
			return self
		self.sEnsign.add(iEnsign)
		self.iEnsign = iEnsign
		self.markDirty()
		return self

	def getLvAddr(self, sKey, uDefault=0):
		return guildData.getLvAddr(self.level, sKey, uDefault) 

	def getWorkTimes(self, iRoleId):
		return self.day.fetch('times', {}).get(iRoleId, MAX_WORK_TIME)	#剩余次数

	def addWorkTimes(self, iRoleId, iTimes = 1):
		dTimes = self.day.fetch('times', {})
		dTimes[iRoleId] = self.getWorkTimes(iRoleId) - iTimes
		self.day.set('times', dTimes)
		self.markDirty()

	def getChangeWorkTimes(self, iRoleId):	#换工作的次数
		return self.day.fetch('ch_times', {}).get(iRoleId, 0)

	def addChangeWorkTime(self, iRoleId):	#增加换工作的次数
		dTimes = self.day.fetch('ch_times', {})
		dTimes[iRoleId] = dTimes.get(iRoleId, 0) + 1
		self.day.set('ch_times', dTimes)
		self.markDirty()
		
	def getWorkInfo(self, iRoleId):	#公会打工信息
		workMsg = guild_pb2.workMsg()
		workMsg.iLevel = self.level			
		workMsg.iAddRota = self.getLvAddr('addRation', 1)		#收入加成
		workMsg.iExp = self.exp()	
		workMsg.iNeedExp = self.getLvAddr('exp', 10000)			#升级所需经验
		workMsg.iLuckStone = self.iStone						#当前幸运石
		workMsg.iNeedStone = self.maxStone()		#
		workMsg.lStoneMsg.extend(self.__getStoneRank())			#幸运石排名信息
		workMsg.iMyStone = self.dLuckStone.get(iRoleId, 0)
		workMsg.iRemainTimes = self.getWorkTimes(iRoleId)
		return workMsg

	def __makeStoneRank(self):
		lTempIds, lStoneIds = self.dLuckStone.keys(), []
		lTempIds.sort(self.__stoneSort)
		lStoneRankMsg = []
		for iRoleId in lTempIds:
			if self.dLuckStone.get(iRoleId, 0) <= 0 or len(lStoneIds) >= 5:
				break
			lStoneIds.append(iRoleId)
		for iRoleId in lStoneIds:
			oMsg = guild_pb2.stoneMsg()
			oMsg.sName = self.dMemberAttrs.get(iRoleId, {}).get('name', '')
			oMsg.iStone = self.dLuckStone.get(iRoleId, 0)
			lStoneRankMsg.append(oMsg)
		self.lStoneRank = lStoneRankMsg
		self.bHasRank = True

	def __stoneSort(self, iIdA, iIdB):
		iStoneA, iStoneB = self.dLuckStone.get(iIdA, 0), self.dLuckStone.get(iIdB, 0)
		if iStoneA > iStoneB:
			return -1
		elif iStoneA < iStoneB:
			return 1
		return -1 if self.dAddStamp.get(iIdA, 0) <= self.dAddStamp.get(iIdB, 0) else 1
		
	def __getStoneRank(self):#幸运石排名信息
		if not self.bHasRank:
			self.__makeStoneRank()
		return self.lStoneRank

	def getMsg(self, oRole = None, *tArgs):#获取信息
		oMsg = guild_pb2.guildInfo()
		for sAttr in tArgs:
			if sAttr == 'id':
				oMsg.iId = self.id
			if sAttr == 'name':
				oMsg.sName = self.name
			if sAttr == 'ensign':
				oMsg.iIcon = self.ensign()
			if sAttr == 'notice':
				oMsg.sNotice = self.notice()
			if sAttr == 'log':
				oMsg.sLog.extend(self.logs())
			if sAttr == 'members':
				oMsg.member.extend(self.getMembersInfo())
			elif sAttr == 'apply':
				oMsg.bHasApply = len(self.sApplyJoinSet)
		# print self.getMembersInfo()i
		return oMsg		

	def getApplyJoinInfos(self):
		lMemberMsg, lRoleId = [], []
		for iRoleId in self.sApplyJoinSet:
			findSort.binaryInsertRight(lRoleId, iRoleId, self.__sortApplyCmp)	#排序
		for iRoleId in lRoleId:
			lMemberMsg.append(self.__makeProtoMsg(iRoleId, self.dApplyAttrs))
		return lMemberMsg

	def __sortApplyCmp(self, iRoleIdA, iRoleIdB):
		iFightAbilityA = self.dApplyAttrs.get(iRoleIdA, {}).get('fight')
		iFightAbilityB = self.dApplyAttrs.get(iRoleIdB, {}).get('fight')
		return [-1,1][iFightAbilityA>=iFightAbilityB]
				
	def getMembersInfo(self):
		if not self.bHasSort:
			self._sortMemberIds()	#排序
			self.bHasSort = True
		lMemberMsg = []	
		for iRoleId in self.lMemberIds:
			lMemberMsg.append(self.__makeProtoMsg(iRoleId, self.dMemberAttrs))
		return lMemberMsg

	def getGuildSceneInfo(self):
		return self.iSceneId, self.iNewX, self.iNewY

	def _sortMemberIds(self):
		lMemberIds = []
		if self.ownerId: lMemberIds.append(self.ownerId)
		if self.lSeniorIds: lMemberIds.extend(self.lSeniorIds)
		lTemp = []
		for iRoleId in self.lMemberIds:
			if iRoleId in lMemberIds:	continue
			findSort.binaryInsertRight(lTemp, iRoleId, self.__sortCmp)	#排序
		self.lMemberIds = lMemberIds + lTemp
	
	def __sortCmp(self, iRoleIdA, iRoleIdB):
		iFightAbilityA = self.dMemberAttrs.get(iRoleIdA, {}).get('fight')
		iFightAbilityB = self.dMemberAttrs.get(iRoleIdB, {}).get('fight')
		return [-1,1][iFightAbilityA>=iFightAbilityB]

	def _dirtyEventHandler(self):
		factoryConcrete.guildFtr.schedule2tail4save(self.iGuildId)

	def _onInitialized(self):	#加载完成
		for iRoleId in self.lMemberIds:	#初始化会员
			self.__setMemberAttr(iRoleId, self.dMemberAttrs)

		for iRoleId in self.sApplyJoinSet:#初始化申请加入成员的属性	
			self.__setMemberAttr(iRoleId, self.dApplyAttrs)

		iSceneNo = sceneData.guildSceneNo()	
		self.oScene = cScene(iSceneNo) #创建公会场景
		self.iSceneId = self.oScene.id
		# self.oScene.addDoor()
		self.iNewX, self.iNewY = self.oScene.landingPoint() 
		#self.lNpc = npc.initGuildNpc(self.oScene)	#初始化公会场景npc
		door.initGuildDoor(self.oScene)	#初始化传送门

	def __makeProtoMsg(self, iRoleId, dData, bForce=False):
		if not bForce and iRoleId in self.dMemberProtoMsg:
			return self.dMemberProtoMsg[iRoleId]
		oMemberMsg = guild_pb2.member()
		oMemberMsg.iRoleId = iRoleId
		dAttr = dData.get(iRoleId, {})
		oMemberMsg.sName = dAttr.get('name', '')
		oMemberMsg.iLevel = dAttr.get('level', 1)
		oMemberMsg.iFightAbility = dAttr.get('fight', 1)
		oMemberMsg.iPosition = getGuildPosition(self, iRoleId)
		oMemberMsg.iVipLv = dAttr.get('vipLv', 0)
		oMemberMsg.iSchool = dAttr.get("school", 1)
		self.dMemberProtoMsg[iRoleId] = oMemberMsg

		return oMemberMsg

	# def __initAttr(self, iRoleId, dData):
	# 	oResume=factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	# 	if not oResume:
	# 		if config.IS_INNER_SERVER:
	# 			raise Exception, '角色简要信息丢失'
	# 		else:#外网
	# 			self.__removeErrorRoleId(iRoleId)	#错误处理,移除错误的ID
	# 			pass
	# 		return
	# 	dAttr = self.dMemberAttrs.setdefault(iRoleId, {})
	# 	dAttr['name'] = oResume.name
	# 	dAttr['level'] = oResume.level
	# 	dAttr['school'] = oResume.school
	# 	dAttr['fight'] = oResume.fightAbility()
	# 	dAttr['vip'] = oResume.vipLv()
	# 	dAttr['active'] = oResume.weekActivite()	#活跃度


	def __onResumeLose(self, iRoleId):
		log.log('error', '公会初始化角色属性时角色简要信息丢失,角色ID:{}'.format(iRoleId))
		if config.IS_INNER_SERVER:
			if config.IS_INNER_SERVER:
				pass
				# raise Exception, '角色简要信息丢失'
			else:#外网
				#错误处理,移除错误的ID
				pass
		pass

import db4ms
import factory
def autoInit():	#初始化公会数据
	sSql = 'SELECT guildId FROM guild'
	rs = db4ms.gConnectionPool.query(sSql)
	for lGuildId in rs.rows:
		oGuild = gGuildKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, lGuildId[0])

def guildCmpByLv(oGuildA, oGuildB):
	return -1 if oGuildA.level <= oGuildB.level else 1

########################################
import role
def getRoleGuild(iRoleId):#获取角色的公会
	oRole = role.gKeeper.getObj(iRoleId)
	if oRole:	
		return oRole.getGuildObj()
	for oGuild in gGuildKeeper.getIterValues():
		if oGuild.isMember(iRoleId):	
			return oGuild
	return None

def removeMemberFromGuildByRoleId(ep, iRoleId):
	oGuild = getRoleGuild(iRoleId)
	if not oGuild:
		return True
	if oGuild.isPresident(iRoleId):
		ep.rpcTips('您是会长，在公会中还有其他会员时不可离会。如需退会，请先将会长一职任命给其他会员。')
		return False
	removeMemberFromGuild(oGuild, iRoleId)
	return True

def removeMemberFromGuild(oGuild, iRoleId):#移除会员
	if not oGuild.isMember(iRoleId):	#不是公会成员
		return False
	return oGuild.removeMember(iRoleId)

#上线删除角色关联公会ID
def deleteRoleGuildId(who,sGuildName,iStamep):
	who.setGuildId(NO_GUILD_ID)
	who.lazy.set('g_c_e_t', iStamep + 24 * 60 * 60)	#冷却结束时间戳
	ep=mainService.getEndPointByRoleId(who.id)
	if ep:
		ep.rpcTips('{}公会将你移出公会'.format('sGuildName'))
		ep.rpcNoticeMsg(notice_pb2.TYPE_GUILD_KICK)

#上线推送角色的请求处理结果
def dealRoleApply(who, bAgree, iGuildId):
	iRoleId = who.id
	lApGuild = who.lazy.fetch('ap_join', [])
	oGuild, bHasGuild = gGuildKeeper.getObj(iGuildId), bool(who.getGuildObj())
	ep= mainService.getEndPointByRoleId(iRoleId)
	if oGuild and bAgree and not bHasGuild:
		who.lazy.delete('ap_join')	#
		who.setGuildId(oGuild.id)	#设置玩家关联公会
		if ep: ep.rpcTips('{}公会同意您的加入'.format(oGuild.name))
		return ''
	if not bAgree and not bHasGuild and ep and oGuild:
		ep.rpcTips('{}公会不同意你的加入'.format(oGuild.name))
	if iGuildId in lApGuild:
		lApGuild.remove(iGuildId)
		if not lApGuild:
			who.lazy.delete('ap_join')
		else:
			who.lazy.set('ap_join', lApGuild)	
	return ''

def initGuildNpc(oGuildScene):
	lNpc = []
	for iNpcNo in npcData.gdDataBySceneno.get(oGuildScene.no(), []):
		dNpcInfo = npcData.gdData.get(iNpcNo, {})
		gdNpcModule[iNpcNo] = gdTypeMapMod.get(dNpcInfo.get('kind'), THIS_MODULE)
		x,y=dNpcInfo.get('x'),dNpcInfo.get('y')
		oNpc=new(iNpcNo,x,y)
		lNpc.append(oNpc)
		oNpc.sceneId=oGuildScene.id
		oNpc.x=x
		oNpc.y=y
		oGuildScene.addEntity(oNpc,x,y)#,x,y #场景管理npc的生命期
	return lNpc

	

########################################
	
def getGuildPosition(oGuild, iRoleId):
	if oGuild.isPresident(iRoleId):
		return	guild_pb2.TYPE_CHAIRMAN
	if oGuild.isSenior(iRoleId):
		return guild_pb2.TYPE_ELDER
	if oGuild.isMember(iRoleId):
		return guild_pb2.TYPE_MEM	
	return guild_pb2.TYPE_NOT_MEM


import guild_pb2
dPosition = {
	guild_pb2.TYPE_MEM 		: '帮众',
	guild_pb2.TYPE_CHAIRMAN	: '会长',
	guild_pb2.TYPE_ELDER 	: '长老',
}
def getStrGuildPosition(oGuild, iRoleId):
	iPosition = getGuildPosition(oGuild, iRoleId)
	return dPosition.get(iPosition, '')


import productKeeper
import factoryConcrete
import sql

if 'gbOnce' not in globals():
	gbOnce = True
	
	if 'mainService' in SYS_ARGV:
		gGuildKeeper = productKeeper.cProductkeeper(factoryConcrete.guildFtr)

import mainService
import findSort
import copy
import resume

import log
import misc
import sceneData
import scene
# import guildData
import u
import npc
import timeU
import mail
import c
import door
import config
'''