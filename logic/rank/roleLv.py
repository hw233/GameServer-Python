#-*-coding:utf-8-*-
import rank.object

class cRanking(rank.object.cRanking):
	'''角色等级排行榜
	'''
	def title3(self, iUid):#override
		return self.getGuildName(iUid)

	def updateExp(self, who):#更新成绩
		iUid = who.id
		iRank = self.getRank(iUid)
		if not iRank and iUid not in self.dBuffer and len(self.lRanking) > self.iStoreSize:#没上榜也没缓存
			return
		self.updateScore(who.id, who.name, who.level, who.level, who.school, exp=who.exp)
		
	def addRank(self, who):#override
		self.updateScore(who.id, who.name, who.level, who.level, who.school, exp=who.exp)

	# def lookInfo(self, who, other, iUid):#override
	# 	dMsg = hyperlink.service.packetRole(other)
	# 	who.endPoint.rpcRoleHyperlink(**dMsg)

	#等级高到低	经验多到少	角色ID小到大
	#override
	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1
		
		iExp1 = self.dIdNameValue[iUid1][4].get("exp", 0)
		iExp2 = self.dIdNameValue[iUid2][4].get("exp", 0)
		if iExp1<iExp2:
			return 1
		elif iExp1>iExp2:
			return -1
		
		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def _checkRankValueComparer(self, iUid):#override
		iExp1 = self.dIdNameValue[iUid][4].get("exp", 0)
		iExp2 = self.dBuffer[iUid][4].get("exp", 0)
		if iExp1 != iExp2:
			return False
		return rank.object.cRanking._checkRankValueComparer(self, iUid)

	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		guildName = who.getGuildName()
		if not guildName:
			guildName = "—"
		tMyInfo.append(guildName)#所在帮派
		tMyInfo.append(who.level)
		return tMyInfo

import hyperlink.service
import role.defines
import resume