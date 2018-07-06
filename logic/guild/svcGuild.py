#-*-coding:utf-8-*-
#公会系统
#2014年6月16日16:15:19
import endPoint
import terminal_main_pb2
import role
import misc
import config

if 'gbIsClosed' not in globals():
	gbIsClosed=False #公会是否关闭

def handleClose(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		global gbIsClosed
		if gbIsClosed:# and not config.IS_INNER_SERVER:#只有生产环境才生效.
			ep.rpcTips('公会临时关闭.')
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:			
			gbIsClosed=True #发生异常,关闭公会
			log.log('guild','公会抛异常,临时关闭')
			raise
	return newFunc

ROLE_MAX_APPLY_JOIN = 5		#角色最大申请加入公会数
GUILD_MAX_APPLY_JOIN = 10	#
MAX_WORK_NUM = 5			#今日最大打工次数

class cService(terminal_main_pb2.terminal2main):

	@endPoint.result
	def rpcGuildEnsign(self,ep, who, reqMsg): return rpcGuildEnsign(self,ep, who, reqMsg)#公会会徽信息

	@endPoint.result
	def rpcOpenGuildView(self,ep, who, reqMsg): return rpcOpenGuildView(self,ep, who, reqMsg)#打开公会界面

	@endPoint.result
	def rpcCreateGuild(self,ep, who, reqMsg): return rpcCreateGuild(self,ep, who, reqMsg)#创建公会
	
	@endPoint.result
	def rpcGuildSearch(self,ep, who, reqMsg): return rpcGuildSearch(self,ep, who, reqMsg)#搜索公会

	@endPoint.result
	def rpcJoinGuild(self,ep, who, reqMsg): return rpcJoinGuild(self,ep, who, reqMsg)#加入公会
	
	@endPoint.result
	def rpcExitGuild(self,ep, who, reqMsg): return rpcExitGuild(self,ep, who, reqMsg)#退出公会
	
	@endPoint.result
	def rpcGuildMemberSetting(self,ep, who, reqMsg): return rpcGuildMemberSetting(self,ep, who, reqMsg)	#设置成员职位

	@endPoint.result
	def rpcApplyRoleInfos(self,ep, who, reqMsg): return rpcApplyRoleInfos(self,ep, who, reqMsg)#申请角色信息列表

	@endPoint.result
	def rpcHandleRequestJoin(self,ep, who, reqMsg): return rpcHandleRequestJoin(self,ep, who, reqMsg)#处理入会申请
	
	@endPoint.result
	def rpcGuildSetting(self,ep, who, reqMsg): return rpcGuildSetting(self,ep, who, reqMsg)#设置公会会徽和战力要求

	@endPoint.result
	def rpcChangeGuildNotice(self,ep, who, reqMsg): return rpcChangeGuildNotice(self,ep, who, reqMsg)#设置公会宣言

	@endPoint.result
	def rpcGoGuildScene(self,ep, who, reqMsg): return rpcGoGuildScene(self,ep, who, reqMsg)	#前往公会场景

	@endPoint.result
	def rpcGuildWorkRule(self,ep, who, reqMsg): return rpcGuildWorkRule(self,ep, who, reqMsg)	#请求公会打工规则

	@endPoint.result
	def rpcSelectWork(self,ep, who, reqMsg): return rpcSelectWork(self,ep, who, reqMsg)	#选择打工卡

	@endPoint.result
	def rpcChangWork(self,ep, who, reqMsg): return rpcChangWork(self,ep, who, reqMsg)	#换工作

	@endPoint.result
	def rpcDrawWorkAward(self, ch, who, reqMsg): return rpcDrawWorkAward(self, ch, who, reqMsg)	#领取打工奖励

def rpcGuildEnsign(self,ep, who, reqMsg):
	oGuild = who.getGuild()
	sEnsign = set() if not oGuild else oGuild.hasEnsign()
	gOEnsignPb2Msg = guild_pb2.ensignMsg()
	for iNo, dValue in guildData.gdBdage.iteritems():
		iCost = dValue.get('cost', 0)
		bFree = (iCost == 0 or iNo in sEnsign)
		oMsg = gOEnsignPb2Msg.freeEnsign.add() if bFree else gOEnsignPb2Msg.payEnsign.add()
		oMsg.iGuildIcon = iNo
		oMsg.iDiamond = iCost
	return gOEnsignPb2Msg

def rpcOpenGuildView(self,ep, who, reqMsg):#打开公会界面
	if who.level < guild.GUILD_LIMIT_LV:
		ep.rpcTips('公会在{}级开启'.format(guild.GUILD_LIMIT_LV))
		return
	oGuild = who.getGuild()
	if oGuild:
		ep.rpcPushGuildInfo(oGuild.getMsg(who, *guild.MSG_DETAIL))	#推送公会信息
		return
	doGuildSearch(ep, who, None, False)	

def rpcCreateGuild(self,ep, who, reqMsg):#创建公会
	doCreateGuide(ep, who, reqMsg.sName, reqMsg.iGuildIcon)

def doCreateGuide(ep, who, sGuildName, iGuildIcon):
	oGuild = who.getGuild()
	if oGuild:
		ep.rpcTips('您已经在{}公会了'.format( oGuild.name ) )
		return
	if guild.GUILD_LIMIT_LV > who.level:
		ep.rpcTips('{}级才能创建公会,继续努力吧'.format(guild.GUILD_LIMIT_LV) )
		return
	if who.lazy.fetch('g_c_e_t', 0) > timeU.getStamp():	#冷却结束时间戳
		ep.rpcTips('您现在处于冷却状态,{}后才能创建公会'.format(getCoolTimeDesc(who) ))
		return 
	if not sGuildName:
		ep.rpcTips('公会名不能为空')
		return
	sInvalid=u.isInvalidText(sGuildName)
	if sInvalid:
		ep.rpcTips('您输入的{}为非法字符，请重新输入!'.format(sInvalid))
		return
	if isUsedGuildName(sGuildName):
		ep.rpcTips('公会名字已被使用')
		return
	iCostDiamond = guildData.getBdageCoset(iGuildIcon)
	if who.diamond < iCostDiamond + guild.GUILD_COST_DIAMOND:
		ep.rpcTips('钻石不足')
		misc.rechargeTips(who,ep)
		return
	who.addDiamond(-iCostDiamond - guild.GUILD_COST_DIAMOND, '创建公会')
	uGuildId = GUId.gGuildId.nextId()	#公会ID生成器
	oGuild = guild.gGuildKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY, uGuildId)
	oGuild.setName(sGuildName)
	oGuild.setEnsign(iGuildIcon)	#设置公会名字,设置会徽
	oGuild.setPresident(who.id, who.name)			#设置会长ID
	oGuild.addMember(who.id)
	ep.rpcPushGuildInfo(oGuild.getMsg(who, *guild.MSG_DETAIL))	#推送公会信息
	ep.rpcTips('创建公会成功')

