#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
import rank
import block.blockRanking

RANK_PAGE=8
#排行榜查询服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcRankFightAbilityReq(self,ep,who,reqMsg):return rpcRankFightAbilityReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcRankLvReq(self,ep,who,reqMsg):return rpcRankLvReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcRankGoldReq(self,ep,who,reqMsg):return rpcRankGoldReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcRankLeagueReq(self,ep,who,reqMsg):return rpcRankLeagueReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcRankArenaDayReq(self,ep,who,reqMsg):return rpcRankArenaDayReq(self,ep,who,reqMsg)#竞技场每日排行
	@endPoint.result
	def rpcRankArenaWeekReq(self,ep,who,reqMsg):return rpcRankArenaWeekReq(self,ep,who,reqMsg)#竞技场每周排行
	@endPoint.result
	def rpcRankArenaAllReq(self,ep,who,reqMsg):return rpcRankArenaAllReq(self,ep,who,reqMsg)#竞技场历史总排行
	@endPoint.result
	def rpcRankDisplayReq(self,ep,who,reqMsg):return rpcRankDisplayReq(self,ep,who,reqMsg)#炫耀一下
	@endPoint.result
	def rpcRankClimbReq(self,ep,who,reqMsg):return rpcRankClimbReq(self,ep,who,reqMsg)#爬塔排行榜
	
def rpcRankDisplayReq(self,ep,who,reqMsg):
	iType=reqMsg.iValue
	iRoleId=who.id
	oRank,sRankName=getRankAndNameByType(iType)
	rankList=oRank.rank() if iType==RANK_LEAGUE else oRank.ranking()[:oRank.iDisplaySize]
	if iRoleId not in rankList:
		ep.rpcTips('你的排名未上榜,还不能进行炫耀')
		return
	iCurStamp=timeU.getStamp()
	if iCurStamp-getattr(who,'iLastShowStamp',0)<=10:
		ep.rpcTips('你炫耀的过于频繁了,稍后再试试吧')
		return
	bFail,uMsg=ep.rpcConfirmBox(sTitle='炫耀一下',sContent='炫耀一次需要消耗一个喇叭,是否炫耀?',sSelect='Q_确定Q_取消')
	if bFail or uMsg.iValue!=0:
		return
	who=role.gKeeper.getObj(iRoleId)
	if not who:
		return
	oTrumpet=who.propsCtn.getTrumpet()
	if not oTrumpet:
		ep.rpcTips('你的喇叭数量不足')
		return
	who.propsCtn.addStack(oTrumpet,-1)#扣除喇叭
	iCurStamp=timeU.getStamp()
	who.iLastShowStamp=iCurStamp#设置炫耀时间
	sContent=getShowContent(iType,who,oRank,sRankName)
	oMsg=chatRoom_pb2.chatSysDown(iChannel=1,sContent=sContent,)
	sPacket=endPoint.makePacket('rpcAnnounce',oMsg)
	for iUid,ep in mainService.gRoleIdMapEndPoint.getAll().iteritems():
		ep.send(sPacket)

def getRank(iType,cRank,who):
	rankInfo=role_pb2.roleRank()
	rankInfo.iType=iType
	rankInfo.myRank.iRoleId=who.id#请求第一页时将玩家自己的排名各项数据发过去
	rankInfo.myRank.sName=who.name
	rankInfo.myRank.iRank=cRank.getRoleRank(who.id)
	rankInfo.myRank.iOldRank=cRank.getOldRoleRank(who.id)
	rankInfo.myRank.iValue=cRank.getRoleValue(who.id) if cRank.getRoleValue(who.id)>0 else value(iType,who)
	rankInfo.myRank.iLevel=who.level
	rankInfo.myRank.iOccu=who.school
	rankInfo.myRank.sGuide='未加入公会'
	rankList=cRank.rank() if iType==RANK_LEAGUE else cRank.lRanking
	iLength=cRank.iDisplaySize if cRank.iDisplaySize<len(rankList) else len(rankList)
	lKeys=list(who.friendCtn.getAllKeys())
	for i in xrange(iLength):
		roleInfo=rankInfo.role.add()
		roleInfo.iRoleId=rankList[i]
		roleInfo.sName=cRank.getRoleName(roleInfo.iRoleId)
		roleInfo.iRank=cRank.getRoleRank(roleInfo.iRoleId)
		roleInfo.iOldRank=cRank.getOldRoleRank(roleInfo.iRoleId)
		roleInfo.iValue=cRank.getRoleValue(roleInfo.iRoleId)
		roleInfo.iLevel=cRank.getRoleLv(roleInfo.iRoleId)
		roleInfo.iOccu=cRank.getRoleSchool(roleInfo.iRoleId)
		roleInfo.sGuide='未加入公会'
		roleInfo.bFriend=roleInfo.iRoleId in lKeys
		if iType==RANK_CLIMB:
			roleInfo.iFighting=cRank.getRoleFight(roleInfo.iRoleId)
		# if iType==RANK_LEAGUE:
		# 	roleInfo.iLevel=cRank.getRoleLv(roleInfo.iRoleId)
		# 	roleInfo.iFighting=cRank.getRoleFighting(roleInfo.iRoleId)
	return rankInfo

