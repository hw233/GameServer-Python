# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''多行导表，如物品奖励表、战斗表、分支脚本表
	'''

	def getParseTxt(self):
		lineList = self.parseTxtTo2dGroup()
		if not lineList:
			return "{\n}"

		titleList = lineList.pop(0)
		keyList = []
		valList = []
		tmpList = []
		lastKey = None
		for i, v in enumerate(lineList):
			if v[0]:
				lastKey = v[0]
			tmpList.append(self.makeDict(titleList[1:], v[1:], False))
			if self.isLastInGroup(lineList, i, 0):
				keyList.append(lastKey)
				valList.append(self.makeTuple(tmpList, True, 2))
				tmpList = []
				lastKey = None
		
		return self.makeDict(keyList, valList, True, 1)