def getCoolTimeDesc(who):#获取冷却描述
	iCoolSeconds = who.lazy.fetch('g_c_e_t', 0)	- timeU.getStamp() + 1
	if iCoolSeconds <= 0:
		return '2秒'
	if iCoolSeconds <= 60:
		return '{}秒'.format(iCoolSeconds)
	if iCoolSeconds < 60*60:
		return '{}分钟'.format(iCoolSeconds/60)
	return '{0:4.1f}小时'.format(iCoolSeconds*1.0/3600)

def isUsedGuildName(sGuildName):#判断公会名是否被占用
	for oGuild in guild.gGuildKeeper.getIterValues():
		if oGuild.name == sGuildName:
			return True
	return False

def _isDimMatchGuild(sSearch, oGuild, iFightAbility):	#
	if not sSearch:#寻找推荐公会
		return True
		# return not oGuild.isFull() and oGuild.fightAbility() <= iFightAbility
	return sSearch in '{}{}'.format(oGuild.id, oGuild.name)

def rpcGuildSearch(self,ep, who, reqMsg):	#搜索公会
	doGuildSearch(ep, who, reqMsg.iValue)

def doGuildSearch(ep, who, sSearch, bTips = True):
	iFightAbility = who.fightAbility()
	lTempGuild = [oGuild for oGuild in guild.gGuildKeeper.getIterValues() if _isDimMatchGuild(sSearch, oGuild, iFightAbility)]
	if not lTempGuild and bTips:
		ep.rpcTips('搜索不到您要查找的公会！')
		return
	lMatchGuild = []
	for oGuild in lTempGuild:
		findSort.binaryInsertRight(lMatchGuild, oGuild, guild.guildCmpByLv)	#排序
	lApJoin = who.lazy.fetch('ap_join', [])
	resp=guild_pb2.guildList()
	for oGuild in lMatchGuild:
		oGuildInfo = resp.guilds.add()
		oGuildInfo.iGuildId = oGuild.id
		oGuildInfo.sName = oGuild.name
		oGuildInfo.iNeedFight = oGuild.fightAbility()
		oGuildInfo.iIcon = oGuild.ensign()
		oGuildInfo.iApplyState = oGuild.id in lApJoin
		oGuildInfo.iMemberAmount = oGuild.memberAmount()
	ep.rpcPushGuildList(resp)

