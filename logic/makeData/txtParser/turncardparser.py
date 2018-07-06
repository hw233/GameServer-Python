#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#小游戏-翻卡片 分析器(已弃用)
class cTxtParser(makeData.txtParser.cTxtParser):

	#override
	def getParseTxt(self):
		tFieldName=("Item","Amount","IsBind","Notify","condition")
		lKey=[]
		lVal=[]

		sKey0=""
		lTupleItem=[]
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeDict(tFieldName,lLine[1:],False)
			lTupleItem.append(sTemp)

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeTuple(lTupleItem,True,2)
				lTupleItem=[]
				lKey.append(sKey0)
				lVal.append(sTemp)

		return self.makeDict(lKey,lVal,True,1)