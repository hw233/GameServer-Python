# -*- coding: utf-8 -*-
# 队伍服务
import endPoint
import team_pb2


def handleLock(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		if who.inEscort() or who.inTreasure():
			message.tips(who, "当前状态下不能进行此类操作")
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			raise
	return newFunc


class cService(team_pb2.terminal2main):

	@endPoint.result
	@handleLock
	def rpcTeamCreate(self, ep, who, reqMsg): return rpcTeamCreate(who, reqMsg)
	
	@endPoint.result
	def rpcTeamQuit(self, ep, who, reqMsg): return rpcTeamQuit(who, reqMsg)
	
	@endPoint.result
	def rpcTeamSetLeader(self, ep, who, reqMsg): return rpcTeamSetLeader(who, reqMsg)
	
	@endPoint.result
	def rpcTeamKick(self, ep, who, reqMsg): return rpcTeamKick(who, reqMsg)
	
	@endPoint.result
	def rpcTeamLeave(self, ep, who, reqMsg): return rpcTeamLeave(who, reqMsg)
	
	@endPoint.result
	@handleLock
	def rpcTeamBack(self, ep, who, reqMsg): return rpcTeamBack(who, reqMsg)
	
	@endPoint.result
	@handleLock
	def rpcTeamInvite(self, ep, who, reqMsg): return rpcTeamInvite(who, reqMsg)
	
	@endPoint.result
	@handleLock
	def rpcTeamApplyJoin(self, ep, who, reqMsg): return rpcTeamApplyJoin(who, reqMsg)
	
	@endPoint.result
	def rpcTeamApplyJoinAccept(self, ep, who, reqMsg): return rpcTeamApplyJoinAccept(who, reqMsg)
	
	@endPoint.result
	def rpcTeamApplyJoinClear(self, ep, who, reqMsg): return rpcTeamApplyJoinClear(who, reqMsg)
	
# 	@endPoint.result
# 	def rpcTeamLineupSet(self, ep, who, reqMsg): return rpcTeamLineupSet(who, reqMsg)

	@endPoint.result
	def rpcTeamSetPos(self, ep, who, reqMsg): return rpcTeamSetPos(who, reqMsg)
	
	@endPoint.result
	def rpcTeamInviteBack(self, ep, who, reqMsg): return rpcTeamInviteBack(who, reqMsg)

	@endPoint.result
	def rpcTeamSetTarget(self, ep, who, reqMsg): return team.platformservice.rpcTeamSetTarget(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcTeamAutoMatch(self, ep, who, reqMsg): return team.platformservice.rpcTeamAutoMatch(who, reqMsg)

	@endPoint.result
	def rpcTeamRefreshMatch(self, ep, who, reqMsg): return team.platformservice.rpcTeamRefreshMatch(who, reqMsg)
	
	@endPoint.result
	def rpcFastChat(self, ep, who, reqMsg): return rpcFastChat(who, reqMsg)

def checkLeaderOP(who,isSetPos=False):
	'''检查队长操作
	'''
	if not who:
		return 0
	if not isSetPos and who.inWar():
		return 0
	teamObj = who.getTeamObj()
	if not teamObj:
		return 0
	if not teamObj.isLeader(who.id):
		return 0
	return 1

def rpcTeamCreate(who, reqMsg):
	'''创建队伍
	'''
	if who.inWar():
		return
	if who.getTeamObj():
		return
	teamObj = team.makeTeam(who)
	if not teamObj:
		return
	message.tips(who, "队伍创建成功，你是队长！")
	team.platform.removePlayerMatch(who)
				
def rpcTeamQuit(who, reqMsg):
	'''退出队伍
	'''
	if who.inWar():
		return
	teamObj = who.getTeamObj()
	if not teamObj:
		return

	if team.checkDenyQuitTeam(who, "退出队伍"):
		return
	
	isLeader = teamObj.isLeader(who.id)
	teamObj = teamObj.this()
	teamObj.remove(who.id)
	# team.platform.teamQuit(who, teamObj.id)
	if teamObj.isReleased():
		message.tips(who, "你解散了队伍")
		team.platform.teamRelease(teamObj.id)
	else:
		message.tips(who, "你已离开队伍")
		if isLeader:
			teamObj.tips("$name成为新队长", teamObj.leader,teamObj.leader)
			#message.tips(teamObj.getOnlineList(), teamObj.transString("$name成为1新队长", teamObj.leader))
			team.platformservice.updateTarget(teamObj)	

		team.platformservice.teamMemberChange(teamObj)
		team.platformservice.teamKickDuel(who.id, teamObj.id, False)

def rpcTeamSetLeader(who, reqMsg):
	'''升为队长
	'''
	targetId = reqMsg.roleId
	if targetId == who.id:
		return
	targetObj = getRole(targetId)
	if not checkSetLeader(who, targetObj):
		return
	
	message.tips(who, "邀请信息已发送，正在等待对方确认")

	teamObj = who.getTeamObj()
	if not hasattr(teamObj, "inviteLeaderList"):
		teamObj.inviteLeaderList = {}
	if getSecond() - teamObj.inviteLeaderList.get(targetId, 0) < 20:
		return
	else:
		teamObj.inviteLeaderList[targetId] = getSecond()
	
	pid = who.id
	targetName = targetObj.name
	content = "#C06%s#n邀请你成为队长，是否接受？\nQ拒绝#20\nQ接受" % who.name
	message.confirmBoxNew(targetObj, functor(responseSetLeader, pid), content)

def responseSetLeader(targetObj, yes, pid):
	who = getRole(pid)
	if not who:
		return
	
	teamObj = who.getTeamObj()
	if not teamObj:
		return

	if targetObj.id in teamObj.inviteLeaderList:
		del teamObj.inviteLeaderList[targetObj.id]

	if not yes:
		message.tips(pid, "#C01%s#n拒绝了你的邀请" % targetObj.name)
		return

	if not checkSetLeader(who, targetObj):
		return

	teamObj = who.getTeamObj()
	teamObj.setLeader(targetObj)
	rpcTeamInfo(teamObj)
	rpcTeamBroadcastMake(teamObj)
	teamObj.teamMessage("$name成为队长", targetObj.id)

	message.tips(targetObj, "你已成为队长！")
	if teamObj.leader:
		teamObj.tips("$name成为队长", targetObj.id, teamObj.leader)
	team.platformservice.updateTarget(teamObj)
	
	
def checkSetLeader(who, targetObj):
	if not checkLeaderOP(who):
		return 0
	if not targetObj:
		message.tips(who, "这位队员处于离线状态，不能当队长。")
		return 0
	teamObj = who.getTeamObj()
	if not teamObj.isLeader(who.id):
		message.tips(targetObj.id, "队长已移交给其他队员")
		return 0
	if targetObj.id not in teamObj.getInTeamList():
		return 0
	return 1
	
def rpcTeamKick(who, reqMsg):
	'''请离队伍
	'''
	targetId = reqMsg.roleId
	if targetId == who.id:
		return
	if not checkLeaderOP(who):
		return
	teamObj = who.getTeamObj()
	if targetId not in teamObj.memberList:
		return
	info = teamObj.infoList[targetId]
	teamObj.remove(targetId)
	message.tips(targetId, "你被请离队伍")
	teamObj.tips("#C01%s#n被请离了队伍" % info["name"])
	team.platformservice.teamMemberChange(teamObj)
	team.platformservice.teamKickDuel(targetId, teamObj.id)
	#组队竞技
	actObj = activity.getActivity("teamRace")
	if actObj:
		actObj.teamKick(teamObj, targetId)

def rpcTeamLeave(who, reqMsg):
	'''暂离队伍
	'''
	if who.inWar():
		return
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	if who.id not in teamObj.getInTeamList():
		return
	if teamObj.isLeader(who.id): # 队长不能暂离
		return
	if team.checkDenyQuitTeam(who, "暂离队伍"):
		return
	teamObj.setLeave(who)
	
def rpcTeamBack(who, reqMsg):
	'''回归队伍
	'''
	if not checkBack(who):
		return

	teamObj = who.getTeamObj()
	leaderObj = getRole(teamObj.leader)
	if not leaderObj:
		return
	if not scene.validTransfer(who):
		return
	scene.switchScene(who, leaderObj.sceneId, leaderObj.x, leaderObj.y)
	if leaderObj.inWar() and not leaderObj.inWatchWar():
		leaderObj.war.addWatch(who, leaderObj.warrior.side)
		who.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
		message.tips(who, "队伍正在战斗中，进入观战")
	else:
		doBack(who)
	
def doBack(who, isWarEnd=False):
	if not checkBack(who):
		return
	teamObj = who.getTeamObj()
	leaderObj = getRole(teamObj.leader)
	if leaderObj.inWar():
		return
	if isWarEnd:
		if not scene.validTransfer(who):
			return
		scene.switchScene(who, leaderObj.sceneId, leaderObj.x, leaderObj.y)

	teamObj.setBack(who)
	teamObj.teamMessage("$name回归队伍", who.id)
	if isWarEnd:
		message.tips(who, "队伍战斗结束，自动归队")
	else:
		message.tips(who, "你已回归队伍")
	
def checkBack(who):
	if who.inWar():
		return False
	teamObj = who.getTeamObj()
	if not teamObj:
		return False
	if teamObj.getState(who.id) != TEAM_STATE_LEAVE:
		return False
	return True
	
def rpcTeamInvite(who, reqMsg):
	'''邀请入队
	'''
	targetId = reqMsg.roleId
	if targetId == who.id:
		return
	targetObj = getRole(targetId)
	if targetObj.level < 13:
		message.tips(who, "对方等级#C04<13级#n，无法加入队伍")
		return
	teamObj = who.getTeamObj()
	if not teamObj:
		teamObj = team.makeTeam(who)
		if not teamObj:
			return
		message.tips(who, "队伍创建成功，你是队长！")
	if not checkInvite(who, targetObj):
		return
	if task.offlineTask.inOfflineTask(targetObj): # 离线任务中的玩家，直接入队
		doInvite(who, targetObj)
		return
	if targetId in teamObj.joinList: # 在申请列表中，直接入队
		doInvite(who, targetObj)
		return
	
	# 防止骚扰
	if not hasattr(teamObj, "inviteList"):
		teamObj.inviteList = {}
	if getSecond() - teamObj.inviteList.get(targetId, 0) < 20:
		return
	else:
		teamObj.inviteList[targetId] = getSecond()
		
	message.tips(who, "邀请信息已发送，正在等待对方确认")
	pid = who.id
	myGreenlet.cGreenlet.spawn(sendInvite, pid, targetId)

def sendInvite(pid, targetId):
	who = getRole(pid)
	if not who:
		return
	targetObj = getRole(targetId)
	if not targetObj:
		return
	if targetObj.getTeamObj():
		return
	
	content = "#C06%s#n邀请你加入队伍，是否接受？\nQ拒绝#20\nQ接受" % who.name
	message.confirmBoxNew(targetObj, functor(responseInvite, pid), content)
		
def responseInvite(targetObj, yes, pid):
	who = getRole(pid)
	if not who:
		return

	teamObj = who.getTeamObj()
	if not teamObj:
		return

	if targetObj.id in teamObj.inviteList:
		del teamObj.inviteList[targetObj.id]

	if not yes:
		message.tips(pid, "#C01%s#n拒绝了你的邀请" % targetObj.name)
		return
	if teamObj.isLeader(who.id): # 队长发的邀请，直接入队
		doInvite(who, targetObj)
	else: # 如果是队员发的邀请，则加入申请列表
		doApplyJoin(targetObj, who)

def doInvite(who, targetObj):
	if not checkInvite(who, targetObj):
		return

	teamObj = who.getTeamObj()
	removeJoinFromAllTeam(targetObj.id)
	teamObj.add(targetObj)
	team.platform.transPlayerTarget(targetObj)
	if targetObj.inWar():
		teamObj.setLeave(targetObj)
		targetObj.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
		message.tips(targetObj, "正在战斗中，自动暂离")
	else:
		if not scene.validTransfer(targetObj):
			teamObj.setLeave(targetObj)
			return
		scene.switchScene(targetObj, who.sceneId, who.x, who.y)
		if who.inWar() and not who.inWatchWar():
			teamObj.setLeave(targetObj)
			who.war.addWatch(targetObj, who.warrior.side)
# 			teamObj.addHandlerForWarEnd(targetObj.id, functor(doBack, targetObj.id, True)) # 队伍战斗结束后处理
			targetObj.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
			message.tips(targetObj, "队伍正在战斗中，进入观战")
	
	
def checkInvite(who, targetObj):
	teamObj = who.getTeamObj()
	if teamObj.size >= MEMBER_LIMIT:
		message.tips(who, "本队伍已满员")
		return 0
	if not targetObj:
		message.tips(who, "对方已下线")
		return 0
	elif targetObj.inEscort():
		message.tips(who, "对方正在运镖中")
		return 0
	elif targetObj.inTreasure():
		message.tips(who, "对方正在探宝中")
		return 0
	if targetObj.getTeamObj():
		if targetObj.getTeamObj() == teamObj:
			message.tips(who, "对方已在本队伍中")
		else:
			message.tips(who, "对方已加入其他队伍")
		return 0
	if team.checkDennyTeam(who, targetObj, "邀请入队"):
		return 0
	if team.checkTeamDennyAdd(who, teamObj, "邀请入队"):
		return
	if getattr(targetObj, "enterCollect", 0):#玩家在收集玩法内不能邀请入队
		message.tips(who, "对方当前无法接受入队")
		return
	return 1

def rpcTeamApplyJoin(who, reqMsg):
	'''申请入队
	'''
	targetId = reqMsg.roleId
	if targetId == who.id:
		return
	# if who.inWar():
	#  	return
	if who.level < 13:
		message.tips(who, "#C0413级#n开启#C02组队系统#n")
		return
	if who.getTeamObj():
		return
	if team.checkDennyTeam(who, None, "申请入队"):
		return
	targetObj = getRole(targetId)
	if not targetObj:
		message.tips(who, "对方已下线")
		return

	teamObj = targetObj.getTeamObj()
	if teamObj:
		if team.checkTeamDennyAdd(who, teamObj, "申请入队"):
			return
		doApplyJoin(who, targetObj)
	else:
		message.confirmBoxNew(who, functor(responseInviteMakeTeam, reqMsg), "对方已离开队伍，是否邀请组队？\nQ取消#20\nQ邀请")
		
def responseInviteMakeTeam(who, yes, reqMsg):
	if yes:
		rpcTeamInvite(who, reqMsg)
	
def doApplyJoin(who, targetObj):
	if not checkApplyJoin(who, targetObj):
		return
	teamObj = targetObj.getTeamObj()
	teamObj.addJoin(who)
	message.tips(who, teamObj.transString("已申请加入$name的队伍，请耐心等候...", teamObj.leader))
	
def checkApplyJoin(who, targetObj):
	if who.getTeamObj():
		return 0
	if not targetObj:
		return 0
	teamObj = targetObj.getTeamObj()
	if not teamObj:
		return 0
	if teamObj.size >= MEMBER_LIMIT:
		message.tips(who, "对方队伍已满")
		return 0
	if who.id in teamObj.joinList:
		message.tips(who, "你已在对方的申请名单中，请稍等...")
		return 0
	if len(teamObj.joinList) >= JOIN_LIMIT:
		message.tips(who, "申请人数已达上限")
		return 0
	return 1
	

def rpcTeamApplyJoinAccept(who, reqMsg):
	'''接受申请入队
	'''
	targetId = reqMsg.roleId
	if targetId == who.id: # 不能接受自己
		return
	
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	if not teamObj.isLeader(who.id):
		message.tips(who, "你不是队长")
		return
	if teamObj.size >= MEMBER_LIMIT:
		message.tips(who, "队伍已经满员，无法再增加新队员")
		teamObj.removeJoin(targetId)
		return
	
	if team.checkTeamDennyAdd(who, teamObj, "接受申请"):
		return
	info = teamObj.removeJoin(targetId)
	if not info:
		return
	
	removeJoinFromAllTeam(targetId, teamObj.id)
	
	targetObj = getRole(targetId)
	if not targetObj:
		message.tips(who, "该玩家已离线，无法接受加入")
		return
	if targetObj.getTeamObj():
		message.tips(who, "该玩家已加入其他队伍，无法接受加入")
		return
	if team.checkDennyTeam(who, targetObj, "接受申请"):
		return
	
	teamObj.add(targetObj)
	team.platform.transPlayerTarget(targetObj)
	if targetObj.inWar():
		teamObj.setLeave(targetObj)
		targetObj.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
		message.tips(targetObj, "正在战斗中，自动暂离")
	else:
		if not scene.validTransfer(targetObj):
			teamObj.setLeave(targetObj)
			return
		scene.switchScene(targetObj, who.sceneId, who.x, who.y)
		if who.inWar() and not who.inWatchWar():
			teamObj.setLeave(targetObj)
			who.war.addWatch(targetObj, who.warrior.side)
# 			teamObj.addHandlerForWarEnd(targetObj.id, functor(doBack, targetObj.id, True)) # 队伍战斗结束后处理
			targetObj.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
			message.tips(targetObj, "队伍正在战斗中，进入观战")
	
def rpcTeamApplyJoinClear(who, reqMsg):
	'''清空申请列表
	'''
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	if not teamObj.isLeader(who.id):
		message.tips(who, "你不是队长")
		return
	teamObj.clearJoinList()
	
# def rpcTeamLineupSet(who, reqMsg):
# 	'''设置阵法
# 	'''
# 	teamObj = who.getTeamObj()
# 	if not teamObj:
# 		return
# 	if not teamObj.isLeader(who.id):
# # 		message.tips(who, "你不是队长")
# 		return
# 		
# 	teamObj.lineup = reqMsg.lineup
# 	teamObj.attrChange(0, "lineup")

def rpcTeamSetPos(who, reqMsg):
	'''调整站位
	'''
	if not checkLeaderOP(who,True):
		return
	if who.inWar():
		message.tips(who,"战斗后生效")
	
	srcId = reqMsg.srcId
	targetId = reqMsg.targetId
	if srcId == targetId:
		return
	if srcId == who.id or targetId == who.id: # 不能调整队长的站位
		return

	teamObj = who.getTeamObj()
	if (srcId not in teamObj.memberList) or (targetId not in teamObj.memberList): # 不是队员
		return
	
	srcIdx = teamObj.memberList.index(srcId)
	targetIdx = teamObj.memberList.index(targetId)
	teamObj.memberList[srcIdx] = targetId
	teamObj.memberList[targetIdx] = srcId
	rpcTeamInfo(teamObj)
	rpcSSModTeamInfo(teamObj)

def rpcTeamInviteBack(who, reqMsg):
	'''邀请归队
	'''
	targetId = reqMsg.roleId
	if targetId == who.id:
		return
	targetObj = getRole(targetId)
	if not checkInviteBack(who, targetObj):
		return

	teamObj = who.getTeamObj()

	if not hasattr(targetObj, "targetRefuseRecall"):
		targetObj.targetRefuseRecall = False

	if not hasattr(teamObj, "inviteLeaderList"):
		teamObj.inviteLeaderList = {}
	clockbuf = getSecond() - teamObj.inviteLeaderList.get(targetId, 0)
	if clockbuf < 20:
		if targetObj.targetRefuseRecall == False:
			return
		else:
			targetObj.targetRefuseRecall = False
	else:
		teamObj.inviteLeaderList[targetId] = getSecond()

	if targetObj.targetRefuseRecall == True:
		targetObj.targetRefuseRecall = False

	content = '''#C06{}#n将你召回队伍，是否接受？
Q拒绝#20
Q接受'''.format(who.name)

	message.confirmBoxNew(targetObj, functor(responseInviteBack, who.id, targetId), content)

def responseInviteBack(who,yes, roleId, targetId):

	targetObj = getRole(targetId)
	if not targetObj:
		return
	
	targetName = targetObj.name
	if not targetName:
		return

	if not yes:
		message.tips(roleId, "#C01%s#n拒绝了你的召回" % targetName)
		targetObj.targetRefuseRecall = True
		return
	else:
		targetObj.targetRefuseRecall = False

	who = getRole(roleId)
	if not who:
		return

	if not checkInviteBack(who, targetObj):
		return

	if targetObj.inWar():
		targetObj.addHandlerForWarEnd("doBack", functor(doBack, True)) # 玩家战斗结束后处理
		message.tips(targetObj, "战斗结束后自动归队")
		return
	if not scene.validTransfer(targetObj):
		return
	scene.switchScene(targetObj, who.sceneId, who.x, who.y)
	if who.inWar() and not who.inWatchWar():
		who.war.addWatch(targetObj, who.warrior.side)
		return
	
	teamObj = who.getTeamObj()
	teamObj.setBack(targetObj)
	teamObj.teamMessage("$name回归队伍", targetObj.id)
	message.tips(targetObj, "你已回归队伍")

def checkInviteBack(who, targetObj):
	if not checkLeaderOP(who):
		return 0
	teamObj = who.getTeamObj()
	if not targetObj:
		message.tips(who, "对方已下线")
		return 0
	if targetObj.id not in teamObj.leaveList:
		return 0
	return 1
	
def rpcFastChat(who, reqMsg):
	channelId = reqMsg.channelId
	content = reqMsg.content
	teamObj = who.getTeamObj()
	if not teamObj or not teamObj.isLeader(who.id):
		message.tips(who, "你不是队长")
		return
	if teamObj.size >= MEMBER_LIMIT:
		message.tips(who, "本队伍已满员")
		return
	teamTarget = team.platform.getTeamTarget(teamObj.id)
	target,subtarget = teamTarget.get("target"),teamTarget.get("subtarget")
	if not target or not subtarget:
		message.tips(who, "请先调整目标")
		return
	if channelId not in teamTargetData.getConfig(target,"一键喊话频道"):
		return
	if channelId == CHANNEL_GUILD and not who.getGuildId():
		message.tips(who, "你没加入任何仙盟，请加入后再发言")
		return
	if calLenForWord(content) > 24:
		message.tips(who, "超出最大字数，请删减后再发送")
		return
	if getSecond() - getattr(teamObj,"fastChatTime",0) < 10:
		return

	content	= trie.fliter(content)
	msg = {
		"channelId":channelId,
		"content":content,
		"roleId":who.id,
		"fastChat":packFastChat(teamObj,teamTarget),
	}
	mainService.getChatEP().rpcFastChat(**msg)
	teamObj.fastChatTime = getSecond()
	message.tips(who,"一键喊话成功")

#===============================================================================
# 下行协议
#===============================================================================

def packMember(teamObj, pid):
	info = {}
	who = getRole(pid)
	if who:
		info["roleId"] = pid
		info["shape"] = who.shape
		info["name"] = who.name
		info["shapeParts"] = who.shapeParts
		info["colors"] = who.getColors()
		info["level"] = who.level
		info["school"] = who.school
	else:
		info = copy.deepcopy(teamObj.infoList[pid])
	
	info["state"] = teamObj.getState(pid)
	info["pos"] = teamObj.getPos(pid)
	
	obj = team_pb2.member()
	for k,v in info.iteritems():
		if isinstance(v, (list, tuple)):
			attr = getattr(obj, k)
			attr.extend(v)
		else:
			setattr(obj, k, v)
	return obj

def packJoin(teamObj, pid):
	info = teamObj.joinList[pid]
	obj = team_pb2.member()
	for k,v in info.iteritems():
		if isinstance(v, (list, tuple)):
			attr = getattr(obj, k)
			attr.extend(v)
		else:
			setattr(obj, k, v)
	return obj

def packTeam(teamObj):
	memberList = [packMember(teamObj, pid) for pid in teamObj.infoList]
	joinList = [packJoin(teamObj, pid) for pid in teamObj.joinList]
	
	msg = {}
	msg["teamId"] = teamObj.id
	msg["leader"] = teamObj.leader
	
	lineupObj = teamObj.getLineup()
	if lineupObj:
		msg["lineup"] = lineup.service.packetLineupMsg(lineupObj)
	
	msg["memberList"] = memberList
	msg["joinList"] = joinList

	buddyList = teamObj.getBuddyList()
	if buddyList:
		msg["buddyList"] = buddyList

	msg["matchInfo"] = team.platformservice.getTeamMatchInfo(teamObj.id)
	return msg

def packTeam4Hyperlink(teamObj):
	msg = {}
	msg["teamId"] = teamObj.id
	msg["leader"] = teamObj.leader
	msg["memberList"] = [packMember(teamObj, pid) for pid in teamObj.infoList]
	msg["matchInfo"] = team.platformservice.getTeamMatchInfo(teamObj.id)
	return msg

def rpcTeamInfo(teamObj, target=None):
	'''队伍信息
	'''
	msg = packTeam(teamObj)
	targetList = []
	if target:
		targetList.append(target.id)
	else:
		targetList.extend(teamObj.getOnlineList())
		
	for pid in targetList:
		who = getRole(pid)
		if who:
			who.endPoint.rpcTeamInfo(**msg)
	
# def rpcMemberAdd(teamObj, pid):
# 	'''增加队员
# 	'''
# 	obj = packMember(teamObj, pid)
# 
# 	for i in teamObj.getOnlineList():
# 		if i == pid:
# 			continue
# 		who = getRole(i)
# 		if who:
# 			who.endPoint.rpcTeamMemberAdd(obj)
	
# def rpcMemberDel(teamObj, pid):
# 	'''删除队员
# 	'''
# 	msg = {}
# 	msg["roleId"] = pid
# 
# 	for i in teamObj.getOnlineList():
# 		who = getRole(i)
# 		if who:
# 			who.endPoint.rpcTeamMemberDel(**msg)
			
def rpcMemberChange(teamObj, pid, *attrs):
	'''改变队员属性
	'''
	msg = {}
	msg["roleId"] = pid
	
	info = teamObj.infoList[pid]
	for attr in attrs:
		if attr in ("state", "pos"):
			func = getattr(teamObj, "get%s" % toTitle(attr))
			val = func(pid)
		else:
			val = info[attr]
		msg[attr] = val

	for pid in teamObj.getOnlineList():
		who = getRole(pid)
		if who:
			who.endPoint.rpcTeamMemberChange(**msg)
			
def rpcInfoChange(teamObj, *attrNameList):
	'''改变队伍信息
	'''
	msg = {}
	for attrName in attrNameList:
		val = teamObj.getValByName(attrName)
		if val is None:
			continue
		msg[attrName] = val
	
	if not msg:
		return

	for pid in teamObj.getOnlineList():
		who = getRole(pid)
		if who:
			who.endPoint.rpcTeamInfoChange(**msg)
			
def rpcRelease(who):
	'''解散队伍
	'''
	if who:
		who.endPoint.rpcTeamRelease()
			
def rpcJoinAdd(teamObj, pid):
	'''增加入队申请
	'''
	obj = packJoin(teamObj, pid)
	for i in teamObj.getOnlineList():
		who = getRole(i)
		if who:
			who.endPoint.rpcTeamJoinAdd(obj)
			
def rpcJoinDel(teamObj, pid):
	'''删除入队申请
	'''
	msg = {}
	msg["roleId"] = pid

	for i in teamObj.getOnlineList():
		who = getRole(i)
		if who:
			who.endPoint.rpcTeamJoinDel(**msg)
			
def rpcJoinClear(teamObj):
	'''清空申请列表
	'''
	for pid in teamObj.getOnlineList():
		who = getRole(pid)
		if who:
			who.endPoint.rpcTeamApplyJoinClear()
			
def packTeamMakeInfo(teamObj):
	obj = team_pb2.makeInfo()
	obj.teamId = teamObj.id
	obj.leader = teamObj.leader
	obj.memberList.extend(teamObj.getInTeamList())
	obj.size = teamObj.size
	return obj
			
def rpcTeamBroadcastMake(teamObj):
	'''广播创建队伍
	'''
	#通知场景服队伍信息改变
	rpcSSModTeamInfo(teamObj)
	makeInfo = packTeamMakeInfo(teamObj)
	who = getRole(teamObj.leader)
	if who:
		scene.broadcastByAvatar(who, "rpcTeamBroadcastMake", makeInfo)
	
def rpcTeamBroadcastDelMember(teamObj, *memberList):
	'''广播删除队伍
	'''
	who = None
	for pid in memberList:
		who = getRole(pid)
		if who:
			break
	
	if not who:
		return
	
	obj = team_pb2.delMemberInfo()
	obj.teamId = teamObj.id
	obj.memberList.extend(memberList)
	scene.broadcastByAvatar(who, "rpcTeamBroadcastDelMember", obj)
	
def removeJoinFromAllTeam(pid, *excludeList):
	'''从所有队伍中删除申请
	'''
	for teamObj in team.getAllTeam():
		if teamObj.id in excludeList:
			continue
		teamObj.removeJoin(pid)

# =========================================================================================
# 发送到场景服
# =========================================================================================
def rpcSSModTeamInfo(teamObj):
	'''通知场景服创建或者队伍信息改变
	'''
	msg = {}
	msg["teamId"] = teamObj.id
	msg["leader"] = teamObj.leader
	msg["memberList"] = teamObj.memberList
	msg["leaveList"] = teamObj.leaveList
	msg["offlineList"] = teamObj.offlineList
	
	backEnd.gSceneEp4ms.rpcModSSTeamInfo(**msg)

def rpcSSDelTeam(teamObj):
	'''通知场景服删除队伍
	'''
	backEnd.gSceneEp4ms.rpcDelSSTeam(teamObj.id)

# =========================================================================================
# 发送到聊天服
# =========================================================================================
def packFastChat(teamObj,teamTarget):
	msg = main_chat_pb2.fastChatInfo()
	msg.teamId = teamObj.id
	msg.count = teamObj.size
	msg.task = teamTarget["target"]
	msg.target.extend(teamTarget["subtarget"])
	return msg

def rpcModFastChat(teamObj):
	'''修改一键喊话
	'''
	if teamObj.size == MEMBER_LIMIT or teamObj.isReleased():
		rpcDelFastChat(teamObj)
		return

	if not hasattr(teamObj,"fastChatTime"):
		return
	msg = {
		"teamId":teamObj.id,
		"count":teamObj.size,
	}
	mainService.getChatEP().rpcModFastChat(**msg)

def rpcDelFastChat(teamObj):
	'''删除一键喊话
	'''
	if not hasattr(teamObj,"fastChatTime"):
		return
	mainService.getChatEP().rpcDelFastChat(teamObj.id)
	del teamObj.fastChatTime

from common import *
from team.defines import *
from chatService.defines import *
import team
import message
import copy
import lineup.service
import scene
import mainService
import main_chat_pb2
import trie
import teamTargetData
import team.platformservice
import team.platform
import myGreenlet
import task.offlineTask
import backEnd
import activity