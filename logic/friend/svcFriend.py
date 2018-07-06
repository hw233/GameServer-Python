#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
import factory
PRAISE_ADDFP=5#点赞增加的友情点
#即时通信服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcAddFriend(self,ep,who,reqMsg):return rpcAddFriend(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcDelFriend(self,ep,who,reqMsg):return rpcDelFriend(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcSendImMsg(self,ep,who,reqMsg):return rpcSendImMsg(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcFetchImMsg(self,ep,who,reqMsg):return rpcFetchImMsg(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcFetchSysMsg(self,ep,who,reqMsg):return rpcFetchSysMsg(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcSearchPlayer(self,ep,who,reqMsg):return rpcSearchPlayer(self,ep,who,reqMsg)#		
	@endPoint.result
	def rpcRecentContact(self,ep,who,reqMsg):return rpcRecentContact(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcSetSign(self,ep,who,reqMsg):return rpcSetSign(self,ep,who,reqMsg)#		
	@endPoint.result
	def rpcDragBlack(self,ep,who,reqMsg):return rpcDragBlack(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcRemoveBlack(self,ep,who,reqMsg):return rpcRemoveBlack(self,ep,who,reqMsg)#				
	@endPoint.result
	def rpcSurroundPlayer(self,ep,who,reqMsg):return rpcSurroundPlayer(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcResumeAttrReq(self,ep,who,reqMsg):return rpcResumeAttrReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcResumeEquipReq(self,ep,who,reqMsg):return rpcResumeEquipReq(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcChatUiInfo(self,ep,who,reqMsg):return rpcChatUiInfo(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcFightCmp(self,ep,who,reqMsg):return rpcFightCmp(self,ep,who,reqMsg)#
	@endPoint.result
	def rpcPraise(self,ep,who,reqMsg):return rpcPraise(self,ep,who,reqMsg)#点赞
	@endPoint.result
	def rpcGetPraise(self,ep,who,reqMsg):return rpcGetPraise(self,ep,who,reqMsg)#收赞
	@endPoint.result
	def rpcFriendBrief(self,ep,who,reqMsg):return rpcFriendBrief(self,ep,who,reqMsg)#好友的简简要(ID,战力)信息
	@endPoint.result
	def rpcFriMsg(self,ep,who,reqMsg):return rpcFriMsg(self,ep,who,reqMsg)#请求好友信息,用于直接在世界聊天请求

def rpcFriMsg(self,ep,who,reqMsg):
	iReceiverId=reqMsg.iValue
	obj=role.gKeeper.getObj(iReceiverId)
	obj=obj if obj else resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iReceiverId)
	if not obj:
		raise Exception, '找不到目标玩家的resume数据:ID={}'.format(iReceiverId)
	oRoleAttr=im_pb2.roleReq()
	oRoleAttr.iReceiverId=iReceiverId
	oRoleAttr.sName=obj.name
	oRoleAttr.iLevel=obj.level
	oRoleAttr.iSchool=obj.school
	oRoleAttr.bFriend=iReceiverId in who.friendCtn.dKeyMapItem
	return oRoleAttr

def rpcFriendBrief(self,ep,who,reqMsg):
	roleList=im_pb2.roleList()
	roleList.iType=1
	for oFriend in who.friendCtn.getAllValues():
		oResume=oFriend.oResume
		player=roleList.roles.add()
		player.iRoleId=oResume.ownerId
		player.iFightAbility=oResume.fightAbility()
	return roleList

def rpcAddFriend(self,ep,who,reqMsg):#
	return tryAddFriend(ep, who, reqMsg.iValue)

def tryAddFriend(ep,who,iTargetId):
	iAccordId=who.id
	if who.id==iTargetId:
		ep.rpcTips('不能加自己为好友.')
		return False
	oFriend=who.friendCtn.getItem(iTargetId)
	if oFriend:
		ep.rpcTips('您已经加了此好友.')
		return False

	iFriendsMax=who.friendCtn.maxFriendAmount()	#好友的最大数量
	#检查自己的好友数量是否到达最大值
	if who.friendCtn.itemCount()>=iFriendsMax:
		ep.rpcTips('你的好友数量过多,无法添加新的好友')
		return  False
	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTargetId)
	oFriendCtn=block.blockFriend.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTargetId)
	if not oFriendCtn:
		raise Exception, '找不到目标玩家:ID={}'.format(iTargetId)
	#检查目标的好友数量是否达到最大值
	if oFriendCtn.itemCount()>=iFriendsMax:
		ep.rpcTips('对方好友数量过多,无法添加新的好友')
		return False

	sAddedSet = gdAddedSet.setdefault(who.id, set())
	
	if iTargetId in sAddedSet:#防止重复发消息球和请求框	
		ep.rpcTips('已向 {} 发出了邀请,请等候回应'.format(targetResume.name))
		return False
	sAddedSet.add(iTargetId)

	ep.rpcTips('已向 {} 发出了邀请,请等候回应'.format(targetResume.name))
	ep1=mainService.getEndPointByRoleId(iTargetId)
	bRes=False
	if ep1:	#对方在线(内存中)
		bRes=sendAddFriendMsg(who, who.id, iTargetId)
	else:
		#对方当前不在线,将请求信息加入到resume中当玩家上线时,提示确认添加好友请求
		ep.rpcTips('好友请求也发出,{}将在下次登录时处理'.format(targetResume.name))
		targetResume.addLoginCall(resume.SENDADDFRIENDMSG, who.id, iTargetId)
	who=role.gKeeper.getObj(iAccordId)
	if who:
		bRes = bRes or who.friendCtn.getItem(iAccordId)
	return bRes
	 
#生成好友请求信息
def confirmationBoxReq(iAccordId):
	accordResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iAccordId)
	req=common_pb2.confirmationBoxReq()
	req.sContent='{} 请求添加你为好友'.format(accordResume.name)
	req.sSubContent=''
	req.sSelect='Q_接受Q_拒绝'
	req.iTimeout=30*60*1000 #确认框超时时间
	return req

#推送未处理的好友请求
def checkUnDealFriMsg(who, ep):
	iMeId=who.id
	sPasvAddedSet=gdPasvAddedSet.setdefault(iMeId, set())
	#在sendAddFriendMsg函数会对sPasvAddedSet进行操作,因此此处直接复制一个lPasvAddedSet
	lPasvAddedSet = list(sPasvAddedSet) 
	for iRoleId in lPasvAddedSet:
		sendAddFriendMsg(who, iRoleId, iMeId)

#下发添加好友请求消息
#此时iAccordId所对应的角色不一定在线(内存中)
#iTargetId对应的角色一定在内存中
def sendAddFriendMsg(who, iAccordId, iTargetId):
	# print '**********   {}当前在线   **********'
	ep=mainService.getEndPointByRoleId(iTargetId)
	if not ep:
		return False

	sPasvAddedSet = gdPasvAddedSet.setdefault(iTargetId, set())
	sPasvAddedSet.add(iAccordId)	#

	bFail,uMsg=ep.rpcPushMsgBall(common_pb2.TYPE_ADD_FRIEND, 3*60*60*1000)	#好友消息球,策划定超时时间3个小时
	if bFail: #超时(客户端不处理超时,掉线超时)
		gdAddedSet.get(iAccordId, set()).discard(iTargetId)
		if iAccordId in gdAddedSet and not gdAddedSet[iAccordId]:
			del gdAddedSet[iAccordId]
		oTargetRole=role.gKeeper.getObj(iTargetId)
		if oTargetRole and not oTargetRole.iDisConnectStamp:#客户端不处理超时
			sPasvAddedSet.discard(iAccordId)	#
		return False

	sPasvAddedSet.discard(iAccordId)	#
	if not sPasvAddedSet:
		gdPasvAddedSet.pop(iTargetId, None)

	ep=mainService.getEndPointByRoleId(iTargetId)
	if not ep:
		return False
	reqMsg=confirmationBoxReq(iAccordId)	#生成请求信息
	bFail,uResponse=ep.rpcConfirmBox(reqMsg)	#向iTarget对象发送好友请求
	bAgree,sNoReason=False,''	#是否同意,拒绝原因
	if bFail or uResponse.iValue!=0:
		#iTarget拒绝iAccordId的好友请求
		bAgree=False	
	else:	
		#iTarget同意添加iAccordId为好友
		bAgree=True 
		addFriend(iTargetId, iAccordId)

	gdAddedSet.get(iAccordId, set()).discard(iTargetId)
	if iAccordId in gdAddedSet and not gdAddedSet[iAccordId]:
		del gdAddedSet[iAccordId]

	ep1=mainService.getEndPointByRoleId(iAccordId)

	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iAccordId)
	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTargetId)
	if not bAgree:	#iTargetId拒绝iAccordId的好友请求
		if ep1:	#角色在线
			ep1.rpcTips('{}拒绝你的好友请求'.format(targetResume.name))
		else:
			selfResume.addLoginCall(resume.CHECKADDFRIENDREPLAY, bAgree, iAccordId, iTargetId)
	else:	#iTargetId同意iAccordId的好友请求
		if ep1:	#角色在线且对方同意添加好友
			addFriend(iAccordId, iTargetId)	
		else:
			selfResume.addLoginCall(resume.CHECKADDFRIENDREPLAY, bAgree, iAccordId, iTargetId)
	return bAgree	

