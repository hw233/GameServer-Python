# -*- coding: utf-8 -*-
# 队伍平台服务

def updateTarget(teamObj):
	'''更新组队目标
	'''
	targetArgs = team.platform.getTeamTarget(teamObj.id)
	leaderObj = getRole(teamObj.leader)
	if leaderObj and not checkTeamTarget(leaderObj,targetArgs,False):
		setTeamDefaultTarget(leaderObj,teamObj)
		msg = getTeamMatchInfo(teamObj.id)
		for pid in teamObj.getOnlineList():
			targetObj = getRole(pid)
			if targetObj:
				targetObj.endPoint.rpcTeamChangeTarget(msg)
				message.tips(targetObj,"由于队长等级不足，组队目标已更改")

def checkTeamTarget(who, targetArgs, bTips=True):
	'''检查目标数据是否合法
	'''
	target = targetArgs.get("target", 0)
	#目标
	if target not in teamTargetData.gdData:
		if bTips:
			message.tips(who, "组队目标数据有错，目标不存在")
		return False
	info = teamTargetData.gdData[target]

	#活动等级
	needLv = info.get("活动等级", 0)
	if who.level < needLv:
		if bTips:
			message.tips(who, "组队目标数据有错，等级不足")
		return False
	
	#是否可以多选
	targetType = info.get("目标类型", 0)
	subtarget = targetArgs.get("subtarget", [])
	if targetType == 0:	#单选
		if len(subtarget) > 1:
			if bTips:
				message.tips(who, "组队目标数据有错，只能选一个目标")
			return False
	#检查子目标
	subinfo = info.get("可选目标", {})
	for sub in subtarget:
		if sub and sub not in subinfo:
			if bTips:
				message.tips(who, "组队目标数据有错，可选目标不存在")
			return False

	#活动时间
	timetype = info.get("活动时间类型", 0)
	datePart = getDatePart()
	day = datePart["day"]
	wday = datePart["wday"]	#星期几
	curTime = (datePart["hour"], datePart["minute"])	#(小时，分钟)
	
	if timetype == 1:#每天活动
		startTime = info.get("活动开始时间", (0,0))
		endTime = info.get("活动结束时间", (0,0))
		print curTime,startTime,endTime,curTime < startTime,curTime >= endTime
		if curTime < startTime:
			if bTips:
				message.tips(who, "组队目标数据有错，活动还没开始")
			return False
		if curTime >= endTime:
			if bTips:
				message.tips(who, "组队目标数据有错，活动已结束")
			return False
	elif timetype == 2:#每周活动
		wdayList = info.get("活动开始时间", ())
		if wday not in wdayList:
			if bTips:
				message.tips(who, "组队目标数据有错，活动已结束")
			return False
	elif timetype == 3:#具体日子
		startTime = info.get("活动开始时间", (0,0,0,0,0))
		endTime = info.get("活动结束时间", (0,0,0,0,0))
		if curTime < startTime:
			if bTips:
				message.tips(who, "组队目标数据有错，活动还没开始")
			return False
		if curTime >= endTime:
			if bTips:
				message.tips(who, "组队目标数据有错，活动已结束")
			return False
	elif timetype == 4:#隔星期活动
		weekNo = getWeekNo()
		week = info.get("活动开始时间", 0)
		if week == 1:	#单周
			if weekNo%2 == 0:
				if bTips:
					message.tips(who, "组队目标数据有错，目标不是单周活动")
				return False
		else:			#双周
			if weekNo%2 == 1:
				if bTips:
					message.tips(who, "组队目标数据有错，目标不是双周活动")
				return False
	elif timetype == 5:#每月活动
		if day != info.get("活动开始时间", 0):
			if bTips:
				message.tips(who, "组队目标数据有错，活动暂不开放")
			return False
	else:
		pass
	return True


def targetEqual(t1, t2):
	'''判断目标是否相同
	'''
	if t1.get("target", 0) != t2.get("target", 0):
		return False
	if t1.get("subtarget", 0) != t2.get("subtarget", 0):
		return False
	return True

