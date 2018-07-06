# -*-coding:utf-8-*-
'''入世修行(任务链)
'''
import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		content = self.getChat()
		selList = []
		content += "\nQ领取入世修行"
		selList.append(1)
		content += "\nQ取消入世修行"
		selList.append(2)
		content += "\nQ入世修行说明"
		selList.append(3)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.takeRingTask(who)
		elif sel == 2:
			self.cancelRingTask(who)
		elif sel == 3:
			self.illustrate(who)

	def takeRingTask(self, who):
		'''领取入世修行
		'''
		taskObj = task.hasTask(who, 30601)
		if taskObj:
			self.say(who, "你已经领取了入世修行了，不要在此胡闹！")
			return
		if who.week.fetch("ringTask"):
			self.say(who, "你本周已领取过一次入世修行，请下周再来吧。")
			return
		taskObj = task.getTask(30601)
		openLv = taskObj.configInfo.get(1005, 50)
		if who.level < openLv:
			self.say(who, "你实力不足以应付这些考验，等你达到50级后再来吧")
			return
		iCash = taskObj.configInfo.get(1001, 200000)
		content = "开启入世修行需要银币{:,}，是否消耗银币{:,}并开启入世修行\nQ取消#10\nQ确定".format(iCash, iCash)
		message.confirmBoxNew(who, functor(self.responseTakeRingTask, iCash), content)

	def responseTakeRingTask(self, who, yes, iCash):
		if not yes:
			return
		if not money.checkCash(who, iCash):
			return
		if task.ring.randRingTask(who, self):
			who.week.set("ringTask", 1)
			who.addCash(-iCash, "领取入世修行消耗", None)
			message.message(who, "消耗#R<{},3,2>#n开启入世修行".format(iCash))
			message.tips(who, "成功开启入世修行")
		else:
			message.tips(who, "没有适合的入世修行任务可以接取")

	def cancelRingTask(self, who):
		'''取消入世修行
		'''
		taskObj = task.hasTask(who, 30601)
		if not taskObj:
			self.say(who, "你没有可取消的入世修行任务")
			return
		content = "入世修行每周仅能领取一次，若放弃上周领取的入世修行，可继续领取本周的入世修行\nQ取消#10\nQ确定"
		message.confirmBoxNew(who, functor(self.responseCancelRingTask, taskObj.id), content)
		
	def responseCancelRingTask(self, who, yes, taskId):
		if not yes:
			return
		taskObj = task.hasTask(who, taskId)
		if not taskObj:
			return
		task.removeTask(who, taskObj.id)
		who.taskCtn.delete("ringRing")
		self.say(who, "入世修行任务已放弃")

	def illustrate(self, who):
		'''任务说明
		'''
		content = "1.大于或等于50级的玩家可领取入世修行\n2.入世修行由200环任务组成，每完成一环任务都可以获得经验奖励\n3.每完成100环任务可获得物品奖励\n4.入世修行战斗可组队完成\n5.遇到难度太大的任务可尝试发送入世修行求助"
		self.say(who, content)


import message
import money
from common import *
import task
import task.ring