def rpcJoinGuild(self,ep, who, reqMsg):	#加入公会
	if who.level < guild.GUILD_LIMIT_LV:
		ep.rpcTips('{}级才能加入公会,请继续努力'.format(guild.GUILD_LIMIT_LV))
		return False
	if who.getGuild():
		ep.rpcTips('您已经在{}公会'.format(who.getGuild().name))
		return False
	if who.lazy.fetch('g_c_e_t', 0) > timeU.getStamp():
		ep.rpcTips('您刚脱离公会，请等待{}再来申请加入新公会'.format(getCoolTimeDesc(who) ))
		return False
	iGuildId = reqMsg.iValue	
	oGuild = guild.gGuildKeeper.getObj(iGuildId)
	if not oGuild:
		ep.rpcTips('您申请加入的公会不存在')
		return False
	lApplyJoin = who.lazy.fetch('ap_join', [])	#ap_join  角色也申请加入公会的集合
	if iGuildId in lApplyJoin:
		oGuild.removeApplyJoinRole(who.id)
		lApplyJoin.remove(iGuildId)
		who.lazy.set('ap_join', lApplyJoin)	#
		ep.rpcTips('取消申请成功')
		return True
	if len(lApplyJoin) >= ROLE_MAX_APPLY_JOIN:
		ep.rpcTips('只能同时申请{}个公会！'.format(ROLE_MAX_APPLY_JOIN))
		return False
	if len(oGuild.applyJoinSet()) >= GUILD_MAX_APPLY_JOIN:
		ep.rpcTips('目标公会申请的人已经满了!')
		return False
	if oGuild.isFull():
		ep.rpcTips('{}公会人数已满,请换一个公会加入'.format(oGuild.name))
		return False
	if who.fightAbility() < oGuild.fightAbility():
		ep.rpcTips('很抱歉您的战力不够公会的要求，请继续努力!')
		return False
	oGuild.addApplyJoinRole(who)	#加入公会申请
	ep.rpcTips('已向{}公会发出申请,请等候长老们的处理'.format(oGuild.name))
	return True

def rpcExitGuild(self,ep, who, reqMsg):	#退出公会
	oGuild = who.getGuild()
	if not oGuild:
		ep.rpcTips('您当前未加入任何公会')
		return False
	if oGuild.isPresident(who.id) and oGuild.memberAmount() >= 2:
		ep.rpcTips('您是会长，在公会中还有其他会员时不可离会。如需退会，请先将会长一职任命给其他会员。')
		return False
	bFail,uResponse=ep.rpcConfirmBox('退出公会','您确定退出{}公会吗?'.format(oGuild.name),'Q_确定Q_容我三思')
	if bFail or uResponse.iValue != 0:
		return False	#操作超时
	if guild.removeMemberFromGuild(oGuild, who.id):
		ep.rpcTips('退出公会成功')
		who.lazy.set('g_c_e_t', timeU.getStamp() + 24 * 60 * 60)	#冷却结束时间戳
		who.setGuildId(guild.NO_GUILD_ID)	#去除公会信息
		return True
	ep.rpcTips('退出失败')
	return False

def rpcGuildMemberSetting(self,ep, who, reqMsg):	#工会成员操作
	iPosition, iRoleId = reqMsg.iValue32, reqMsg.iValue64
	oGuild = who.getGuild()
	if not oGuild:
		ep.rpcTips('您当前未加入任何公会')
		return False
	if not oGuild.isMember(iRoleId):
		ep.rpcTips('对方不是{}公会的成员'.format(oGuild.name))
		return False
	bResult = oGuild.changePosition(who,ep, iRoleId, iPosition)
	# ep.rpcTips(oGuild.changePosition(who, iRoleId, iPosition))	#设置iRoleId的权限(职位)
	return bResult

def rpcApplyRoleInfos(self,ep, who, reqMsg):	#获取申请加入公会角色信息列表
	iRoleId, oGuild = who.id, who.getGuild()
	if not oGuild:
		return ['您当前未加入任何公会']
	if not ( oGuild.isPresident(iRoleId) or oGuild.isSenior(iRoleId) ):
		return ['权限不够,不能查看']
	oMsg = guild_pb2.applyMember()
	oMsg.applyMember.extend(oGuild.getApplyJoinInfos())
	return oMsg 