#检查添加好友请求信息对方的回应
#此时iAccordId对应的role一定在内存中
def checkAddFriendReplay(who, bAgree, iAccordId, iTargetId):
	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTargetId)
	if not bAgree:	#iTarget不同意添加好友
		ep=mainService.getEndPointByRoleId(iAccordId)
		if not ep:
			return
		ep.rpcTips('{}拒绝你的好友请求'.format(targetResume.name))	
		return
	addFriend(iAccordId, iTargetId)	#将对方添加为好友

#添加好友函数
def addFriend(iSelfId, iFriendId):
	who=role.gKeeper.getObj(iSelfId)
	if not who:
		return
	if who.friendCtn.getItem(iFriendId):	#iFriendId也在好友列表
		return 
	obj=friend.new(iFriendId)	
	who.friendCtn.addItem(obj)

	friendResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iFriendId)
	friendResume.addInterestMe(who.id)

	ep=mainService.getEndPointByRoleId(iSelfId)
	if not ep:
		return
	roleList=im_pb2.roleList()
	roleList.iType=1
	roleChange(roleList,obj.oResume,who)
	ep.rpcFriendChange(roleList)#好友变更

#删除好友处理
def delFriend(who, iSelfId, iTargetId):
	oFriend=who.friendCtn.getItem(iTargetId)
	if not oFriend:
		return False
	who.friendCtn.removeItem(oFriend)

	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTargetId)
	if targetResume:
		targetResume.removeInterestMe(who.id)

	#删除好友成功,发送好友变更消息
	if targetResume.isPraise(iSelfId):  #如果被点赞,删除的时候先pop出存放的list
		targetResume.getPraised(iSelfId)
	ep=mainService.getEndPointByRoleId(iSelfId)	
	if not ep:
		return False
	roleList=im_pb2.roleList()
	roleList.iType=2
	roleChange(roleList,oFriend.oResume,who)
	ep.rpcFriendChange(roleList)#好友变更
	return True

