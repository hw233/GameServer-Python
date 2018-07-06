#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#抽奖概率分布表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lPosList=[]
		lProbabilityList=[]
		lLvRef=[]
		lLvValue=[]
		tLv = ()
		lQty = []
		sLotty = ""

		lLines=self.parseTxtTo2dGroup()
		lKeys = [[lLine[0],lLine[2]] for lLine in lLines]
		for iRow,lLine in enumerate(lLines):

			lPosList.append(lLine[2])
			lProbabilityList.append(lLine[3])
			if not tLv:
				tLv = lLine[0]
			if not lQty:
				lQty = lLine[1]

			if self.isLastInGroup(lKeys,iRow,0):
				sLotty = self.makeDict(lPosList,lProbabilityList,True,3)
				lRefKey = []
				lRefValue = []
				lRefKey.append("qty")
				lRefValue.append(lQty)
				lRefKey.append("lotty")
				lRefValue.append(sLotty)
				sValue = self.makeDict(lRefKey,lRefValue,True,2)
				lLvRef.append(tLv)
				lLvValue.append(sValue)
				tLv = ()
				lQty = []
				lPosList=[]
				lProbabilityList=[]
		return self.makeDict(lLvRef,lLvValue,True,1)