def rpcTeamSetTarget(who, reqMsg):
	'''设置匹配目标
	'''
	targetArgs = {
		"target":reqMsg.target,
		"subtarget":[x for x in reqMsg.subtarget],
	}
	if not checkTeamTarget(who, targetArgs):
		return
	
	teamObj = who.getTeamObj()
	if not teamObj:
		oldTarget = team.platform.gTeamPlatformObj.getPlayerTarget(who)
		if targetEqual(oldTarget, targetArgs):	#目标一样不用重新改
			return
		auto = team.platform.gTeamPlatformObj.getPlayerAuto(who)
		team.platform.addPlayerMatch(who, targetArgs)
		if auto:	#自动匹配中更换目标
			playerSetAutoMatch(who, auto)
	else:
		if not teamObj.isLeader(who.id):
			message.tips(who, "你不是队长,不能进行匹配操作")
			return
		oldTarget = team.platform.gTeamPlatformObj.getTeamTarget(teamObj.id)
		if targetEqual(oldTarget, targetArgs):	#目标一样不用重新改
			return
		auto = team.platform.gTeamPlatformObj.getTeamAuto(teamObj.id)
		team.platform.addTeamMatch(teamObj.id, targetArgs)
		team.service.rpcDelFastChat(teamObj)
		rpcChangeTeamTarget(who, teamObj)
		if auto:	#自动匹配中更换目标
			teamSetAutoMatch(who, teamObj, auto)

def rpcTeamAutoMatch(who, reqMsg):
	teamObj = who.getTeamObj()
	auto = reqMsg.iValue
	if teamObj:
		if auto and team.checkTeamDennyAdd(who, teamObj, "自动匹配"):
			who.endPoint.rpcTeamAutoMatchRes(0)
			return
		who.endPoint.rpcTeamAutoMatchRes(auto)
		teamSetAutoMatch(who, teamObj, auto)
	else:
		if auto and team.checkDennyTeam(who, None, "自动匹配"):
			who.endPoint.rpcTeamAutoMatchRes(0)
			return
		who.endPoint.rpcTeamAutoMatchRes(auto)
		playerSetAutoMatch(who, auto)

def teamSetAutoMatch(who, teamObj, auto):
	if not teamObj.isLeader(who.id):
		message.tips(who, "你不是队长")
		return
	team.platform.setTeamAutoMatch(teamObj.id, auto)
	if not auto:#自动匹配
		return
	teamAutoMatch(who, teamObj)

def teamAutoMatch(who, teamObj):
	'''who是队长
	'''
	matchList = team.platform.getAutoMatchPlayer(who, teamObj)
	random.shuffle(matchList)
	# print "teamSetAutoMatch matchTeam=",who.id,matchList,team.platform.gTeamPlatformObj.getTeamTarget(teamObj.id)
	for pid in matchList:
		if teamObj.size >= MEMBER_LIMIT:
			break
		targetObj = getRole(pid)
		if not targetObj:
			continue
		if targetObj.getTeamObj():
			continue
		if getattr(targetObj, "denyTeam", {}):
			continue
		if targetObj.id in teamObj.memberList:
			continue
		# if getattr(targetObj, "enterCollect", 0):#玩家在收集玩法内
		# 	continue
		team.service.removeJoinFromAllTeam(targetObj.id)
		teamObj.add(targetObj)
		team.platform.gTeamPlatformObj.transPlayerTarget(targetObj)
		#team.platform.removePlayerMatch(targetObj)
		if targetObj.inWar():
			teamObj.setLeave(targetObj)
			targetObj.addHandlerForWarEnd("doBack", functor(team.service.doBack, True)) # 玩家战斗结束后处理
			message.tips(targetObj, "正在战斗中，自动暂离")
		else:
			if not scene.validTransfer(targetObj):
				teamObj.setLeave(targetObj)
				return
			scene.switchScene(targetObj, who.sceneId, who.x, who.y)
			if who.inWar():
				teamObj.setLeave(targetObj)
				who.war.addWatch(targetObj, who.warrior.side)
