# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''组队平台
	'''

	def getParseTxt(self):
		lineList = self.parseTxtTo2dGroup()
		if not lineList:
			return "{\n}"

		titleList = lineList.pop(0)
		tFieldName = ("任务名字", "一键喊话频道", "目标类型", "活动等级", "活动时间类型", "活动开始时间", "活动结束时间", "可选目标", "可选范围1", "可选范围2", "默认选择范围")
		keyList = []
		valList = []
		keyList2 = []
		valList2 = []
		keyList3 = []
		valList3 = []

		for i, v in enumerate(lineList):
			if v[0]:
				keyList.append(v[0])
				#行动目标
				keyList2.append(tFieldName[0])
				valList2.append(v[1])
				#一键喊话频道
				keyList2.append(tFieldName[1])
				valList2.append(v[2])
				#目标类型
				keyList2.append(tFieldName[2])
				valList2.append(v[3])

			if v[4]:	#活动等级
				keyList2.append(tFieldName[3])
				valList2.append(v[4])
			if v[5] and v[5].find("$NONE$") == -1:	#活动时间类型
				keyList2.append(tFieldName[4])
				valList2.append(v[5])
			if v[6] and v[6].find("$NONE$") == -1:	#活动开始时间
				keyList2.append(tFieldName[5])
				valList2.append(v[6])
			if v[7] and v[7].find("$NONE$") == -1:	#活动结束时间
				keyList2.append(tFieldName[6])
				valList2.append(v[7])
					#默认选择范围

			if v[8]:
				keyList4 = tFieldName[8:]
				valList4 = [x for x in v[9:]]
				#可选目标
				keyList3.append(v[8])
				valList3.append(self.makeDict(keyList4, valList4, False))
			
			if self.isLastInGroup(lineList, i, 0):
				if keyList3:
					keyList2.append(tFieldName[7])
					valList2.append(self.makeDict(keyList3, valList3, True, 3))
				valList.append(self.makeDict(keyList2, valList2, True, 2))

				keyList2 = []
				valList2 = []
				keyList3 = []
				valList3 = []
		
		return self.makeDict(keyList, valList, True, 1)







