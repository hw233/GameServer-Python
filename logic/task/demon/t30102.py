# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

difficulty = {3001:"简单",3002:"普通",3003:"困难","F9006":"简单","F9007":"普通","F9008":"困难"}
#导表开始
class Task(customTask):
	parentId = 30102
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''厉魔'''
	intro = '''$target为祸世间，请速去捉拿'''
	detail = '''$target已经逃出了禁闭之地，四处作恶，请速速将其捉拿'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NE(9002,1004)'''
#导表结束

	def getHelpScoreMax(self):
		return self.getRefObj().globalInfo.get(30101).get("每周帮打降魔积分上限", 0)

	def getRefObj(self):
		'''关联对象
		'''
		return task.getTask(30101)

	# def handleTeamConfirm(self):
	# 	'''全队人员确认
	# 	'''
	# 	msg = "您确定挑战{}任务吗？\nQ取消\nQ确定".format(self.title)
	# 	ownerObj = getRole(self.ownerId)
	# 	if not ownerObj:
	# 		return 0
	# 	teamObj = ownerObj.getTeamObj()
	# 	leader = teamObj.leader
	# 	teamId = teamObj.id
	# 	dJobs={pid:myGreenlet.cGreenlet.spawn(message.confirmBox, pid, msg) for pid in teamObj.getInTeamList()}
	# 	gevent.joinall(dJobs.values(),None,True)
	# 	res = True
	# 	for pid,job in dJobs.iteritems():
	# 		if not job.value:
	# 			res = False
	# 			continue
	# 		if job.value != 2:
	# 			res = False
	# 			continue
	# 		obj = getRole(pid)
	# 		if not obj:
	# 			res = False
	# 		elif not obj.getTeamObj():
	# 			res = False
	# 		elif obj.getTeamObj().id != teamId:
	# 			res = False
	# 		elif not pid in teamObj.getInTeamList():
	# 			res = False
	# 	return res

	def validDoEventScript(self, who, npcObj, key):
		if key in ("点击", "回复"):
			if not who.validInTeamSize(3):
				message.tips(who, self.getRefObj().chatInfo.get(1001))
				self.doScript(who, npcObj, "TM1001")
				return 0
			for obj in self.getRoleList():
				if obj.level < 20:
					self.doScript(obj, npcObj, "TM1002")
					return 0
		return 1

	def onMissionDone(self, who, npcObj):
		if self.id == 30102:
			pass

	def transNpcInfo(self, npcIdx, info, who=None):
		if "$name" in info["名称"]:
			info["名称"] = self.createRandName()
		if "$pos" in info["位置"]:
			info["位置"] = self.createRandPos()
		return customTask.transNpcInfo(self, npcIdx, info, who)

	def getNameInfo(self, idx):
		return self.getRefObj().nameInfo.get(idx)

	def createRandName(self):
		idxList = self.getRefObj().nameInfo.keys()
		idxList.sort()
		nameParts = []
		for idx in idxList:
			lst = self.getNameInfo(idx)
			part = lst[rand(len(lst))]
			nameParts.append(part)
		return "".join(nameParts)

	def createRandPos(self):
		# 获取sceneId的途径
		# TODO
		sceneId = 1130
		x, y = scene.randSpace(sceneId)
		return "%d,%d,%d,0" % (sceneId, x, y)

	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利
		'''
		leader = getRole(self.ownerId)
		if leader:
			self.onWarWin(warObj, npcObj, leader)
		else:
			raise Exception, "team leader not found!"

	def rewardTeam(self, who, rwdIdx, npcObj=None):
		'''奖励队伍
		'''
		teamObj = who.getTeamObj()
		leaderId = 0
		if teamObj:
			lst = teamObj.getInTeamList()
			leaderId = teamObj.leader
		else:
			lst = [who.id]
		tag="taskFirstBoss{}".format(rwdIdx)
		for pid in lst:
			rewardId = rwdIdx
			obj = getRole(pid)
			if not obj:
				continue
			if 1 == obj.day.fetch(tag):
				msg = "今天已战胜过#C02{}·{}#n难度，只能获得#C04降魔积分#n".format(self.title,difficulty.get(rwdIdx))
				message.tips(obj,msg)
				message.message(obj,msg)
				rewardId = rwdIdx + 1000#和策划说好了发放+1000后的配置奖励
			elif 1 < obj.day.fetch(tag):
				msg = "今天已战胜#C02{}·{}#n超过#C042#n次，无法获得任何奖励".format(self.title,difficulty.get(rwdIdx))
				message.tips(obj,msg)
				message.message(obj,msg)
				continue
			obj.day.add(tag, 1)
			if leaderId == obj.id:
				self.rewardLeader(obj, rewardId, npcObj)
			else:
				self.reward(obj, rewardId, npcObj)
		
	def rewardLeader(self, who, rwdIdx, npcObj=None):
		'''奖励
		'''
		self.log("%d reward %d" % (who.id, rwdIdx))
		self.initTmpReward(who.id)
		ratio = 1.1		# 队长奖励系数
		info = self.getRewardInfo(rwdIdx)
		for _type in info.iterkeys():
			if _type in ("传闻",):
				continue
			val = info[_type]
			if not val:
				continue
			val = self.transCodeForReward(val, _type, who)
			self.rewardLeaderByType(who, val, _type, ratio)
		if info.get("传闻"):
			# toDo 传闻  message.annouce(self.getText(info["传闻"]))
			pass

	def rewardLeaderByType(self, who, val, _type, ratio):
		'''根据类型奖励
		'''
		roleId = who.id
		self.initTmpReward(roleId)

		if type(val) == types.StringType:
			return template.Template.rewardByType(self, who, val, _type)
		if _type == "经验":
			val = int(val * ratio)
			who.rewardExp(val, self.name)
		elif _type == "宠物经验":
			val = int(val * ratio)
			self.rewardPetExp(who, val)
		elif _type == "银币":
			val = int(val * ratio)
			who.rewardCash(val, self.name)
		elif _type == "物品":
			for rwdIdx in val:
				self.rewardLeaderProps(who, rwdIdx, ratio)
		elif _type == "宠物":
			self.rewardPet(who, val)

	def rewardLeaderProps(self, who, rwdIdx, ratio, total=0):
		'''奖励物品
		'''
		info = self.getRewardPropsInfo(rwdIdx)
		idx = self.chooseKey(info, total=total, key="权重", factor=ratio)
		if idx is None:
			return
		info = info[idx]
		if info["物品"] in ("", "0",):
			return
		propsNo, args, kwargs = misc.parseItemInfo(info["物品"])
		amount = int(self.transCodeForReward(info["数量"], "数量", who))
		binded = info.get("绑定", 0)
		propsNo = str(self.transIdxByGroup(propsNo))
		if not propsNo:
			return
		if not hasattr(self, "customRewardProps") or not self.customRewardProps(who, propsNo, amount, args, kwargs, binded):
			#launch.launchForTask(who, int(propsNo), amount, binded, self.name)
			self.launchProps(who, int(propsNo), amount, binded)
		if info.get("传闻"):
			# toDo 传闻  message.annouce(self.getText(info["传闻"]))
			pass

	def chooseKey(self, data, total=0, key=None, filt=None, factor=0):
		'''根据几率选出一项
		key: 指定哪一项是概率
		filt: 过滤函数
		factor: 额外系数
		'''
		if isinstance(data, (list, tuple)):
			data = {i:v for i,v in enumerate(data)}

		ratioList= {}
		for k,v in data.iteritems():
			if filt and not filt(k, v):
				continue
			if key:
				ratio = v[key]
			else:
				ratio = v
			ratioList[k] = ratio
		
		if total == 0:
			total = sum(ratioList.values())
		n = rand(total) * factor
		m = 0
		for k,ratio in ratioList.iteritems():
			m += ratio
			if n < m:
				return k
		return None

	def customEvent(self, who, npcObj, eventName, *args):
		m = re.match("check(\S+)", eventName)
		if m:
			subEvent = m.group(1)
			teamObj = who.getTeamObj()
			if not teamObj:
				return
			msg = self.getRefObj().chatInfo.get(3000)
			msg = msg.replace("$target",self.title)
			msg = msg.replace("$difficulty",difficulty.get(subEvent))
			message.teamConfirmBox(teamObj, functor(self.handleCheck, who.id, npcObj.id, subEvent), self.title, msg, 60)

	def handleCheck(self, pid, npcId, eventName):
		who = getRole(pid)
		if not who:
			return
		npcObj = getNpc(npcId)
		if not npcObj:
			return
		# if not self.handleTeamConfirm():
		# 	return
		self.doScript(who, npcObj, eventName)

	def setupWar(self, warObj, who, npcObj):
		'''战斗设置,设置为手动战斗
		'''
		warObj.setAutoFight(False)


import types
from common import *
import task
import scene
import template
import misc
import launch
import message
import gevent
import myGreenlet
