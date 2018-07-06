# -*- coding: utf-8 -*-

if "gTeamLastId" not in globals():
	gTeamLastId = 0
	
def _newTeamId():
	'''新队伍id
	'''
	global gTeamLastId
	gTeamLastId += 1
	return gTeamLastId

class Team(object):
	
	def __init__(self):
		self.id = _newTeamId()
		self.memberList = []  # 全部队员
		self.leaveList = []  # 暂离队员 
		self.offlineList = []  # 离线队员
		self.infoList = {}  # 队员信息
		self.joinList = {}  # 加入申请列表
		self.leader = 0  # 队长
		self.taskCtn = block.blockTeamTask.TeamTaskContainer(self.id)
		self.handlerListForWarEnd = {} # 战斗后处理的操作
		
	def this(self):
		return self
		
	@property
	def size(self):
		'''全部队员数量
		'''
		return len(self.memberList)
	
	@property
	def inTeamSize(self):
		'''在线队员数量
		'''
		return len(self.getInTeamList())
		
	def setLeader(self, who):
		'''设置队长
		'''
		pid = who.id
		if pid in self.memberList:
			self.memberList.remove(pid)
		elif pid in self.leaveList:
			self.leaveList.remove(pid)
		self.memberList.insert(0, pid)  # 队长放在首位
		oldLeaderId = self.leader
		self.leader = pid
		who.setTeamObj(self)
		self.updateInfo(who)
		who.attrChange("addon")
		
		if oldLeaderId:
			oldLeader = getRole(oldLeaderId)
			if oldLeader:
				oldLeader.attrChange("addon")

		team.service.rpcDelFastChat(self)
		
		if task.offlineTask.inOfflineTask(who):
			task.offlineTask.autoMatchTaskTeam(who)

		
	def autoSetNewLeader(self):
		'''自动设置新队长
		'''
		leaderObj = None
		inTeamList = self.getInTeamList()
		if len(inTeamList): # 从在队队员中选
			leaderObj = getRole(inTeamList[0])
		elif len(self.leaveList) > 1: # 从离队队员中选
			leaderObj = getRole(self.leaveList[0])
			self.setBack(leaderObj)

		if leaderObj:
			self.setLeader(leaderObj)
			message.tips(leaderObj, "你已成为新队长！")
			
		return leaderObj
		
	def add(self, who):
		'''增加队员
		'''
		self.memberList.append(who.id)
		self.updateInfo(who)
		who.setTeamObj(self)
		team.service.rpcTeamInfo(self)
		team.service.rpcTeamBroadcastMake(self)
		self.teamMessage("$name加入队伍", who.id)
		self.tips("$name加入队伍", who.id, who.id)
		message.tips(who, self.transString("成功加入$name的队伍", self.leader))
		
		for taskObj in self.taskCtn.getAllValues():
			taskObj.onReEnter(who, ENTER_TASK_ADD)

		team.service.rpcModFastChat(self)
		friend.addTeamMate(self,who)
		
	def updateInfo(self, who):
		pid = who.id
		info = {}
		info["roleId"] = pid
		info["shape"] = who.shape
		info["shapeParts"] = who.shapeParts
		info["colors"] = who.getColors()
		info["name"] = who.name
		info["level"] = who.level
		info["school"] = who.school
		self.infoList[pid] = info
			
	def remove(self, pid):
		'''移除队员
		'''
		info = self.infoList.pop(pid)
		self.memberList.remove(pid)
		if pid in self.leaveList:
			self.leaveList.remove(pid)
		elif pid in self.offlineList:
			self.offlineList.remove(pid)
		confirmList= getattr(self, "confirmList",{})
		if confirmList.get(pid,False):
			del self.confirmList[pid]
		who = getRole(pid)
		if who:
			who.setTeamObj(None)
			team.service.rpcRelease(who)
			team.service.rpcTeamBroadcastDelMember(self, pid)
		msg = "#C01%s#n离开队伍" % info["name"]
		self.teamMessage(msg)
		self.tips(msg)
		for taskObj in self.taskCtn.getAllValues():
			taskObj.onLeave(pid, LEAVE_TASK_REMOVE)
		
		if pid == self.leader:  # 如果是队长退出，需要换个队长
			leader = self.autoSetNewLeader()
			if not leader: # 换不到新队长，解散队伍
				self.release()
				team.service.rpcDelFastChat(self)
				return
			
		team.service.rpcModFastChat(self)
		team.service.rpcTeamInfo(self)
		team.service.rpcTeamBroadcastMake(self)
			
	def setLeave(self, who):
		'''设置暂离
		'''
		pid = who.id
		if pid in self.leaveList: # 已暂离
			print "[setLeave] already setLeave"
			return
		if len(self.getOnlineList()) == 1: # 只有一个在线队员，不能暂离
			return

		self.leaveList.append(pid)
		team.service.rpcTeamBroadcastDelMember(self, pid)
		self.teamMessage("$name暂离队伍", pid)
		
		if self.leader == pid: # 如果是队长暂离，需要换个队长
			self.autoSetNewLeader()
				
		team.service.rpcTeamInfo(self)
		team.service.rpcTeamBroadcastMake(self)
		who.broadcastAttrChange("teamState")
		
		for taskObj in self.taskCtn.getAllValues():
			taskObj.onLeave(who.id, LEAVE_TASK_LEAVE)
		
	def setBack(self, who):
		'''回归队伍
		'''
		pid = who.id
		if pid not in self.leaveList: # 已回归
			print "[setBack] already setBack"
			return
			
		self.leaveList.remove(pid)
		team.service.rpcTeamInfo(self)
		team.service.rpcTeamBroadcastMake(self)
		who.broadcastAttrChange("teamState")
		
		for taskObj in self.taskCtn.getAllValues():
			taskObj.onReEnter(who, ENTER_TASK_BACK)
			
	def setOffline(self, who):
		'''离线
		'''
		pid = who.id
		if pid in self.offlineList: # 已离线
			print "[setOffline] already setOffline"
			return
		
		if pid not in self.leaveList:  # 在队状态
			if len(self.getOnlineList()) == 1: # 只有一个在线队员，解散队伍
				self.remove(pid)
				return
			self.setLeave(who)

		self.leaveList.remove(pid)
		self.offlineList.append(pid)

		self.updateInfo(who)
		team.service.rpcTeamInfo(self)
		who.broadcastAttrChange("teamState")
		
		for taskObj in self.taskCtn.getAllValues():
			taskObj.onLeave(who.id, LEAVE_TASK_OFFLINE)
		
	def setOnline(self, who):
		'''上线
		'''
		pid = who.id
		if pid not in self.offlineList: # 已上线
			print "[setOnline] already setOnline"
			return
				
		self.offlineList.remove(pid)
		self.leaveList.append(pid)
		who.setTeamObj(self)
		team.service.rpcTeamInfo(self)
		
	def release(self):
		'''解散队伍
		'''
		self.released = True
		
		self.taskCtn.clearAll()

		for pid in self.memberList:
			who = getRole(pid)
			if who:
				who.setTeamObj(None)
				team.service.rpcRelease(who)
				
		leaderObj = getRole(self.leader)
		if leaderObj:
			leaderObj.attrChange("addon")

		inTeamList = self.getInTeamList()
		if inTeamList:
			team.service.rpcTeamBroadcastDelMember(self, *self.getInTeamList())

		self.tips("队伍解散了")
		team.service.rpcSSDelTeam(self)
		
			
	def isReleased(self):
		return getattr(self, "released", False) == True
		
	def addJoin(self, who):
		'''申请加入队伍
		'''
		pid = who.id
		info = {}
		info["roleId"] = pid
		info["shape"] = who.shape
		info["shapeParts"] = who.shapeParts
		info["colors"] = who.getColors()
		info["name"] = who.name
		info["level"] = who.level
		info["school"] = who.school
		self.joinList[pid] = info
		team.service.rpcJoinAdd(self, pid)
		
	def clearJoinList(self):
		'''清空申请列表
		'''
		self.joinList = {}
		team.service.rpcJoinClear(self)
		
	def removeJoin(self, pid):
		'''删除入队申请
		'''
		info = self.joinList.pop(pid, None)
		if info:
			team.service.rpcJoinDel(self, pid)
		return info
		
	def getState(self, pid):
		'''队员状态
		'''
		if pid in self.leaveList:
			return TEAM_STATE_LEAVE
		if pid in self.offlineList:
			return TEAM_STATE_OFFLINE
		if pid in self.memberList:
			return TEAM_STATE_NORMAL
		return TEAM_STATE_NONE
	
	def getPos(self, pid):
		return self.memberList.index(pid) + 1
	
	def isLeader(self, pid):
		return self.leader == pid
	
	def getMemberList(self):
		'''全部队员列表
		'''
		for roleId in self.memberList:
			yield roleId
	
	def getOnlineList(self):
		'''在线队员，包括暂离
		'''
		lst = []
		for pid in self.memberList:
			if pid in self.offlineList:
				continue
			lst.append(pid)
		return lst
	
	def getInTeamList(self):
		'''在队队员
		'''
		lst = []
		for pid in self.memberList:
			if pid in self.leaveList:
				continue
			if pid in self.offlineList:
				continue
			lst.append(pid)
		return lst
	
	def attrChange(self, pid, *attrs):
		'''改变队员或队伍信息
		'''
		if pid: # 队员信息
			who = getRole(pid)
			if who:
				self.updateInfo(who)
			team.service.rpcMemberChange(self, pid, *attrs)
		else: # 队伍信息
			team.service.rpcInfoChange(self, *attrs)
			
	def getValByName(self, attrName):
		if attrName == "lineup":
			lineupObj = self.getLineup()
			if lineupObj:
				return lineup.service.packetLineupMsg(lineupObj)
			return None
	
		return getValByName(self, attrName)
		
	def teamMessage(self, content, pid=0):
		'''队伍频道系统提示
		
		pid: 引用指定队员数据
		'''
		content = self.transString(content, pid)
		message.teamMessage(self.id, content)
		
	def tips(self, msg, pid=0, *excludeList):
		'''提示
		
		pid: 引用指定队员数据
		excludeList: 排除列表
		'''
		msg = self.transString(msg, pid)
		for pid in self.getOnlineList():
			if pid in excludeList:
				continue
			message.tips(pid, msg)
		
	def transString(self, content, pid=0):
		if pid:
			info = self.infoList[pid]
			content = content.replace("$name", "#C01%s#n" % info["name"])
		return content
	
	def getLineup(self):
		who = getRole(self.leader)
		return who.buddyCtn.getCurrentLineup()
			
	def addTask(self, taskObj):
		'''增加任务
		'''
		taskObj.setRoleList(self.getInTeamList())
		self.taskCtn.addItem(taskObj)
		
		# 刷新可接任务
		import activity.center
		for roleId in self.getInTeamList():
			roleObj = getRole(roleId)
			if roleObj:
				activity.center.refreshTaskNpc(roleObj)
			
	def removeTask(self, taskObj):
		'''移除任务
		'''
		self.taskCtn.removeItem(taskObj)

		# 刷新可接任务
		import activity.center
		for roleId in self.getInTeamList():
			roleObj = getRole(roleId)
			if roleObj:
				activity.center.refreshTaskNpc(roleObj)
	
	def reEnter(self, who):
		team.service.rpcTeamInfo(self, who)
		if who.id in self.getInTeamList():
			self.taskCtn.rpcRefresh(who)

	def getAvgLV(self):
		'''平均等级
		'''
		lvList = []
		for pid in self.getInTeamList():
			who = getRole(pid)
			if who:
				lvList.append(who.level)
		return sum(lvList) / len(lvList)
	
	def getMaxLV(self):
		'''最大等级
		'''
		lvList = []
		for pid in self.getInTeamList():
			who = getRole(pid)
			if who:
				lvList.append(who.level)
		return max(lvList)

	def getBuddyList(self):
		'''伙伴信息
		'''
		who = getRole(self.leader)
		return who.buddyCtn.getTeamBuddyListMsg(who)
	
	def updateBuddyList(self):
		'''更新助战伙伴
		'''
		self.attrChange(None,"buddyList")
	
	def updateLineup(self):
		self.attrChange(None, "lineup")
		
	def leaveWar(self):
		'''离开战斗
		'''
		self.executeHandlerForWarEnd()
		
	def addHandlerForWarEnd(self, pid, handler):
		'''增加战后处理
		'''
		self.handlerListForWarEnd[pid] = handler
		
	def executeHandlerForWarEnd(self):
		'''执行战后处理
		'''
		funcList = self.handlerListForWarEnd.values()
		self.handlerListForWarEnd = {}
		for func in funcList:
			func()
	

from common import *
from team.defines import *
import team.service
import message
import block.blockTeamTask
import lineup.service
import team.platformservice
import task
import friend