def handleRequestJoin(iRoleId, bAgree, sGuildName, dAttr, oGuild):
	if guild.getRoleGuild(iRoleId) and bAgree:
		return '{}的请求也过期'.format(dAttr.get('name', ''))
	#此时角色未加入任何公会
	if bAgree:
		oGuild.addMember(iRoleId)	#角色加入公会
	ep, oRole = mainService.getEndPointByRoleId(iRoleId), role.gKeeper.getObj(iRoleId)
	if ep and oRole:#角色在线
		return guild.dealRoleApply(oRole, bAgree, oGuild.id)

	oTargetResume = resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	if not oTargetResume:
		return ''
	oTargetResume.addLoginCall(resume.DEALROLEAPPLY, bAgree, oGuild.id)
	return ''
		
def rpcHandleRequestJoin(self,ep, who, reqMsg):	#处理入会申请
	iRoleId, oGuild = who.id, who.getGuild()
	if not oGuild:
		ep.rpcTips('您当前未加入任何公会')
		return False
	if not ( oGuild.isPresident(iRoleId) or oGuild.isSenior(iRoleId) ):
		ep.rpcTips('权限不够')
		return False
	sGuildName = oGuild.name
	for handleMsg in reqMsg.applyMsg:
		iTargetRoleId, bAgree = handleMsg.iRoleId, handleMsg.bAgree
		dAttr = oGuild.removeApplyJoinRole(iTargetRoleId)	#公会清除角色的请求数据
		if not dAttr:
			ep.rpcTips('该请求已过期')	
			continue
		if oGuild.isFull():
			oGuild.clearApplyJoinRole()	#移除所有的入会申请
			ep.rpcTips('公会已满员')
			return True
		sTips = handleRequestJoin(iTargetRoleId, bAgree, sGuildName, dAttr, oGuild)
		if sTips:	
			ep.rpcTips(sTips)
	ep.rpcTips('操作成功')
	return True

def rpcGuildSetting(self,ep, who, reqMsg):	#设置战力和宣言
	iEnsign, iFightAbility = reqMsg.iIcon, reqMsg.iFightLimit
	oGuild = who.getGuild()
	if not oGuild:
		return ['您当前未加入任何公会']
	iRoleId = who.id
	if not oGuild.isSenior(iRoleId) and not oGuild.isPresident(iRoleId):
		return ['权限不够']
	if oGuild.ensign() != iEnsign:	#设置会徽
		iCostDiamond = 0 if (iEnsign in oGuild.hasEnsign()) else guildData.getBdageCoset(iEnsign)
		if who.diamond < iCostDiamond:
			misc.rechargeTips(who, ep)
			return False
		who.addDiamond(-iCostDiamond, '修改公会会徽', None)
		oGuild.setEnsign(iEnsign)
	if oGuild.fightAbility() != iFightAbility:
		oGuild.setFightAbility(iFightAbility)
	ep.rpcTips('设置成功')
	return True

def rpcChangeGuildNotice(self,ep, who, reqMsg):	#设置公会宣言
	oGuild = who.getGuild()
	if not oGuild:
		return ['您当前未加入任何公会']
	sNotice = reqMsg.iValue
	sInvalid=u.isInvalidText(sNotice)
	if sInvalid:
		ep.rpcTips('您输入的{}为非法字符，请重新输入!'.format(sInvalid))
		return False
	oGuild.setNotice(sNotice)
	return True

def rpcGoGuildScene(self,ep, who, reqMsg):#前往公会场景
	oGuild = who.getGuild()
	if not oGuild:
		ep.rpcTips('您当前未加入任何公会')
		return
	iGuildSceneId, iNewX, iNewY = oGuild.getGuildSceneInfo()
	scene.tryTransfer(who.id, iGuildSceneId, iNewX, iNewY)

def rpcGuildWorkRule(self,ep, who, reqMsg):#公会打工规则
	return guildData.getWorkRuleDesc()

def rpcSelectWork(self,ep, who, reqMsg):	#打工卡
	if not who.getGuild():
		return ['您当前未加入任何公会']
	if who.getGuild().getWorkTimes(who.id) <= 0:
		return ['今日打工次数已用完']
	if not who.eDisConnected.contain(onRoleDisconnect):
		who.eDisConnected += onRoleDisconnect
	return makeWorkMsg(ep, who, guildData.getRandmWorkNo(MAX_WORK_NUM))

def _getWorkAwardKey(lWorkNos):
	dTemp = {}
	for iWorkNo in lWorkNos:
		dTemp[iWorkNo] = dTemp.get(iWorkNo, 0) + 1
	lTemp = dTemp.values()
	lTemp.sort(None, None, True)
	return tuple(lTemp)