def rpcRankClimbReq(self,ep,who,reqMsg):
	ep.rpcRank(getRank(RANK_CLIMB,block.blockClimbRank.gClimbRank,who))

def rpcRankFightAbilityReq(self,ep,who,reqMsg):
	#ep.rpcTips('更新调整，排行榜暂不可用')
	ep.rpcRank(getRank(RANK_FIGHTING,block.blockRanking.gFightRank,who))

def rpcRankLvReq(self,ep,who,reqMsg):
	ep.rpcRank(getRank(RANK_LV,block.blockRanking.gLvRank,who))

def rpcRankGoldReq(self,ep,who,reqMsg):
	ep.rpcRank(getRank(RANK_GOLD,block.blockRanking.gGoldRank,who))

def rpcRankLeagueReq(self,ep,who,reqMsg):
	ep.rpcRank(getRank(RANK_LEAGUE,block.blockLeagueRank.gLeagueRank,who))

def rpcRankArenaDayReq(self,ep,who,reqMsg):
	msg=block.blockArenaRank.gArenaDayRank.getMsg(who)
	ep.rpcRank(msg)

def rpcRankArenaWeekReq(self,ep,who,reqMsg):
	msg=block.blockArenaRank.gArenaWeekRank.getMsg(who)
	ep.rpcRank(msg)

def rpcRankArenaAllReq(self,ep,who,reqMsg):
	msg=block.blockArenaRank.gArenaAllRank.getMsg(who)
	ep.rpcRank(msg)

def value(iType,who):
	if iType==RANK_FIGHTING:
		return who.fightAbility()
	elif iType==RANK_LV:
		return who.level
	elif iType==RANK_GOLD:
		return who.gold
	elif iType==RANK_LEAGUE:
		return who.fightAbility()
	elif iType==RANK_CLIMB:
		return who.day.fetch('climb_prcess', 0)

def getRankAndNameByType(iType):
	oRank=None
	sRankName=''
	if iType==RANK_FIGHTING:
		oRank=block.blockRanking.gFightRank
		sRankName='战力榜'
	elif iType==RANK_LV:
		oRank=block.blockRanking.gLvRank
		sRankName='等级榜'
	elif iType==RANK_GOLD:
		oRank=block.blockRanking.gGoldRank
		sRankName='金钱榜'
	elif iType==RANK_LEAGUE:
		oRank=block.blockLeagueRank.gLeagueRank
		sRankName='英雄榜'
	elif iType==RANK_CLIMB:
		oRank=block.blockClimbRank.gClimbRank
		sRankName='爬塔榜'
	if not oRank:
		raise Exception,'还有其他排行榜可以炫耀一下???'
	return oRank,sRankName

def getShowContent(iType,oRole,oRank,sRankName):#得到炫耀的内容
	iRank=oRank.getRoleRank(oRole.id)
	sRoleName=oRole.name
	if iRank==1:
		return '玩家&06{}&荣登本区{}&02榜首&,大家快来膜拜他吧!!!'.format(sRoleName,sRankName)
	elif iRank==2:
		return '玩家&06{}&获得本区{}&02亚军&,离冠军只有一步之遥了!!!'.format(sRoleName,sRankName)
	elif iRank==3:
		return '玩家&06{}&{}排名挤入本区&02前3&,实力不可小觑!'.format(sRoleName,sRankName)
	elif iRank==4:
		return '玩家&06{}&获得本区{}&02第4名&,继续向前3名奋进吧!'.format(sRoleName,sRankName)
	elif iRank==5:
		return '玩家&06{}&{}排名闯入&02前5名&,继续向前3名奋进吧!'.format(sRoleName,sRankName)
	elif iRank==6:
		return '玩家&06{}&本区{}排名&02第6&,继续向前5名奋进吧!'.format(sRoleName,sRankName)
	elif iRank<=10:
		return '玩家&06{}&本区{}排名&02第{}&,进入前10行列!'.format(sRoleName,sRankName,iRank)
	elif iRank==11:
		return '玩家&06{}&本区{}排名&02第11&,即将迈入前10行列!'.format(sRoleName,sRankName)
	return '玩家&06{}&本区{}排名&02第{}&,进入了前20行列。'.format(sRoleName,sRankName,iRank)

RANK_FIGHTING=1
RANK_LV=2
RANK_GOLD=3
RANK_LEAGUE=4
RANK_ARENA_DAY=5 #竞技场日榜
RANK_ARENA_WEEK=6 #竞技场周榜
RANK_ARENA_ALL=7 #竞技场总榜
RANK_CLIMB=8 #爬塔

import role_pb2
import resume
import factory
import c

import role
import mainService
import u
import timeU