#-*-coding:utf-8-*-
import rank.object
import config

class cRanking(rank.object.cRanking):
	'''组队竞技积分排行榜,只在活动期间看到的
	'''
	#排行榜按照玩家积分排行，全队会默认排在一起，比如队伍积分第三名，则所有成员都排名第三，并按照队伍中的排序排在一起，队长第一
	#若多个队伍积分一样，则按照获得这个积分的时间排序，若时间一样，则按照队伍整体实力排序
	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1
			
		dRoleArgs1 = self.getRoleArgs(iUid1)
		dRoleArgs2 = self.getRoleArgs(iUid2)

		#积分获得时间
		gainTime1 = dRoleArgs1.get("gainTime", getSecond())
		gainTime2 = dRoleArgs2.get("gainTime", getSecond())
		if gainTime1<gainTime2:
			return -1
		elif gainTime1>gainTime2:
			return 1

		#队伍整体实力
		teamTotalScore1 = dRoleArgs1.get("teamTotalScore", 0)
		teamTotalScore2 = dRoleArgs2.get("teamTotalScore", 0)
		if teamTotalScore1<teamTotalScore2:
			return 1
		elif teamTotalScore1>teamTotalScore2:
			return -1

		teamId1 = dRoleArgs1.get("teamId", 1)
		teamId2 = dRoleArgs2.get("teamId", 2)
		if teamId1 == teamId2:	#同个队伍按照队伍中的排序排在一起，队长第一
			pos1 = dRoleArgs1.get("teamId", 0)
			pos2 = dRoleArgs2.get("teamId", 0)
			if pos1 == pos2:
				return 0
			elif pos1<pos2:
				return -1
			elif pos1>pos2:
				return 1

		return 1 if teamId1>teamId2 else -1

	def _checkRankValueComparer(self, iUid):#override
		dRoleArgs = self.getRoleArgs(iUid)

		gainTime1 = dRoleArgs.get("gainTime", getSecond())
		gainTime2 = self.dBuffer[iUid][4].get("gainTime", getSecond())
		if gainTime1 != gainTime2:
			return False

		teamTotalScore1 = dRoleArgs.get("teamTotalScore", 0)
		teamTotalScore2 = self.dBuffer[iUid][4].get("teamTotalScore", 0)
		if teamTotalScore1 != teamTotalScore2:
			return False

		return rank.object.cRanking._checkRankValueComparer(self, iUid)


	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(who.day.fetch("teamRaceActPoint", 0))
		return tMyInfo


from common import *
import role.defines