# 				teamObj.addHandlerForWarEnd(targetObj.id, functor(team.service.doBack, targetObj.id, True)) # 队伍战斗结束后处理
				targetObj.addHandlerForWarEnd("doBack", functor(team.service.doBack, True)) # 玩家战斗结束后处理
				message.tips(targetObj, "队伍正在战斗中，进入观战")


def teamMemberChange(teamObj):
	'''队伍有人退出或踢人后，重新匹配加人
	'''
	leaderObj = getRole(teamObj.leader)#队伍队长
	if not leaderObj:
		return
	targetArgs = team.platform.gTeamPlatformObj.getTeamTarget(teamObj.id)
	if not targetArgs.get("automatch", 0):
		return

	teamAutoMatch(leaderObj, teamObj)

def playerSetAutoMatch(who, auto, *excludeList):
	team.platform.setPlayerAutoMatch(who, auto)
	if not auto:#自动匹配
		return
	teamObj = None
	matchTeamId = team.platform.getAutoMatchTeam(who, *excludeList)
	# print "playerSetAutoMatch matchTeam=",who.id,matchTeamId
	random.shuffle(matchTeamId)
	for teamId in matchTeamId:
		if teamId in excludeList:
			continue
		teamObj = team.getTeam(teamId)
		if not teamObj:
			continue
		if teamObj.size >= MEMBER_LIMIT:
			continue
		# if who.id in teamObj.joinList:
		# 	continue
		if who.id in teamObj.memberList:
			continue
		# if len(teamObj.joinList) >= JOIN_LIMIT:
		# 	continue
		if team.checkTeamDennyAdd(who, teamObj, "自动匹配", False):
			return
		team.service.removeJoinFromAllTeam(who.id)
		teamObj.add(who)
		# team.platform.removePlayerMatch(who)
		team.platform.gTeamPlatformObj.transPlayerTarget(who)
		if who.inWar():
			teamObj.setLeave(who)
			who.addHandlerForWarEnd("doBack", functor(team.service.doBack, True)) # 玩家战斗结束后处理
			message.tips(who, "正在战斗中，自动暂离")
		else:
			leaderObj = getRole(teamObj.leader)#队伍队长
			if leaderObj:
				if not scene.validTransfer(who):
					teamObj.setLeave(who)
					return
				scene.switchScene(who, leaderObj.sceneId, leaderObj.x, leaderObj.y)
				if leaderObj.inWar():
					teamObj.setLeave(who)
					leaderObj.war.addWatch(who, leaderObj.warrior.side)
# 					teamObj.addHandlerForWarEnd(who.id, functor(team.service.doBack, who.id, True)) # 队伍战斗结束后处理
					who.addHandlerForWarEnd("doBack", functor(team.service.doBack, True)) # 玩家战斗结束后处理
					message.tips(who, "队伍正在战斗中，进入观战")
		break

def rpcTeamRefreshMatch(who, reqMsg):
	'''刷新匹配界面
	'''
	teamObj = who.getTeamObj()
	if teamObj:
		refreshMatchPlayer(who, reqMsg, teamObj)
	else:
		refreshMatchTeam(who, reqMsg)

def packMatchPlayer(obj, teamObj):
	msg = team_pb2.matchPlayer()
	msg.roleId = obj.id
	msg.shape = obj.shape
	msg.name = obj.name
	msg.level = obj.level
	msg.school = obj.school

	inviteList = getattr(teamObj, "inviteList", {})
	if getSecond() - inviteList.get(obj.id, 0) < 20:
		msg.invite = 1
	else:
		msg.invite = 0
	return msg

def refreshMatchPlayer(who, reqMsg, teamObj):
	'''匹配的玩家
	'''
	if not teamObj.isLeader(who.id):
		message.tips(who, "你不是队长")
		return

	matchList = team.platform.getAutoMatchPlayer(who, teamObj)
	playerList = []
	for pid in matchList:
		if pid == who.id:
			continue
		targetObj = getRole(pid)
		if not targetObj:
			continue
		if targetObj.getTeamObj():
			continue
		if pid in teamObj.memberList:
			continue
		playerList.append(packMatchPlayer(targetObj, teamObj))
	msg = {}
	msg["playerList"] = playerList
	msg["teamCnt"] = team.platform.gTeamPlatformObj.getMatchTeamCnt(teamObj.id)
	msg["playerCnt"] = len(playerList)
	# print "refreshMatchPlayer = ",msg
	who.endPoint.rpcTeamMatchPlayer(**msg)

