#-*-coding:utf-8-*-
import rank.object

class cRanking(rank.object.cRanking):
	'''宠物排行榜
	'''
	def title3(self, iPetId):#override
		'''宠物名称
		'''
		return self.getRoleArgs(iPetId).get("petName", "")

	def quitRank(self, who):#override
		if self.iRankNo == rank.defines.giPetScoreRankNo:	#只有宠物总榜才能操作
			rank.allPetQuitRank(who)

	def addRank(self, who):#override
		if self.iRankNo == rank.defines.giPetScoreRankNo:	#只有宠物总榜才能操作
			rank.allPetAddRank(who)

	def lookInfo(self, who, other, iUid):#override
		petObj = other.petCtn.getItem(iUid)
		if not petObj:
			message.tips(who, "要查看的宠物已消失")
			return
		who.endPoint.rpcPetHyperlink(pet.service.packPetData(petObj))

	def getConfig(self, key, default):#override
		return RankData.gdData.get(rank.defines.giPetScoreRankNo, {}).get(key, default)

	def getMyRankInfo(self, who):#override
		'''我的名次信息:最高战力宠物排行
		'''
		petObj = None
		if self.iRankNo == rank.defines.giPetScoreRankNo:	#只有宠物总榜才能操作
			iMaxRank = 10000
			iMaxRankPetId = 0
			iMaxScore = 0
			iMaxScorePetId = 0
			for petObj in who.petCtn.getAllValues():
				iRank = self.getRank(petObj.id)
				if iRank and iRank < iMaxRank:
					iMaxRank = iRank
					iMaxRankPetId = petObj.id

				if not iMaxRankPetId:	#没有上榜宠物找最高评分的
					iScore = petObj.getScore()
					if iScore > iMaxScore:
						iMaxScore = iScore
						iMaxScorePetId = petObj.id

			if iMaxRankPetId:
				petObj = who.petCtn.getItem(iMaxRankPetId)
			elif iMaxScorePetId:
				petObj = who.petCtn.getItem(iMaxScorePetId)
		else:
			iMaxScore = 0
			for _petObj in who.petCtn.getAllValues():
				if _petObj.idx == self.iRankNo:
					iScore = _petObj.getScore()
					if iScore > iMaxScore:
						iMaxScore = iScore
						petObj = _petObj

		if not petObj:
			return []

		tMyInfo = []
		tMyInfo.append(self.getRank(petObj.id))
		tMyInfo.append(who.name)
		tMyInfo.append(petObj.name)
		tMyInfo.append(petObj.getScore())
		return tMyInfo

	def roleChangeInfo(self, who):#override
		'''角色信息改变
		'''
		for petObj in who.petCtn.getAllValues():
			iUid = petObj.id
			if iUid in self.dIdNameValue:
				self.dIdNameValue[iUid][0] = who.name
				self.dIdNameValue[iUid][2] = who.level
				self.markDirty()

			if iUid in self.dBuffer:
				self.dBuffer[iUid][0] = who.name
				self.dBuffer[iUid][2] = who.level

import pet.service
import message
import rank
import rank.defines
import RankData