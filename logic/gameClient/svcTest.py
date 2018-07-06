#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
import misc

class cService(terminal_main_pb2.main2terminal):
	@endPoint.result
	def rpcHeHeHe(self,ep,ctrlr,reqMsg):
		print 'rpcHeHeHe called'	
	###############################################
	@endPoint.result
	def rpcAvatarAttrChange(self,ep,ctrlr,reqMsg):
		print reqMsg
	##################################################
	@endPoint.result
	def rpcRouletteInfo(self,ep,ctrlr,reqMsg):
		print '---------rpcRouletteInfo-----------'
		print reqMsg

	@endPoint.result
	def rpcSpinResult(self,ep,ctrlr,reqMsg):
		print '---------rpcSpinResult-----------'
		print reqMsg		

	@endPoint.result
	def rpcClientBarrierList(self,ep,ctrlr,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcSelectBox(self,ep,ctrlr,reqMsg):
		print 'rpcSelectBox',u.trans(reqMsg.sTitle),u.trans(reqMsg.sQuestion)
		#return 0
		sInput=raw_input('select: ')
		if not sInput:
			return 0
		return int(sInput)

	@endPoint.result
	def rpcClientTaskDialog(self,ep,ctrlr,reqMsg):
		print 'rpcClientTaskDialog',u.trans(reqMsg.sContent)
		return 1

	@endPoint.result
	def rpcModalDialog(self,ep,ctrlr,reqMsg):
		print 'rpcModalDialog',u.trans(reqMsg.sTitle),u.trans(reqMsg.sContent)

	@endPoint.result
	def rpcPushMsgBall(self,ep,ctrlr,reqMsg):
		print 'rpcPushMsgBall', reqMsg
		return 1

	@endPoint.result
	def rpcConfirmBox(self,ep,ctrlr,reqMsg):
		print 'rpcConfirmBox',reqMsg
		return 1
	

	@endPoint.result
	def rpcChat(self,ep,ctrlr,reqMsg):
		print 'rpcChat',reqMsg

	@endPoint.result
	def rpcAnnounce(self,ep,ctrlr,reqMsg):
		print 'rpcAnnounce',reqMsg

	@endPoint.result
	def rpcAddTitle(self,ep,ctrlr,reqMsg):
		print reqMsg.iTitleNo

	@endPoint.result
	def rpcRemoveTitle(self,ep,ctrlr,reqMsg):
		print reqMsg.iValue

	@endPoint.result
	def rpcTips(self,ep,ctrlr,reqMsg):
		print 'rpcTips',u.trans(reqMsg.sValue)

	@endPoint.result
	def rpcShutdown(self,ep,ctrlr,reqMsg):
		print reqMsg.iValue
		#做些返回登录界面之类的事情

	@endPoint.result
	def rpcEttEnter(self,ep,who,reqMsg):
		print 'rpcEttEnter',timeU.stamp2str(),u.transMsg(reqMsg)

	@endPoint.result
	def rpcEttLeave(self,ep,who,reqMsg):
		print 'rpcEttLeave',timeU.stamp2str(),u.transMsg(reqMsg)

	@endPoint.result
	def rpcEttMoveStart(self,ep,who,reqMsg):
		print 'rpcEttMoveStart',timeU.stamp2str(),u.transMsg(reqMsg)

	@endPoint.result
	def rpcEttMoveStop(self,ep,who,reqMsg):
		print 'rpcEttMoveStop',timeU.stamp2str(),u.transMsg(reqMsg)

	@endPoint.result
	def rpcSwitchScene(self,ep,who,reqMsg):
		print 'rpcSwitchScene',timeU.stamp2str(),u.transMsg(reqMsg)
		return True

	@endPoint.result
	def rpcMapInfo(self,ep,who,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcAvatarAttrInit(self,ep,who,reqMsg):#角色属性初始化
		print reqMsg

	@endPoint.result
	def rpcAvatarAttrChange(self,ep,who,reqMsg):#角色属性变更
		print reqMsg

	@endPoint.result
	def rpcFriendAttr(self,ep,who,reqMsg):#好友属性
		print reqMsg

	@endPoint.result
	def rpcFriendEquip(self,ep,who,reqMsg):#好友已穿戴装备
		msg=props_pb2.propsMsg()
		for prop in reqMsg.props:
			msg.ParseFromString(prop.serialized)
			print prop.uiType(),prop.iPos
			print msg

	@endPoint.result
	def rpcImMsgArrival(self,ep,who,reqMsg):#有新聊天消息
		print '您有来自{}的消息，请查收'.format(reqMsg.sContent)

	@endPoint.result
	def rpcSendImMsg(self,ep,who,reqMsg):#新聊天消息抵达
		print reqMsg

	@endPoint.result
	def rpcAddPropsToPackage(self,ep,who,reqMsg):#向包裹添加物品
		print reqMsg.iUiType,reqMsg.iPos

	@endPoint.result
	def rpcAllPropsInPackage(self,ep,who,reqMsg):#接收全部包裹物品
		print reqMsg
		# for msg in reqMsg.props:
		# 	print msg.iUiType,msg.iPos

	@endPoint.result
	def rpcChangePropsAttr(self,ep,who,reqMsg):#使用包裹物品
		print reqMsg.iPropsId,reqMsg.iPropsStack

	@endPoint.result
	def rpcOnline(self,ep,who,reqMsg):#好友上线
		print '{}上线了'.format(reqMsg.iValue)

	@endPoint.result
	def rpcOffline(self,ep,who,reqMsg):#好友下线
		print '{}下线了'.format(reqMsg.iValue)

	@endPoint.result
	def rpcFriendList(self,ep,who,reqMsg):#好友列表
		if reqMsg.iType==1:
			print 'rpcFriendList','len(reqMsg.roles)=',len(reqMsg.roles)
		elif reqMsg.iType==2:
			print 'rpcBlackList','len(reqMsg.roles)=',len(reqMsg.roles)
		elif reqMsg.iType==4:
			print 'rpcRecentContactList','len(reqMsg.roles)=',len(reqMsg.roles)
		for role in reqMsg.roles:			
			print 'Id：{}'.format(role.iRoleId)
			print '角色名：{}'.format(role.sRoleName)
			print '等级：{}'.format(role.iRoleLevel)
			print '-------------------------------------'

	@endPoint.result
	def rpcFriendChange(self,ep,who,reqMsg):#好友变化
		if reqMsg.iType==1:
			print 'rpcFriendAdd'
		elif reqMsg.iType==2:
			print 'rpcFriendDel'
		for role in reqMsg.roles:			
			print 'Id：{}'.format(role.iRoleId)
			print '角色名：{}'.format(role.sRoleName)
			print '等级：{}'.format(role.iRoleLevel)
			print '-------------------------------------'

	@endPoint.result
	def rpcBlackChange(self,ep,who,reqMsg):#黑名单变化
		if reqMsg.iType==1:
			print 'rpcBlackAdd'
		elif reqMsg.iType==2:
			print 'rpcBlackDel'
		for role in reqMsg.roles:			
			print 'Id：{}'.format(role.iRoleId)
			print '-------------------------------------'

	@endPoint.result
	def rpcRollAnnounce(self,ep,who,reqMsg):#滚动公告
		print reqMsg.iValue

	@endPoint.result
	def rpcChangePropsPos(self,ep,who,reqMsg):#物品位置变化
		print reqMsg.iValue1,reqMsg.iValue2
	
	@endPoint.result
	def rpcSendPropsDetail(self,ep,who,reqMsg):#物品详细信息
		print reqMsg

	@endPoint.result
	def rpcRank(self,ep,who,reqMsg):
		print reqMsg
		
	@endPoint.result
	def rpcClientTaskList(self,ep,who,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcTaskAdd(self,ep,who,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcPushGuildList(self,ep,who,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcEnhanceInfo(self,ep,who,reqMsg):
		print reqMsg

	@endPoint.result
	def rpcPushTeamInfo(self,ep,who,reqMsg):
		print reqMsg

########################################################################
	@endPoint.result
	def rpcResetGuildAttr(self,ep,who,reqMsg):#邮件列表
		print reqMsg

	@endPoint.result
	def rpcPushMailList(self,ep,who,reqMsg):#邮件列表
		for mail in reqMsg.mails:
			print mail
		return

		iMinX,iMaxX=400,2300
		iMinY,iMaxY=20,280
		import gevent
		import random
		import sync_pb2
		while 1:
			bFail,uResponse=ep.rpcPos()
			if bFail:
				print 'socket is broken'
				break
			iRoleId=uResponse.iRoleId
			iCurX=uResponse.iX
			iCurY=uResponse.iY
			iDstX=random.randint(iMinX,iMaxX)
			iDstY=random.randint(iMinY,iMaxY)
			diffX=iDstX-iCurX
			diffY=iDstY-iCurY
			iFlip=1
			if diffX>0:
				if diffY>0:
					iDir=3
				elif diffY<0:
					iDir=5
				else:
					iDir=4
			elif diffX<0:
				iFlip=-1
				if diffY>0:
					iDir=9
				elif diffY<0:
					iDir=7
				else:
					iDir=8
			else:
				if diffY>0:
					iDir=2
				elif diffY<0:
					iDir=6
				else:
					iDir=1
			fSleepTime=(diffX**2+diffY**2)**0.5/313
			#--- start moving ---
			msg=sync_pb2.syncMsg()
			#--- act ---
			msg.act.iEttId=iRoleId
			msg.act.iState=1030
			msg.act.iDir=iDir
			msg.act.iCurX=iCurX
			msg.act.iCurY=iCurY
			#--- flip ---
			msg.flip.iEttId=iRoleId
			msg.flip.iFlip=iFlip
			#--- dir ---
			msg.dir.iEttId=iRoleId
			msg.dir.iDir=iDir
			msg.dir.iCurX=iCurX
			msg.dir.iCurY=iCurY
			ep.rpcRoleSync(msg)
			gevent.sleep(fSleepTime)
			#--- stop moving ---
			msg=sync_pb2.syncMsg()
			#--- dir ---
			msg.dir.iEttId=iRoleId
			msg.dir.iDir=1
			msg.dir.iCurX=iDstX
			msg.dir.iCurY=iDstY
			ep.rpcRoleSync(msg)

			msg=sync_pb2.syncMsg()
			#--- act ---
			msg.act.iEttId=iRoleId
			msg.act.iState=1010
			msg.act.iDir=1
			msg.act.iCurX=iDstX
			msg.act.iCurY=iDstY
			ep.rpcRoleSync(msg)
			gevent.sleep(2)
	
	@endPoint.result
	def rpcPushMail(self,ep,who,reqMsg):#邮件
		print reqMsg

	@endPoint.result
	def rpcRoleSkillList(self,ep,who,reqMsg):#角色技能列表
		print '====================================='
		print 'skill NUM=',len(reqMsg.skills)
		print '技能栏1：{}'.format(reqMsg.iGrid1)
		print '技能栏2：{}'.format(reqMsg.iGrid2)
		print '技能栏3：{}'.format(reqMsg.iGrid3)
		print '技能栏4：{}'.format(reqMsg.iGrid4)
		print '====================================='
		for skill in reqMsg.skills:
			print 'Id：{}'.format(skill.iSkillNo)
			print '技能名称：{}'.format(skill.sSkillName)
			print '描述：{}'.format(skill.sSkillDesc)
			print '限制等级：{}'.format(skill.iLiminitLv)
			print '当前等级：{}'.format(skill.level)
			print '属性：{}'.format(skill.iAttr)
			print '是否可用：{}'.format(skill.iUse)
			print '-------------------------------------'

	@endPoint.result
	def rpcSkillGridStatus(self,ep,who,reqMsg):#角色技能列表
		print 'chang skil grid=',reqMsg.iValue

	@endPoint.result
	def rpcRoleSkillInfo(self,ep,who,reqMsg):#单个技能
		print 'Id：{}'.format(reqMsg.iSkillNo)
		print '技能名称：{}'.format(reqMsg.sSkillName)
		print '描述：{}'.format(reqMsg.sSkillDesc)
		print '限制等级：{}'.format(reqMsg.iLiminitLv)
		print '当前等级：{}'.format(reqMsg.level)
		print '属性：{}'.format(reqMsg.iAttr)
		print '是否可用：{}'.format(reqMsg.iUse)
		print '-------------------------------------'
	
	@endPoint.result
	def rpcAuctionGoodsList(self,ep,who,reqMsg):#拍卖物品列表
		print 'auction goods info list'
		for info in reqMsg.goods:
			print info

	@endPoint.result
	def rpcAuctionGoodsInfo(self,ep,who,reqMsg):#
		print 'auction goods Info'
		print reqMsg

	@endPoint.result
	def rpcMailDetails(self,ep,who,reqMsg):#
		print 'mail: open mail info '
		print reqMsg
	@endPoint.result
	def rpcPushGuildInfo(self,ep,who,reqMsg):#
		print 'rpcPushGuildInfo '
		print reqMsg
	@endPoint.result
	def rpcPushGuildMember(self,ep,who,reqMsg):#
		print 'rpcPushGuildMember '
		print reqMsg
	@endPoint.result
	def rpcPushGuildList(self,ep,who,reqMsg):#
		print 'rpcPushGuildList '
		print reqMsg
	@endPoint.result
	def rpcPushGuildJoinList(self,ep,who,reqMsg):#
		print 'rpcPushGuildJoinList '
		print reqMsg

	@endPoint.result
	def rpcClientMonsterFlush(self,ep,who,reqMsg):#测试下发怪物
		print 'rpcClientMonsterFlush '
		for monster in reqMsg.monsterList:
			print '=====',monster.iId,monster.iNo,monster.sClass,monster.sAi,monster.iHP

	@endPoint.result
	def rpcClientTaskChapterList(self,ep,who,reqMsg):#章节
		print 'rpcClientTaskChapterList '
		for task in reqMsg.list:
			print '========',task.iNo,u.trans(task.sName)

	@endPoint.result
	def rpcClientTaskList(self,ep,who,reqMsg):#章节任务
		print 'rpcClientTaskList '
		for task in reqMsg.tasks:
			print task.iNo,u.trans(task.sName),u.trans(task.sDesc),u.trans(task.sTarget),task.iState

	@endPoint.result
	def rpcClientArenaRoom(self,ep,who,reqMsg):
		print 'rpcClientArenaRoom '
		record=reqMsg.record
		iWinRate=record.iWinRate
		iWeekWin=record.iWeekWin
		iRank=record.iRank

		iRemainEnterTime=reqMsg.iRemainEnterTime
		print 'winRate:',iWinRate,' weekWin:',iWeekWin,' Rank:',iRank,' EnterTime:',iRemainEnterTime

		roomInfo=reqMsg.roomInfo
		for room in roomInfo:
			iRoomNo=room.iRoomNo
			iModel=room.iModel
			iRoomCreater=room.iRoomCreater
			iAFighting=room.iAFighting
			iCurNum=room.iCurNum
			iMaxNum=room.iMaxNum
			sCreaterName=room.sCreaterName
			print 'roomNo:',iRoomNo,' model:',iModel,' creater:',iRoomCreater,' fighting:',iAFighting,' curNum:',iCurNum,' maxNum:',iMaxNum,' sCreaterName:',sCreaterName

	@endPoint.result
	def rpcClientFlushRoomInfo(self,ep,who,reqMsg):
		roomInfo=reqMsg.roomInfo
		for room in roomInfo:
			iRoomNo=room.iRoomNo
			iModel=room.iModel
			iRoomCreater=room.iRoomCreater
			iAFighting=room.iAFighting
			iCurNum=room.iCurNum
			iMaxNum=room.iMaxNum
			print 'roomNo:',iRoomNo,' model:',iModel,' creater:',iRoomCreater,' fighting:',iAFighting,' curNum:',iCurNum,' maxNum:',iMaxNum

	@endPoint.result
	def rpcClientRoomPlayer(self,ep,who,reqMsg):
		for palyer in reqMsg.oPlayer:
			print "ID:",palyer.iRoleId," status:",palyer.iStatus," pos:",palyer.iPos," lv:",palyer.iLevel," fighting:",palyer.iFighting

	@endPoint.result
	def rpcClientModel(self,ep,who,reqMsg):
		print 'rpcClientArenaRoom '
		print reqMsg.iValue



import c
import u
import log


import timeU
import mysqlCnt
import account
import role
import mainService
import props
import props_pb2
