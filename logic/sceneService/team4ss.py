#-*-coding:utf-8-*-
import u
import c
import keeper

#场景服队伍对象

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'sceneService' in SYS_ARGV:		
		gTeamKeeper=keeper.cKeeper()#实体实例存放处

		

class SSTeam(object):#实体基类
	def __init__(self, id):
		self.id = id
		self.memberList = []  # 全部队员
		self.leaveList = []  # 暂离队员 
		self.offlineList = []  # 离线队员
		self.leader = 0  # 队长

	def this(self):
		return self

	@property
	def size(self):
		'''全部队员数量
		'''
		return len(self.memberList)

	def isLeader(self, pid):
		return self.leader == pid

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

	def isInTeam(self, pid):
		'''在队伍中
		'''
		if pid in self.leaveList:
			return False
		return pid in self.memberList

	def setTeamInfo(self, reqMsg):
		self.leader = reqMsg.leader
		self.memberList = reqMsg.memberList
		self.leaveList = reqMsg.leaveList
		self.offlineList = reqMsg.offlineList

		for iScriptEttId in self.memberList:
			oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
			if not oEntity:
				continue
			oEntity.setTeamId(self.id)

	def release(self):
		for iScriptEttId in self.memberList:
			oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
			if not oEntity:
				continue
			oEntity.setTeamId(0)

	def packTeamMakeInfo(self):
		obj = team_pb2.makeInfo()
		obj.teamId = self.id
		obj.leader = self.leader
		obj.memberList.extend(self.getInTeamList())
		obj.size = self.size
		return obj

	def getEttList(self, ingoreIdList=None):
		'''获取在队实体列表
		'''
		ettList = []
		for iScriptEttId in self.getInTeamList():
			if ingoreIdList and iScriptEttId in ingoreIdList:#跳过
				continue
			ettObj = sceneService.entity4ss.getEttByScriptId(iScriptEttId)
			if ettObj:
				ettList.append(ettObj)
		return ettList



#生成实体实例
def newSSTeam(teamId):
	teamObj=SSTeam(teamId)
	gTeamKeeper.addObj(teamObj, teamId)
	return teamObj

def getSSTeam(teamId):
	return gTeamKeeper.getObj(teamId)

def getAndCreateSSTeam(teamId):
	teamObj = gTeamKeeper.getObj(teamId)
	if not teamObj:
		teamObj = newSSTeam(teamId)
	return teamObj

#生成实体实例
def delSSTeam(teamId):
	return gTeamKeeper.removeObj(teamId)

#=====================================
def rpcModSSTeamInfo(ctrlr, reqMsg):
	'''改变队伍信息（包含创建）
	'''
	# sceneService.sceneServerLog("service4main", "rpcModSSTeamInfo teamId={}".format(reqMsg.teamId))
	teamObj = getAndCreateSSTeam(reqMsg.teamId)
	teamObj.setTeamInfo(reqMsg)

def rpcDelSSTeam(ctrlr, reqMsg):
	'''删除队伍
	'''
	teamObj = gTeamKeeper.getObj(reqMsg.teamId)
	if not teamObj:
		print "场景服删除队伍错误，对象不存在"
		return
	# sceneService.sceneServerLog("service4main", "rpcDelSSTeam teamId={}".format(reqMsg.teamId))
	teamObj.release()
	delSSTeam(reqMsg.teamId)
	

import timeU
import log
import sceneService.scene4ss
import sceneService.entity4ss
import sceneService
import zfmPyEx
import team_pb2