def packMatchTeam(who, teamObj):
	memberList = [team.service.packMember(teamObj, pid) for pid in teamObj.infoList]
	msg = team_pb2.matchTeam()
	msg.teamId = teamObj.id
	msg.leader = teamObj.leader
	msg.memberList.extend(memberList)
	if who.id in teamObj.joinList:
		msg.apply = 1
	else:
		msg.apply = 0
	return msg

def refreshMatchTeam(who, reqMsg):
	'''匹配的队伍
	'''
	matchTeam = team.platform.getMatchTeam(who)
	# print "refreshMatchTeam matchTeam=",who.id,matchTeam,team.platform.gTeamPlatformObj.getPlayerTarget(who)
	teamList = []
	for id in matchTeam:
		teamObj = team.getTeam(id)
		if not teamObj:
			continue
		if teamObj.size >= MEMBER_LIMIT:
			continue
		teamList.append(packMatchTeam(who, teamObj))

	msg = {}
	msg["teamList"] = teamList
	msg["teamCnt"] = len(teamList)
	msg["playerCnt"] = team.platform.gTeamPlatformObj.getMatchPlayerCnt(who)
	# print "refreshMatchTeam = ",msg
	who.endPoint.rpcTeamMatchTeam(**msg)

def getTeamMatchInfo(teamId):
	targetArgs = team.platform.getTeamTarget(teamId)
	msg = team_pb2.teamMatchInfo()
	msg.target = targetArgs.get("target", 0)
	msg.subtarget.extend(targetArgs.get("subtarget", []))
	return msg


def rpcChangeTeamTarget(who, teamObj):
	'''队伍目标改变，告诉其它客户端
	'''
	msg = getTeamMatchInfo(teamObj.id)
	for pid in teamObj.getOnlineList():
		targetObj = getRole(pid)
		if targetObj:
			targetObj.endPoint.rpcTeamChangeTarget(msg)

def setTeamDefaultTarget(who, teamObj):
	'''设置队伍默认目标
	'''
	target = 0
	subtarget = 0
	for i,info in teamTargetData.gdData.iteritems():
		#等级
		if info.get("活动等级", 0) > who.level:
			continue
		#活动时间
		timetype = info.get("活动时间类型", 0)
		if timetype:
			datePart = getDatePart()
			year = datePart["year"]
			month = datePart["month"]
			day = datePart["day"]
			hour = datePart["hour"]
			minute = datePart["minute"]
			wday = datePart["wday"]

			if timetype == 1:#每天活动
				startTime = info.get("活动开始时间", (0,0))
				endTime = info.get("活动结束时间", (0,0))
				curTime = (hour, minute)	#(小时，分钟)
				if curTime < startTime:
					continue
				if curTime >= endTime:
					continue
			elif timetype == 2:#每周活动
				wdayList = info.get("活动结束时间", ())
				if wday not in wdayList:
					continue
			elif timetype == 3:#具体日子
				startTime = info.get("活动开始时间", (0,0,0,0,0))
				endTime = info.get("活动结束时间", (0,0,0,0,0))
				curTime = (year, month, day, hour, minute)	#(年,月,日,时,分)
				if curTime < startTime:
					continue
				if curTime >= endTime:
					continue
			elif timetype == 4:#隔星期活动
				weekNo = getWeekNo()
				week = info.get("活动开始时间", 0)
				if week == 1:	#单周
					if weekNo%2 == 0:
						continue
				else:			#双周
					if weekNo%2 == 1:
						continue
			elif timetype == 5:#每月活动
				if day != info.get("活动开始时间", 0):
					continue

		for sub,_info in info.get("可选目标", {}).iteritems():
			lvRange = _info.get("默认选择范围", (0, 0))
			if lvRange[0] <= who.level <= lvRange[1]:
				target = i
				subtarget = sub
				break
		if target and subtarget:
			break
	
	if not target or not subtarget:	#没有找到合适的目标，拿第一个
		for i,info in teamTargetData.gdData.iteritems():
			target = i
			for sub,_info in info.get("可选目标", {}).iteritems():
				subtarget = sub
				break
			break
	targetArgs = {
		"target":target,
		"subtarget":[subtarget],
	}
	team.platform.addTeamMatch(teamObj.id, targetArgs)


