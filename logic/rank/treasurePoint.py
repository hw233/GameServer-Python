#-*-coding:utf-8-*-
import rank.object
import config

class cRanking(rank.object.cRanking):
	'''探宝积分排行榜
	'''
	if config.IS_INNER_SERVER: #排行榜刷新间隔(秒)
		REFRESH_INTERVAL=5
	else:
		REFRESH_INTERVAL=5

	#探宝积分高到低	
	#按时间前后
	#1，积分降低，后达到目标积分的排前面
	#2，积分增加，先达到目标积分的排前面
	#override
	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1
		
		history1 = self.dIdNameValue[iUid1][4].get("history", 0)
		history2 = self.dIdNameValue[iUid2][4].get("history", 0)
		if history1<history2:
			return 1
		elif history1>history2:
			return -1
		
		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def _checkRankValueComparer(self, iUid):#override
		history1 = self.dIdNameValue[iUid][4].get("history", 0)
		history2 = self.dBuffer[iUid][4].get("history", 0)
		if history1 != history2:
			return False
		return rank.object.cRanking._checkRankValueComparer(self, iUid)

	def getMyRankInfo(self, who):
		'''我的名次信息,参加过本周竞技才显示
		'''
		point = who.week.fetch("treasureP")
		# if not who.day.fetch("treasureP"):
		# 	return []
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(point)
		return tMyInfo


import hyperlink.service
import role.defines