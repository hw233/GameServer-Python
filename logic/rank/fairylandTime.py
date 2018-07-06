#-*-coding:utf-8-*-
import rank.object
import config

class cRanking(rank.object.cRanking):
	'''试炼幻境排行榜
	'''

	def title4(self, iUid):#override
		iStage = self.dIdNameValue[iUid][1]
		if iStage == 25:
			return "%d秒" % self.dIdNameValue[iUid][4].get("time", 0)

		return "第%d关" % iStage

	#override
	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1
		
		time1 = self.dIdNameValue[iUid1][4].get("time", 0)
		time2 = self.dIdNameValue[iUid2][4].get("time", 0)
		if time1<time2:
			return -1
		elif time1>time2:
			return 1
		
		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def getMyTitle4(self, who):
		iStage,iTime = who.week.fetch("flFast",(0,0))
		if iStage == 25:
			return "%d秒" % iTime
			
		return "第%d关" % iStage

	def getMyRankInfo(self, who):
		title4 = self.getMyTitle4(who)
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(title4)
		return tMyInfo

import hyperlink.service
import role.defines