def quickMakeTeam(who, target, auto=1):
	'''便捷组队
	'''
	subtarget = []
	for sub ,_ in teamTargetData.gdData[target].get("可选目标", {}).iteritems():
		subtarget.append(sub)
	targetArgs = {
		"target":target,
		"subtarget":subtarget,
		# "automatch":auto,
	}

	teamObj = who.getTeamObj()
	if teamObj:
		if not teamObj.isLeader(who.id):
			message.tips(who, "你不是队长")
			return
		team.platform.addTeamMatch(teamObj.id, targetArgs)
		team.service.rpcDelFastChat(teamObj)
		rpcChangeTeamTarget(who, teamObj)
		who.endPoint.rpcTeamQuick(**targetArgs)
		teamSetAutoMatch(who, teamObj, auto)
	else:
		team.platform.addPlayerMatch(who, targetArgs)
		who.endPoint.rpcTeamQuick(**targetArgs)
		playerSetAutoMatch(who, auto)


def teamKickDuel(pid, teamId, auto=True):
	'''被队长踢出，则自动匹配状态不变，会继续加入其他队伍
		自己退出队伍不自动匹配
	'''
	who = getRole(pid)
	if not who:
		return
	targetArgs = team.platform.gTeamPlatformObj.getPlayerTargetTemp(who)
	if not targetArgs:
		return

	if not auto:
		targetArgs["automatch"] = 0
	team.platform.gTeamPlatformObj.addPlayerMatch(who, targetArgs)
	#自动匹配一次
	playerSetAutoMatch(who, targetArgs.get("automatch", 0), teamId)


def offlineMatch(who):
	'''离线挂机
	'''
	subtarget = []
	for sub, _ in teamTargetData.gdData[team.platform.DEMON_TASK_NPC].get("可选目标", {}).iteritems():
		subtarget.append(sub)
	targetArgs = {
		"target": team.platform.DEMON_TASK_NPC,
		"subtarget": subtarget,
	}
	team.platform.addPlayerMatch(who,targetArgs)
	playerSetAutoMatch(who,True)

def cancleOfflineMatch(who):
	'''取消离线挂机
	'''
	team.platform.removePlayerMatch(who)

def playerAutoMatch(who):
	'''退出收集玩法时匹配一次
	'''
	targetArgs = team.platform.getPlayerTarget(who)
	if targetArgs.get('automatch', 0):
		playerSetAutoMatch(who, 1)


def cancelAutoMatch(who):
	'''服务端主动取消匹配
	'''
	teamObj = who.getTeamObj()
	if teamObj:
		if not teamObj.isLeader(who.id):
			return
		targetArgs = team.platform.getTeamTarget(teamId)
		if targetArgs and targetArgs.get("automatch") == 1:
			team.platform.setTeamAutoMatch(teamObj.id, 0)
			targetArgs["automatch"] = 0
			team.platform.addTeamMatch(teamObj.id, targetArgs)
			team.service.rpcDelFastChat(teamObj)
			rpcChangeTeamTarget(who, teamObj)
	else:
		targetArgs = team.platform.getPlayerTarget(who)
		if targetArgs and targetArgs.get("automatch") == 1:
			team.platform.setPlayerAutoMatch(who, 0)
			who.endPoint.rpcTeamAutoMatchRes(0)


from common import *
import message
from team.defines import *
import team_pb2
import teamTargetData
import team
import team.service
import team.platform
import scene
import random
