# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def __init__(self, taskId, *parsers):
		self.taskId = taskId
		super(PyMaker, self).__init__(*parsers)
	
	def getName(self):
		return "任务%s" % self.taskId
	
	def transIdx(self, idx):
		return "%05d" % idx

	def getMainModName(self, idx):
		return "task.%s.t%s" % (self.path, self.transIdx(idx))
	
	def getLoadModName(self):
		return "task.load"
	
	def getHeadContent(self, idx):
		content = '''# -*- coding: utf-8 -*-
from task.defines import *
'''
		if idx == self.taskId:
			content += "from task.object import Task as customTask%s" % LINE_SEP
		else:
			content += "from task.%s.t%s import Task as customTask%s" % (self.path, self.transIdx(self.taskId), LINE_SEP)
		return content
	
	def getMainContent(self, idx, data):
		parentId = data.get("父任务编号")
		if not parentId:
			parentId = self.taskId
		targetType = task.defines.getTargetTypeDesc(data["目标类型"])
		icon = data["图标"]
		title = data["标题"]
		intro = data["简介"]
		detail = data["详情"]
		rewardDesc = data.get("奖励描述", "")
		goAheadScript = data.get("前往脚本", "")
		initScript = data.get("初始化脚本", "")
		
		dataList = []
		dataList.append("class Task(customTask):")
		dataList.append("parentId = %s" % parentId)
		dataList.append("targetType = %s" % targetType)
		dataList.append("icon = %s" % icon)
		dataList.append("title = '''%s'''" % title)
		dataList.append("intro = '''%s'''" % intro)
		dataList.append("detail = '''%s'''" % detail)
		dataList.append("rewardDesc = '''%s'''" % rewardDesc)
		dataList.append("goAheadScript = '''%s'''" % goAheadScript)
		dataList.append("initScript = '''%s'''" % initScript)
		
		if idx == self.taskId:  # 父任务
			for parser in self.tParser:
				if parser.getVarName() in ("main",):
					continue
				dataList.append("%s%s = %s" % (LINE_SEP, parser.getVarName(), parser.getParseTxt()))

		return indent(LINE_SEP.join(dataList), 1, False)
	
	def makeToPyFile(self):
		self.loadConfig()
		super(PyMaker, self).makeToPyFile()
		
	def loadConfig(self):
		'''加载配置
		'''
		configParser = self.getParserByName("configInfo")
		configInfo = configParser.getParseTxt()
		if not configInfo:
			raise Exception("%s表错误" % configParser.sTextName)
		
		configInfo = eval(configInfo)
		self.path = configInfo["生成路径"]
		self.pathReal = "logic/task/%s" % self.path
# 		if not taskTypeData.getConfig(self.taskType, "名称"):
# 			raise Exception("不存在的任务类型:%s" % self.taskType)
		if not os.path.exists(self.pathReal):
			raise Exception("目标生成目录不存在:%s" % self.pathReal)

from makeData.defines import *
import os
import task.defines