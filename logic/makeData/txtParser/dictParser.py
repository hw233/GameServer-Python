# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''二层字典导表
	'''
	
	def getParseTxt(self):
		lineList = self.parseTxtTo2dGroup()
		if not lineList:
			return "{\n}"

		titleList = lineList.pop(0)
		keyList = []
		key2List = []
		valList = []
		tmpList = []
		lastKey = None
		for i, v in enumerate(lineList):
			if v[0]:
				lastKey = v[0]

			key2List.append(v[1])
			tmpList.append(self.makeDict(titleList[2:], v[2:], False))
			if self.isLastInGroup(lineList, i, 0):
				keyList.append(lastKey)
				valList.append(self.makeDict(key2List, tmpList, True, 2))
				tmpList = []
				key2List = []
				lastKey = None

		return self.makeDict(keyList, valList, True, 1)