def rpcDelFriend(self,ep,who,reqMsg):
	iTargetId=reqMsg.iValue
	bDelOver=delFriend(who, who.id, iTargetId)
	if not bDelOver:
		return
	ep1=mainService.getEndPointByRoleId(iTargetId)
	if ep1:	#对方角色对象在线
		oRole=role.gKeeper.getObj(iTargetId)
		delFriend(oRole, iTargetId, who.id)
	else:
		targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iTargetId)
		targetResume.addLoginCall(resume.DELFRIEND, iTargetId, who.id)

#删除角色时,从该角色遍历该角色的好友的好友解除好友关系
#iDelRoleId被删除的角色ID
def delFriendOnDelRole(iDelRoleId):
	oFriendCtn=block.blockFriend.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iDelRoleId)
	for iFriRoleId in oFriendCtn.getAllKeys():	#被删除角色的好友
		ep=mainService.getEndPointByRoleId(iFriRoleId)
		if ep: 	#好友在线
			delFriend(role.gKeeper.getObj(iFriRoleId), iFriRoleId, iDelRoleId)
		else:		#好友不在线
			friendResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iFriRoleId)
			friendResume.addLoginCall(resume.DELFRIEND, iFriRoleId, iDelRoleId)
	return True

def rpcSendImMsg(self,ep,who,reqMsg):
	iSenderId=who.id
	sContent=reqMsg.sContent
	iReceiverId=reqMsg.iReceiverId
	sInvalid=u.isInvalidText(sContent)
	if sInvalid:
		ep.rpcTips('您输入的{}为非法字符，请重新输入!'.format(sInvalid))
		return False
	if len(sContent)>100:
		return False
	#过滤敏感词,把敏感词屏蔽成xxx
	sContent=trie.fliter(sContent)
	rpcSendImMsg
	if iReceiverId==iSenderId:
		ep.rpcTips('不能发消息给自己.')
		return False
	#对方是否拒收任何人的消息
	#todo 检查收消息的人是否在自己的黑名单上.
	senderResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	sSenderName=senderResume.name
	receiverResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iReceiverId)
	if not receiverResume:
		return False
	#todo 检查收消息人的消息箱是否满了
	if receiverResume.imMsgAmount()>=receiverResume.maxReceiveMsg():
		ep.rpcTips('对方未读消息已满，无法继续发送')
		return False
	receiverResume.addImMsg(iSenderId,sSenderName,sContent)
	senderResume.addRecentContact(iReceiverId)
	return True
	#ep.rpcImMsgArrival(iSenderId)	
	
