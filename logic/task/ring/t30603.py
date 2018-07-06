# -*- coding: utf-8 -*-
from task.defines import *
from task.ring.t30601 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30601
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''入世修行'''
	intro = '''收集$props(拥有$process)'''
	detail = '''帮$target收集$props(拥有$process)'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''PW1002,E(9015,1004),I(203021,1)'''
#导表结束

	def getHyperLink(self, who):
		'''获取任务求助超链接
		'''
		propsNeeded = self.getPropsNeeded()
		if not propsNeeded:
			return
		propsNo = propsNeeded.keys()[0]
		if propsGroupData.isPropsGroup(propsNo):
			propsName = propsGroupData.getConfig(propsNo, "名字", "名字")
		else:
			propsName = props.getCacheProps(propsNo).name
		iRing = self.getRing(who)
		sLink = "#L2<{},3,{},{}>*[{}]*08#n".format(who.id, self.getUniqueId(), self.id, propsName)
		content = "我在{}环#L1<14,20>*[入世修行]*02#n中需求{}，请求帮助".format(iRing, sLink)
		return content

	def offerHelp(self, who):
		'''提供帮助
		'''
		sHelpCnt = self.configInfo.get(5006, "1") # 帮助次数
		cnt = eval(sHelpCnt.replace("LV", str(who.level)))
		if who.week.fetch("ringHelped") >= cnt:
			message.tips(who, "本周帮助次数已达上限")
			return
		npcObj = self.getTargetNpc()
		if not self.hasAllNeededProps(who):
			self.popHelpGoodsUI(who)
			return
		self.popHelpPropsUI(who, npcObj)

	def release(self):#override
		'''释放
		'''
		customTask.release(self)
		# 删除任务物品
		who = self.getOwnerObj()
		if who:
			who.propsCtn.removePropsByNo(203021)
			state.removeState(who, 107)


import props
import state
import propsGroupData
