#-*-coding:utf-8-*-
import rank.object
import config

class cRanking(rank.object.cRanking):
	'''组队竞技积分排行榜
	'''
	def __init__(self,iMainNo,iRankNo,sChineseName,sName,iDisplaySize):#override
		rank.object.cRanking.__init__(self,iMainNo,iRankNo,sChineseName,sName,iDisplaySize)
		timerEvent.geNewWeek += self.onNewWeek

	def onNewWeek(self, year, month, day, hour, wday):
		self.checkTeamRacePointChange()

	# def load(self,dData):#override
	# 	rank.object.cRanking.load(self,dData)
	# 	self.checkTeamRacePointChange()

	#按照个人的最近4周（包含本周）的竞技积分总和排行
	#若计算出来最近四周竞技积分总和相同，则以综合实力进行排行，之后仍相同则以角色ID前后进行排行
	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1
			
		dRoleArgs1 = self.getRoleArgs(iUid1)
		dRoleArgs2 = self.getRoleArgs(iUid2)

		#综合实力
		iScore1 = dRoleArgs1.get("score", getSecond())
		iScore2 = dRoleArgs2.get("score", getSecond())
		if iScore1<iScore2:
			return -1
		elif iScore1>iScore2:
			return 1

		#角色ID
		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def _checkRankValueComparer(self, iUid):#override
		dRoleArgs = self.getRoleArgs(iUid)

		iScore1 = dRoleArgs.get("score", getSecond())
		iScore2 = self.dBuffer[iUid][4].get("score", getSecond())
		if iScore1 != iScore2:
			return False

		return rank.object.cRanking._checkRankValueComparer(self, iUid)

	def checkTeamRacePointChange(self):
		'''刷周或者初始化时检查积分是否有变化
		'''
		actObj = activity.getActivity("teamRace")
		if not actObj:
			return

		bMarkDirty = False
		for iUid,lInfo in self.dIdNameValue.iteritems():
			sName,iValue,iLv,iSchool,dArgs = lInfo
			dTeamRacePoint = dArgs.get("teamRacePoint", {})
			bChange = actObj.checkTeamRacePoint(dTeamRacePoint)
			if bChange:
				bMarkDirty = True
				#有变化
				iTeamRacePoint = actObj.calcAttrTeamRacePoint(dTeamRacePoint)
				self.updateScore(iUid, sName, iTeamRacePoint, iLv, iSchool, **dArgs)
		if bMarkDirty:
			self.markDirty()


	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(who.getTeamRacePoint())
		return tMyInfo


from common import *
import timerEvent
import activity
import role.defines