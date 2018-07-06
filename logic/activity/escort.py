# -*- coding: utf-8 -*-
'''
运镖
'''
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
		10101:{"名字":"小男孩","称号":"被护送的委托人","造型":"2006(0,1,0,0,0,0)","染色":"0,0,0,0,0"},
		10102:{"名字":"小女孩","称号":"被护送的委托人","造型":"2008(0,1,0,0,0,0)","染色":"0,0,0,0,0"},
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		1001:'''运镖次数已用完''',
		1002:'''等级不足，领取该任务需达到35级''',
		1003:'''该任务组队状态无法领取，请退出组队后再次领取''',
		1004:'''活跃度不足，领取该任务需活跃度达到55''',
		1005:'''战斗失败扣除10%运镖奖励''',
		1006:'''运镖中，无法进行该操作''',
		1007:'''交付押金#IS#n$cash，护送一趟镖？\nQ取消#10\nQ确定''',
		1008:'''是否终止运镖，终止运镖不扣除次数但该次运镖押金不返还。\nQ取消#10\nQ确定''',
		1009:'''是否返回镖师处再次领取任务？\nQ取消\nQ确定''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
		"开启等级":35,
		"所需活跃度":55,
		"次数":3,
		"押金":100000,
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)

	def getText(self, chatIdx, pid=0):
		content = self.transString(self.getChatInfo(chatIdx), pid)
		content = content.replace("$cash", "{:,}".format(self.getDeposit()))
		return content

	def init(self):
		pass

	def getOpenLevel(self):
		return self.configInfo.get("开启等级", 30)

	def getNeedActPoint(self):
		return self.configInfo.get("所需活跃度", 55)

	def getMaxCount(self):
		return self.configInfo.get("次数", 3)

	def getDeposit(self):
		return self.configInfo.get("押金", 250000)

	def doEscort(self, who, npcObj):
		'''开始运镖
		'''
		if task.hasTask(who, 30301):
			message.tips(who, "你已经领取了运镖任务了，赶紧完成吧！")
			return
		taskObj = task.newTask(who, npcObj, 30301)
		if not taskObj:
			return
		taskObj.set("start", getSecond())
		lst = self.npcInfo.keys()
		npcId = lst[rand(len(lst))]
		taskObj.set("escortNpc", npcId)
		self.escort(who, taskObj)

	def escort(self, who, taskObj):
		who.setEscort()
		rpcEscortInfo(who, self, taskObj)
		npcId = taskObj.fetch("escortNpc")
		npcInfo = self.npcInfo.get(npcId, {})
		follow = scene_pb2.followMsg()
		follow.iFollowNo = npcId
		info = scene_pb2.npcInfo()
		shape, shapeParts = template.transShapeStr(npcInfo["造型"])
		info.iShape = shape
		info.shapeParts.extend(shapeParts)
		colors = template.transColorsStr(npcInfo["染色"])
		info.colors.extend(colors)
		info.sName = npcInfo.get("名字", "")
		info.title = npcInfo.get("称号", "")
		follow.followInfo.CopyFrom(info)
		scene.addFollow(who, follow)
		who.escortFollow = npcId
		taskObj.goAhead(who)

	def doneEscort(self, who):
		'''完成运镖
		'''
		who.setEscort(False)
		who.endPoint.rpcEscortDone()
		scene.delFollow(who, who.escortFollow)

	def onLogin(self, who, bRelogin):
		taskObj = task.hasTask(who, 30301)
		if taskObj:
			self.escort(who, taskObj)

def rpcEscortAbort(who, reqMsg):
	taskObj = who.taskCtn.getItem(30301)
	if not taskObj:
		message.tips(who, "你还未领取运镖任务")
		return
	actObj = activity.getActivity("escort")
	if not actObj:
		return
	taskObj.abort(who)
	actObj.doneEscort(who)

def rpcEscortQuest(who, reqMsg):
	message.tips(who, "该功能尚未开放")

def rpcEscortQuestGoAhead(who, reqMsg):
	message.tips(who, "该功能尚未开放")

def rpcEscortInfo(who, actObj, taskObj):
	msg = act_escort_pb2.escortMsg()
	npcObj = taskObj.getTargetNpc()
	msg.sceneName = scene.getScene(npcObj.sceneId).name
	msg.npcName = npcObj.name
	msg.time = taskObj.fetch("start", getSecond())
	who.endPoint.rpcEscortInfo(msg)

def rpcEscortGoAheadNpc(who):
	pass


from common import *
import message
import task
import act_escort_pb2
import scene
import scene_pb2
import activity
import role
import template