def rpcFetchImMsg(self,ep,who,reqMsg):#请求具体聊天内容
	iSenderId=reqMsg.iValue
	chatMsgRelay=im_pb2.chatMsgRelay()
	chatMsgRelay.iSenderId=iSenderId
	bHas=False
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	for obj in selfResume.popImMsgBySenderId(iSenderId):
		aMsg=chatMsgRelay.imMsg.add()
		aMsg.sContent=obj.content()
		aMsg.iSendStamp=obj.sendStamp()
		bHas=True
	if not bHas:
		return
	selfResume.addRecentContact(iSenderId)
	ep.rpcSendImMsg(chatMsgRelay)
	
def rpcSearchPlayer(self,ep,who,reqMsg):
	sString=reqMsg.iValue.strip()
	if not sString:
		ep.rpcTips('搜索名字不能为空')
		return
	iLastSearch=getattr(who,'iLastSearch',0)
	if timeU.getStamp()-iLastSearch<5:
		ep.rpcTips('5秒内只能搜索一次，请稍后再试')
		return
	who.iLastSearch=timeU.getStamp()
	#todo 控制玩家搜索频率
	if sString.isdigit():
		rs=db4ms.gConnectionPool.query(sql.SEARCH_ROLE_ID,sString)
		if not rs.rows:
			rs=db4ms.gConnectionPool.query(sql.SEARCH_ROLE_NAME,sString)
	else:
		rs=db4ms.gConnectionPool.query(sql.SEARCH_ROLE_NAME,sString)
	if not rs.rows:
		ep.rpcTips('所查找的玩家不存在')
		return
	roleList=im_pb2.roleList()
	roleList.iType=5
	for roleId in rs.rows:#发送找到的玩家名字和等级
		targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,roleId[0])	
		roleChange(roleList,targetResume,who)
	# if not sString.isdigit():
	# 	ep.rpcFriendList(roleList)
	# 	return
	# for roleId in rs2.rows:#发送找到的玩家名字和等级
	# 	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,roleId[0])	
	# 	roleChange(roleList,targetResume)

	ep.rpcFriendList(roleList)

