#-*-coding:utf-8-*-
import rank.object


class cRanking(rank.object.cRanking):
	'''角色战斗力排行榜
	'''
	def title3(self, iUid):#override
		'''装备名称
		'''
		if self.sName == "rank_school_all":
			return rank.object.cRanking.title3(self, iUid)
		#所在帮派
		return self.getGuildName(iUid)
		

	def addRank(self, who):#override
		iCompositeScore = rank.rankCompositeScore(who)
		self.updateScore(who.id, who.name, iCompositeScore, who.level, who.school)

	def lookInfo(self, who, other, iUid):#override
		rank.service.rpcLookOtherRoleScore(who, other)

	def getMyRankInfo(self, who):#override
		'''我的名次信息
		'''
		#同门派才显示
		iSchool = rank.load.gdRankModInfo.get(self.iRankNo, {}).get("school", 0)
		if iSchool and who.school != iSchool:
			return []
		if self.sName == "rank_school_all":
			return rank.object.cRanking.getMyRankInfo(self, who)
		else:
			tMyInfo = []
			tMyInfo.append(self.getRank(who.id))
			tMyInfo.append(who.name)
			guildName = who.getGuildName()
			if not guildName:
				guildName = "—"
			tMyInfo.append(guildName)#所在帮派
			tMyInfo.append(rank.rankCompositeScore(who))
			return tMyInfo

		

import rank.service
import rank.load
import rank_pb2
import rank