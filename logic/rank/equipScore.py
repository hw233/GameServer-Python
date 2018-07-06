#-*-coding:utf-8-*-
import rank.object
from props.defines import *


gdSubNoMapEquipPos = {
	401:EQUIP_WEAPON,	#武器
	402:EQUIP_CLOTHES,	#衣服	
	403:EQUIP_HEAD,		#帽子
	404:EQUIP_NECKLACE,	#饰品
	405:EQUIP_BELT,		#腰带
	406:EQUIP_SHOES,	#鞋子
}
class cRanking(rank.object.cRanking):
	'''角色装备排行榜
	'''
	def title3(self, iUid):#override
		'''装备名称
		'''
		idx = self.getRoleArgs(iUid).get("idx", 0)
		return equipData.getConfig(idx, "名称", "")

	def addRank(self, who):#override
		iWearPos = gdSubNoMapEquipPos.get(self.iRankNo, 0)
		oWearEquip = who.equipCtn.getEquipByWearPos(iWearPos)
		if not oWearEquip:
			return
		self.updateScore(who.id, who.name, oWearEquip.getScore(), who.level, who.school, idx=oWearEquip.idx, id=oWearEquip.id)

	def lookInfo(self, who, other, iUid):#override
		iPropsId = self.getRoleArgs(iUid).get("id", 0)
		oWearEquip = other.propsCtn.getItem(iPropsId)
		if not oWearEquip:
			oWearEquip = other.equipCtn.getItem(iPropsId)
		if not oWearEquip:
			message.tips(who,"该装备已经失效")
			return
		who.endPoint.rpcPropsHyperlink(oWearEquip.getMsg4Item(None,*oWearEquip.MSG_ALL))	

	def getMyRankInfo(self, who):#override
		'''我的名次信息
		'''
		iWearPos = gdSubNoMapEquipPos.get(self.iRankNo, 0)
		oWearEquip = who.equipCtn.getEquipByWearPos(iWearPos)
		if not oWearEquip:
			return []

		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(oWearEquip.name)
		tMyInfo.append(oWearEquip.getScore())
		return tMyInfo



import equipData
import rank_pb2
import props.equip
import message