def rpcSetSign(self,ep,who,reqMsg):
	sSign=reqMsg.iValue
	#todo过滤敏感字
	selfRsume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	selfResume.setSign(sSign)	

def rpcDragBlack(self,ep,who,reqMsg):
	iTarget=reqMsg.iValue
	if who.id==iTarget:
		ep.rpcTips('不能拉黑自己.')
		return
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	if selfResume.isBlack(iTarget):
		ep.rpcTips('您已将此人拉黑.')
		return
	#iMax=who.friendCtn.maxFriendAmount()
	# if who.friendCtn.itemCount()>=iMax:
	# 	ep.rpcTips('好友数不能超过{}人'.format(iMax))
	# 	return  False
	#黑名单人数满了
	oFriend=who.friendCtn.getItem(iTarget)
	if oFriend:
		ep.rpcTips('拉黑前请先解除好友关系')
		return		
	selfResume.blackAdd(iTarget)
	ep.rpcTips('拉黑成功')

	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTarget)	
	roleList=im_pb2.roleList()
	roleList.iType=1
	roleChange(roleList,targetResume,who)
	ep.rpcBlackChange(roleList)#黑名单变更

def rpcRemoveBlack(self,ep,who,reqMsg):
	iTarget=reqMsg.iValue
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	if not selfResume.isBlack(iTarget):
		ep.rpcTips('此人不在黑名单中')
		return
	selfResume.blackRemove(iTarget)
	ep.rpcTips('解除黑名单')

	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTarget)	
	roleList=im_pb2.roleList()
	roleList.iType=2
	roleChange(roleList,targetResume,who)
	ep.rpcBlackChange(roleList)#黑名单变更
				
def rpcFetchSysMsg(self,ep,who,reqMsg):#取系统消息
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	obj=selfResume.popSysMsg()
	if not obj:
		raise Exception,'没有系统消息可取.'
	if selfResume.sysMsgCount()>0:#通知还有下一条系统消息
		ep.rpcSysMsgArrival()
	return obj.content(),obj.sendStamp()

def rpcSurroundPlayer(self,ep,who,reqMsg):
	playerList=im_pb2.roleList()
	playerList.iType=3
	lKeys=list(who.friendCtn.getAllKeys())
	for iRoleId in scene.getSurroundPlayer(who):
		if iRoleId==who.id:
			continue
		oRole=role.gKeeper.getObj(iRoleId)
		if oRole.name==c.BORN_NAME:
			continue
		player=playerList.roles.add()
		player.iRoleId=oRole.id
		player.sRoleName=oRole.name
		player.iRoleLevel=oRole.level
		player.iRoleSchool=oRole.school
		player.iFightAbility=oRole.fightAbility()
		player.iIsFriend=int(oRole.id in lKeys) #填充是否是好友属性
	ep.rpcFriendList(playerList)

def rpcRecentContact(self,ep,who,reqMsg):
	who.friendCtn.rpcRecentContact(ep)

def rpcResumeAttrReq(self,ep,who,reqMsg):
	iTarget=reqMsg.iValue
	# oTargetResume=resume.gKeeper.getObj(iTarget)
	# if not oTargetResume or not role.gKeeper.getObj(iTarget):
	# 	ep.rpcTips('你查看的角色未上线')
	# 	return
	#todo:这里不能频繁地从工厂拿对象啊.要从keeper上拿
	oTargetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTarget)
	if not oTargetResume:
		raise Exception, '角色简要信息丢失,角色ID:{}'.format(iTarget)
	# oTargetResume=factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iTarget)
	msg=oTargetResume.getAttrMsg()
	ep.rpcFriendAttr(msg)

def rpcResumeEquipReq(self,ep,who,reqMsg):
	iTarget=reqMsg.iValue
	# oTargetResume=resume.gKeeper.getObj(iTarget)
	#  if not oTargetResume or not role.gKeeper.getObj(iTarget):
	# 	ep.rpcTips('你查看的角色未上线')
	# 	return
	# oTargetResume=factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iTarget)
	ep.rpcFriendEquip(block.blockPackage.getEquipMsg(iTarget))

