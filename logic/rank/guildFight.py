#-*-coding:utf-8-*-
import rank.object

class cRanking(rank.object.cRanking):
	'''帮派排行榜
	'''
	def title2(self, iUid):#override
		#帮派名称
		oGuild = guild.getGuild(iUid)
		if oGuild:
			return oGuild.name
		return "未知帮派"

	def title3(self, iUid):#override
		#帮主名称
		oGuild = guild.getGuild(iUid)
		if oGuild:
			return oGuild.chairmanName()
		return "未知帮主"

	def title4(self, iUid):
		#todo 帮战积分
		return 0

	def addRank(self, who):#override
		pass

	def lookInfo(self, who, other, iUid):#override
		pass

	def getMyRankInfo(self, who):#override
		'''我的名次信息
		'''
		oGuild = who.getGuildObj()
		if not oGuild:
			return []

		tMyInfo = []
		# tMyInfo.append(self.getRank(who.id))
		# tMyInfo.append(oGuild.anme)
		# tMyInfo.append(oGuild.chairmanName())
		# tMyInfo.append(0)	#todo 帮战积分
		return tMyInfo


import guild