def makeWorkMsg(ep, who, lWorkNos):
	oGuild = who.getGuild()
	slWork = guild_pb2.selectWork()
	for iWorkNo in lWorkNos:
		slWork.workList.extend([guildData.gdPb2Work[iWorkNo]])
	# slWork.sRuleList.extend(guildData.lAwardRule)
	tKey = _getWorkAwardKey(lWorkNos)
	iVipRotation = 50 if who.accountObj.vipLv()>=6 else 0
	fAddRotation = (oGuild.getLvAddr('addRation', 0) + 100 + iVipRotation) * 1.0 /100	
	slWork.iGold = int(guildData.getAwardMsg(tKey, 'gold') * fAddRotation)
	slWork.iStone = guildData.getAwardMsg(tKey, 'stone')
	slWork.sRule = guildData.getAwardMsg(tKey, 'desc')
	iChangeTimes, iVipFreeTimes = oGuild.getChangeWorkTimes(who.id) + 1, vip.helper.changeWorkTimes(who)
	if iChangeTimes > iVipFreeTimes:
		iChangeTimes -= iVipFreeTimes
		slWork.iDiamond = guildData.getChangeWorkCost(iChangeTimes)
	else:
		slWork.iDiamond = 0
	setattr(who, 'g_w_l', lWorkNos)
	return slWork

def onRoleDisconnect(who):
	doDrawWorkAward(who)

def rpcChangWork(self,ep, who, reqMsg):#换工作
	oGuild = who.getGuild()
	if not oGuild:
		return ['您当前未加入任何公会']
	if not getattr(who, 'g_w_l', None):
		return ['未开始打工,不能进行更换工作操作']
	if not reqMsg.iValue:
		return ['请选择需要更换的工作']
	print 'rpcChangWork:', reqMsg.iValue
	iChangeTimes, iVipFreeTimes = oGuild.getChangeWorkTimes(who.id) + 1, vip.helper.changeWorkTimes(who)
	if iChangeTimes > iVipFreeTimes:
		iChangeTimes -= iVipFreeTimes
		iCostDiamond = guildData.getChangeWorkCost(iChangeTimes)
	else:
		iCostDiamond = 0
		ep.rpcTips('VIP特权换工作免费')
	if who.diamond < iCostDiamond:
		misc.rechargeTips(who, ep)
		return ['钻石不足']
	who.addDiamond(-iCostDiamond, '更换公会工作扣除')

	lNewWorkNo = guildData.getRandmWorkNo(len(reqMsg.iValue))
	
	for iIdx,iPos in enumerate(reqMsg.iValue):
		who.g_w_l[iPos] = lNewWorkNo[iIdx]
	oGuild.addChangeWorkTime(who.id)	#增加换工作的次数
	return makeWorkMsg(ep, who, who.g_w_l)

def rpcDrawWorkAward(self,ep, who, reqMsg):#领取打工奖励
	doDrawWorkAward(who,ep, reqMsg.iValue)	

def doDrawWorkAward(who, ep=None, iType = 0):
	oGuild = who.getGuild()
	if not oGuild:
		if ep:	ep.rpcTips('您当前未加入任何公会')
		return
	lWorkNos = getattr(who, 'g_w_l', [])
	if not lWorkNos:
		if ep:	ep.rpcTips('您当前未选择任何工作')
		return
	iRoleId = who.id
	tKey = _getWorkAwardKey(lWorkNos)
	iVipRotation = 50 if who.accountObj.vipLv()>=6 else 0
	fAddRotation = (oGuild.getLvAddr('addRation', 0) + 100 + iVipRotation) * 1.0 /100
	who.addTradeCash(int(guildData.getAwardMsg(tKey, 'gold') * fAddRotation), '公会打工领取')	#增加角色的元宝
	oGuild.addExp(guildData.getAwardMsg(tKey, 'exp'))	#增加公会经验
	oGuild.addStone(iRoleId, guildData.getAwardMsg(tKey, 'stone'))	#增加公会幸运石
	oGuild.addWorkTimes(iRoleId)						#增加角色打工次数
	del who.g_w_l	#清除角色打工数据
	if ep and iType:										
		ep.rpcPushGuildWorkInfo( oGuild.getWorkInfo(iRoleId) )


import timeU
import guild
import u
import guildData
import factory
import log
import GUId
import findSort
import guild_pb2
import role
import resume
import scene
import mainService
