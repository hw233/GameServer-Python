# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return "门派法术"

	def getMainModName(self, idx):
		return "perform.school.pf%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "perform.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import %s as CustomPerform
''' % self.performTypeName
	
	def getMainContent(self, idx, data):
		if not data.get("法术"):
			return None

		self.performTypeName = performTypeNameDesc[data.get("类型", "无")]
		
		dataList = []
		dataList.append("class Perform(CustomPerform):")
		dataList.append("id = %s" % idx)
		dataList.append("name = \"%s\"" % data["名称"])
		if data.get("五行"):
			dataList.append("fiveEl = %s" % fiveElDesc2ValStr[data["五行"]])
		if data.get("作用目标"):
			dataList.append("targetType = %s" % targetTypeNameDesc[data["作用目标"]])
		if data.get("作用人数"):
			dataList.append("targetCount = %s" % data["作用人数"])
		if data.get("最大作用人数"):
			dataList.append("targetCountMax = %s" % data["最大作用人数"])
		if data.get("持续回合"):
			dataList.append("bout = %s" % data["持续回合"])
		if data.get("最大持续回合"):
			dataList.append("boutMax = %s" % data["最大持续回合"])
		if data.get("准备回合"):
			dataList.append("readyBout = %s" % data["准备回合"])
		if data.get("冷却回合"):
			dataList.append("frozenBout = %s" % data["冷却回合"])
		if data.get("伤害"):
			dataList.append("damage = %s" % data["伤害"])
		if data.get("威力"):
			dataList.append("power = %s" % data["威力"])
			
		consumeList = []
		if data.get("真气消耗"):
			consumeList.append('"真气": %s' % data.get("真气消耗"))
		if data.get("生命消耗"):
			consumeList.append('"生命": %s' % data.get("生命消耗"))
		if data.get("愤怒消耗"):
			consumeList.append('"愤怒": %s' % data.get("愤怒消耗"))
		if data.get("符能消耗"):
			consumeList.append('"符能": %s' % data.get("符能消耗"))
		if consumeList:
			consumeList = ",\n".join(consumeList)
			dataList.append("consumeList = {\n%s,\n}" % indent(consumeList, 1))
			
		recoverList = []
		if data.get("符能回复"):
			recoverList.append('"符能": %s' % data.get("符能回复"))
		if recoverList:
			recoverList = ",\n".join(recoverList)
			dataList.append("recoverList = {\n%s,\n}" % indent(recoverList, 1))
			
		if data.get("buff"):
			dataList.append("buffId = %s" % data["buff"])
		if data.get("速率"):
			dataList.append("speRatio = %s" % data["速率"])
		if data.get("命中率"):
			dataList.append("hitRatio = %s" % data["命中率"])
		if data.get("法术效果"):
			applyList = transApplyList(data["法术效果"])
			dataList.append("applyList = {\n%s\n}" % applyList)
		if data.get("配置数据"):
			configInfo = transApplyList(data["配置数据"])
			dataList.append("configInfo = {\n%s\n}" % configInfo)
			
		if hasattr(self, "customMainContent"):
			dataList.extend(self.customMainContent(idx, data))
			
		return indent(LINE_SEP.join(dataList), 1, False)

from makeData.defines import *
from perform.defines import *