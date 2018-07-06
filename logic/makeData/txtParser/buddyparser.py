#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#配置型分析器,字典内嵌字典
class cTxtParser(makeData.txtParser.cTxtParser):

	initList = [{},{},{},{},{}]
	
	def getParseTxt(self):#override
		dataList = self.parseTxtTo2Dict()
		if not dataList:
			return "{\n}"

		txtList = []
		lKeys = []
		lvales = []
		for data in dataList:
			keyList = []
			valueList = []
			effectList = [{},{},{},{},{}]
			for key,value in data.items():
				if key == "序号" or key == "评分":
					lKeys.append(value)
					continue
				if "羁绊" not in key:
					keyList.append(key)
					valueList.append(value)
				else:
					index = eval(key[0])-1
					effectList[index] = value

			if effectList != self.initList:
				effectList = self.makeTuple(effectList)
				keyList.append("效果")
				valueList.append(effectList)
			sTemp=self.makeDict(keyList,valueList,False)
			lvales.append(sTemp)
			
		return self.makeDict(lKeys,lvales,True)

	def customFormatData(self, titleName, val, fmt):
		if "羁绊" in titleName or "型" in titleName:
			return self.transEffect(val)
		return self.formatData(val, fmt)

	def transEffect(self,effectListStr):
		if not effectListStr:
			return ""

		effectListStr = transApplyList(effectListStr, False, 0)
		return "{%s}" % effectListStr


import u
from makeData.defines import *