def rpcChatUiInfo(self,ep,who,reqMsg):
	iTarget=reqMsg.iValue
	oTargetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTarget)
	if not oTargetResume:
		return
	ep.rpcChatUiInfoDown(oTargetResume.getAttrMsg())

def roleChange(roleList,oResume,cRole):
	player=roleList.roles.add()
	player.iRoleId=oResume.ownerId
	player.bOnline=bool(role.gKeeper.getObj(oResume.ownerId))
	player.sRoleName=oResume.name
	player.iRoleLevel=oResume.level
	player.iRoleSchool=oResume.school
	player.iFightAbility=oResume.fightAbility()
	player.bPraise=bool(cRole.friendCtn.day.fetch(oResume.ownerId,0))
	player.iGetPraise=cRole.friendCtn.praiseStatus(oResume.ownerId)
	oFriend=cRole.friendCtn.getItem(oResume.ownerId)
	if roleList.iType==2 or not oFriend:#删除好友不用广播下面的
		return
	player.iTacit=oFriend.tacit()
	player.iTacitStar=oFriend.tacitStar()
	player.iNextTacit=oFriend.nextTacit()
	player.iFightAdd=oFriend.fightAdd()
	player.iIsFriend=int(oResume.ownerId in cRole.friendCtn.getAllKeys())	#是否是好友

def rpcPraise(self,ep,who,reqMsg):#点赞
	iTarget=reqMsg.iValue#被点赞人的ID
	if who.id==iTarget:
		ep.rpcTips('不能对自己点赞')
		return
	if who.day.fetch('praiseTimes',0)>=10:
		ep.rpcTips('你今天的点赞次数已经用完')
		return
	oFriend=who.friendCtn.getItem(iTarget)
	if not oFriend:
		ep.rpcTips('对方不是你的好友,不能点赞')
		return
	if oFriend.isNewFriend():
		ep.rpcTips('新加好友要第二天才能点赞')
		return
	if who.friendCtn.day.fetch(iTarget,0):
		ep.rpcTips('今天已经对该好友点过赞了')
		return
	who.day.add('praiseTimes',1)
	who.friendCtn.day.set(iTarget,1)
	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iTarget)
	targetResume.bePraised(who.id)
	ep.rpcTips('点赞成功')
	roleList=im_pb2.roleList()
	roleList.iType=3
	roleChange(roleList,targetResume,who)
	ep.rpcFriendChange(roleList)#好友变更
	oTarget=role.gKeeper.getObj(iTarget)
	ep2=mainService.getEndPointByRoleId(iTarget)
	if not ep2 or not oTarget:
		return
	#对方在线的时候还要更变我在对方的好友列表信息
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	roleList2=im_pb2.roleList()
	roleList2.iType=3
	roleChange(roleList2,selfResume,oTarget)
	ep2.rpcFriendChange(roleList2)

def rpcGetPraise(self,ep,who,reqMsg):#收赞
	iFriendId=reqMsg.iValue
	selfResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,who.id)
	targetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iFriendId)
	if not selfResume.isPraise(iFriendId):
		ep.rpcTips('该好友并没有对你点赞')
		return
	selfResume.getPraised(iFriendId)
	who.active.addFriendPoint(PRAISE_ADDFP,'收赞')
	ep.rpcTips('收赞成功')
	roleList=im_pb2.roleList()
	roleList.iType=3
	roleChange(roleList,targetResume,who)
	ep.rpcFriendChange(roleList)#好友变更

#也请求加好友缓存,避免同一角色对同一对象多次发出好友请求
gdAddedSet={}	#{iRoleId:set([请求的好友ID])}
#被请求加好友缓存,在角色重新登录时继续推送未处理的好友请求
gdPasvAddedSet={}	#{iMeId:set(请求加ME的iRoleID)}

import role
import resume
import sql
import u
import c
import misc
import friend
import im_pb2
import factoryConcrete
import scene
import db4ms
import timeU
import block.blockPackage
import factory
import props.equip
import common_pb2
import mainService
import block.blockFriend
import trie