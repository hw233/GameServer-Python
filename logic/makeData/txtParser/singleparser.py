# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''单项导表，如对白表
	'''

	def getParseTxt(self):
		lineList = self.parseTxtTo2dGroup()
		if not lineList:
			return "{\n}"

		titleList = lineList.pop(0)
		keyList = []
		valList = []
		for i, v in enumerate(lineList):
			keyList.append(v[0])
			valList.append(v[1])
		
		return self.makeDict(keyList, valList, True, 1)







