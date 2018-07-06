# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.NpcBase):
	
	def __init__(self):
		npc.object.NpcBase.__init__(self)
		self.name = "测试Npc"
	
	def doLook(self, who):
		content = '''请选择要测试的功能
Q测试输入框
Q测试选择框
Q测试确认框
Q测试组队确认框
Q测试物品上交
Q测试进度条'''
		message.selectBoxNew(who, self.responseLook, content, self)

	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.testInputBox(who)
		elif selectNo == 2:
			self.testSelectBox(who)
		elif selectNo == 3:
			self.testConfirmBox(who)
		elif selectNo == 4:
			self.testTeamConfirmBox(who)
		elif selectNo == 5:
			self.testPopPropsUI(who)
		elif selectNo == 6:
			self.testProgressBar(who)
			
	def testInputBox(self, who):
		'''测试输入框
		'''
		content = "请输入内容"
		message.inputBox(who, self.responseInputBox, "测试输入框", content)
		
	def responseInputBox(self, who, content):
		'''输入框回调处理
		'''
		self.say(who, "你输入了:{}".format(content))
			
	def testSelectBox(self, who):
		'''测试选择框
		'''
		content = '''请选择下面的选项
Q选项1
Q选项2
Q选项3'''
		message.selectBoxNew(who, self.responseSelectBox, content, self)
		
	def responseSelectBox(self, who, selectNo):
		'''选择框回调处理
		'''
		self.say(who, "你选择了选项{}".format(selectNo))
		
	def testConfirmBox(self, who):
		'''测试确认框
		'''
		content = '''请选择确认或取消
Q取消#20
Q确认'''
		message.confirmBoxNew(who, self.responseConfirmBox, content)
		
	def responseConfirmBox(self, who, yes):
		'''确认框回调处理
		'''
		if yes:
			self.say(who, "你选择了确认")
		else:
			self.say(who, "你选择了取消")
	
	def testTeamConfirmBox(self, who):
		teamObj = who.getTeamObj()
		if not teamObj:
			self.say(who, "请先组队再测试，人数不限")
			return
		message.teamConfirmBox(teamObj, functor(self.responseTeamConfirmBox, who.id), "标题", "内容", 60)

	def responseTeamConfirmBox(self, pid):
		'''组队确认框回调处理
		'''
		who = getRole(pid)
		if who:
			self.say(who, "全体同意确认")
			
	def testPopPropsUI(self, who):
		'''测试物品上交
		'''
		propsIdList = list(who.propsCtn.getAllKeys())
		message.popPropsUI(who, self.responsePopPropsUI, "测试物品上交", propsIdList)
		
	def responsePopPropsUI(self, who, propsList):
		propsObjList = []
		for propsId, amount in propsList.iteritems():
			propsObj = who.propsCtn.getItem(propsId)
			if not propsObj:
				message.tips(who, "你身上没有此物品")
				return
			if amount > propsObj.stack():
				message.tips(who, "上交的数量不对")
				return
			propsObjList.append(propsObj)
		
		propsNameList = []
		for propsObj in propsObjList:
			amount = propsList[propsObj.id]
			who.propsCtn.addStack(propsObj, -amount)
			if amount > 1:
				propsNameList.append("%sx%s" % (propsObj.name, amount))
			else:
				propsNameList.append("%s" % propsObj.name)
			
		content = "你上交了[%s]" % "、".join([propsName for propsName in propsNameList])
		self.say(who, content)
		
	def testProgressBar(self, who):
		title = "测试进度条"
		icon = 0
		ti = 3
		brk = True
		message.progressBar(who, self.responseProgressBar, title, icon, ti, brk)
		
	def responseProgressBar(self, who, isDone):
		if isDone:
			self.say(who, "进度条完成")
		else:
			self.say(who, "进度条中断")


from common import *
from qanda.defines import *
import message
